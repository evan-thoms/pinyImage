from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from connections import getConnections
from werkzeug.exceptions import abort
import pinyin
import requests
import re
import json 
import os
import logging
from dotenv import load_dotenv
from datetime import datetime

# Import our new models and config
from models import db, User, Card
from config import config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Configure database
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

charinput = ""
charPinyin = ""

def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s) 


@app.route('/api/post', methods=["POST"])
def addToDb():
    logger.info("addToDb called")
    try:
        formData = request.get_json()
        if not formData:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['title', 'pinyin', 'meaning', 'con']
        for field in required_fields:
            if field not in formData or not formData[field]:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400
        
        # Get default user (for now, we'll implement proper auth later)
        default_user = User.query.filter_by(username='default_user').first()
        if not default_user:
            # Create default user if it doesn't exist
            default_user = User(
                username='default_user',
                email='default@pinyimage.com',
                password_hash='default_user'
            )
            db.session.add(default_user)
            db.session.commit()
        
        # Create new card
        card = Card(
            user_id=default_user.id,
            title=formData['title'],
            pinyin=formData['pinyin'],
            meaning=formData['meaning'],
            con=formData['con']
        )
        db.session.add(card)
        db.session.commit()
        
        logger.info(f"Successfully added card: {formData['title']}")
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"Error adding to db: {e}")
        db.session.rollback()
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route("/api/result", methods=["POST"])
def result():
    logger.info("result function called")
    try:
        formData = request.get_json()
        if not formData or 'user_input' not in formData:
            return jsonify({"error": "No user input provided"}), 400
        
        uinput = formData['user_input'].strip()
        if not uinput:
            return jsonify({"error": "Empty input provided"}), 400
        
        # Get existing cards
        cards = Card.query.all()
        
        if contains_chinese_characters(uinput):
            try:
                info = getCharInfo(uinput)
                result = f"\nYour character {uinput} is pronounced {info[1]} and means {info[2]}. \nYour character uses radical #{info[3]}: {info[4]}, which means {info[5]}."
                connections = getConnections(charinput, charPinyin, info[2])
                
                return jsonify({
                    "result": result, 
                    "meaning": info[2], 
                    "connections": connections, 
                    "pinyin": charPinyin, 
                    "cards": [card.to_dict() for card in cards]
                })
            except Exception as e:
                logger.error(f"Error processing character {uinput}: {e}")
                # Fallback: provide basic info without external API
                try:
                    charPinyin = pinyin.get(uinput)
                    connections = getConnections(uinput, charPinyin, "character")
                    result = f"\nYour character {uinput} is pronounced {charPinyin}."
                    
                    return jsonify({
                        "result": result,
                        "meaning": "character",
                        "connections": connections,
                        "pinyin": charPinyin,
                        "cards": [card.to_dict() for card in cards]
                    })
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
                    return jsonify({
                        "error": "Unable to process character. Please try again later.",
                        "cards": [card.to_dict() for card in cards]
                    }), 500
        else:
            return jsonify({
                "result": "The input does not contain any Chinese characters.",
                "connections": "",
                "cards": [card.to_dict() for card in cards]
            })
            
    except Exception as e:
        logger.error(f"Error in result endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/cards')
def getCards():
    try:
        cards = Card.query.all()
        return jsonify([card.to_dict() for card in cards])
    except Exception as e:
        logger.error(f"Error fetching cards: {e}")
        return jsonify({"error": "Unable to fetch cards"}), 500

@app.route('/api/status')
def getStatus():
    """Get system status including AI service availability"""
    try:
        from ai_service import AIService
        from character_data_service import CharacterDataService
        
        ai_service = AIService()
        char_service = CharacterDataService()
        
        return jsonify({
            "ai_services": ai_service.get_available_services(),
            "ai_available": ai_service.is_available(),
            "character_service_available": char_service.is_available(),
            "database": "postgresql" if "postgresql" in app.config['SQLALCHEMY_DATABASE_URI'] else "sqlite",
            "environment": os.getenv("FLASK_ENV", "development"),
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({"error": "Unable to get status"}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    # Check AI service
    try:
        from ai_service import AIService
        ai_service = AIService()
        ai_status = "healthy" if ai_service.is_available() else "unhealthy"
    except Exception as e:
        logger.error(f"AI service health check failed: {e}")
        ai_status = "unhealthy"
    
    # Check character service
    try:
        from character_data_service import CharacterDataService
        char_service = CharacterDataService()
        char_status = "healthy" if char_service.is_available() else "unhealthy"
    except Exception as e:
        logger.error(f"Character service health check failed: {e}")
        char_status = "unhealthy"
    
    overall_status = "healthy" if all([db_status == "healthy", ai_status == "healthy"]) else "degraded"
    
    return jsonify({
        "status": overall_status,
        "services": {
            "database": db_status,
            "ai_service": ai_status,
            "character_service": char_status
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def getCharInfo(uinput):
    global charinput, charPinyin
    charinput = uinput
    logger.info(f"Getting character info for: {uinput}")
    
    try:
        from character_data_service import CharacterDataService
        char_service = CharacterDataService()
        
        # Get character info with fallbacks
        char_info = char_service.get_character_info(uinput)
        if not char_info:
            raise ValueError("Unable to get character information")
        
        charPinyin = pinyin.get(uinput)
        
        return (
            uinput,
            charPinyin,
            char_info['definition'],
            char_info['radical_number'],
            char_info['radical_character'],
            char_info['radical_meaning']
        )
        
    except Exception as e:
        logger.error(f"Error getting character info for {uinput}: {e}")
        # Fallback to basic info
        charPinyin = pinyin.get(uinput)
        return uinput, charPinyin, "character", "1", uinput, "basic character"

def getRads(radNumC):
    logger.info(f"Getting radical info for number: {radNumC}")
    try:
        radNumC = int(radNumC)
        with open("radicals.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        rad = None
        for item in data:
            if item['id'] == radNumC:
                rad = item
                break
        
        if not rad:
            logger.warning(f"Radical {radNumC} not found in database")
            
        return rad
        
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Error reading radical data: {e}")
        raise

# SQLite functions removed - using SQLAlchemy now

def get_card(card_id):
    conn = getDbConnection()
    card = conn.execute('SELECT * FROM cards WHERE id = ?', (card_id)).fetchone()
    conn.close()
    if card is None:
        abort(404)
    return card
     

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "127.0.0.1")
    
    logger.info(f"Starting Flask app on {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
    
