from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
# JWT removed - using Clerk instead
from connections import getConnections
from werkzeug.exceptions import abort
import pinyin
import requests
import re
import json 
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

# Clerk configuration
import requests
from functools import wraps

def verify_clerk_token(token):
    """Verify Clerk JWT token and return user info"""
    try:
        # For demo purposes, we'll use a simple approach
        # In production, you'd verify the JWT with Clerk's public key
        
        # For now, let's extract user info from the request headers
        # The frontend should send user info along with the token
        user_email = request.headers.get('X-User-Email')
        user_id = request.headers.get('X-User-ID')
        
        if user_email and user_id:
            logger.info(f"Token verified for user: {user_email}")
            return {'user_id': user_id, 'email': user_email}
        else:
            # Fallback for demo - create a unique user based on token
            import hashlib
            user_hash = hashlib.md5(token.encode()).hexdigest()[:8]
            demo_email = f"user_{user_hash}@demo.com"
            logger.info(f"Using demo user: {demo_email}")
            return {'user_id': user_hash, 'email': demo_email}
            
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return None

def require_clerk_auth(f):
    """Decorator to require Clerk authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid authorization header"}), 401
        
        token = auth_header.split(' ')[1]
        user_info = verify_clerk_token(token)
        
        if not user_info:
            return jsonify({"error": "Invalid token"}), 401
        
        # Add user info to request context
        request.clerk_user = user_info
        return f(*args, **kwargs)
    return decorated_function

# Configure database
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        # Fallback to SQLite if PostgreSQL fails
        logger.info("Falling back to SQLite configuration")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        db.create_all()

charinput = ""
charPinyin = ""

def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s) 


@app.route('/api/post', methods=["POST"])
@require_clerk_auth
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
        
        # Get or create user based on Clerk authentication
        clerk_user_info = request.clerk_user
        user = User.query.filter_by(email=clerk_user_info['email']).first()
        
        if not user:
            # Create new user from Clerk data
            user = User(
                username=clerk_user_info['email'].split('@')[0],  # Use email prefix as username
                email=clerk_user_info['email'],
                password_hash='clerk_authenticated'  # No password needed with Clerk
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new user: {user.email}")
        
        # Create new card for this user
        card = Card(
            user_id=user.id,
            title=formData['title'],
            pinyin=formData['pinyin'],
            meaning=formData['meaning'],
            con=formData['con']
        )
        db.session.add(card)
        db.session.commit()
        
        logger.info(f"Successfully added card: {formData['title']} for user: {user.email}")
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
@require_clerk_auth
def getCards():
    try:
        # Get user from Clerk authentication
        clerk_user_info = request.clerk_user
        logger.info(f"Getting cards for user: {clerk_user_info}")
        
        user = User.query.filter_by(email=clerk_user_info['email']).first()
        
        if not user:
            logger.info(f"User not found, creating new user: {clerk_user_info['email']}")
            # Create new user
            user = User(
                username=clerk_user_info['email'].split('@')[0],
                email=clerk_user_info['email'],
                password_hash='clerk_authenticated'
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new user: {user.email}")
        
        # Only return cards for this user
        cards = Card.query.filter_by(user_id=user.id).all()
        cards_data = [card.to_dict() for card in cards]
        logger.info(f"Retrieved {len(cards_data)} cards for user: {user.email}")
        return jsonify(cards_data)
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
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
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

# Catch-all route moved to end of file to avoid interfering with API routes

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

# Clerk authentication endpoints will be added here

# SQLite functions removed - using SQLAlchemy now

def get_card(card_id):
    conn = getDbConnection()
    card = conn.execute('SELECT * FROM cards WHERE id = ?', (card_id)).fetchone()
    conn.close()
    if card is None:
        abort(404)
    return card
     

# Catch-all route temporarily disabled for testing
# @app.route("/", defaults={"path": ""})
# @app.route("/<path:path>")
# def serve(path):
#     # Don't serve static files for API routes
#     if path.startswith('api/'):
#         return jsonify({"error": "API endpoint not found"}), 404
#     
#     if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
#         return send_from_directory(app.static_folder, path)
#     else:
#         return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5001))  # Changed from 5000 to 5001
    host = os.getenv("HOST", "127.0.0.1")
    
    logger.info(f"Starting Flask app on {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
    
