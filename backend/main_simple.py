from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from connections import getConnections
import pinyin
import requests
import re
import json 
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import sqlite3

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)  # Enable CORS for all routes

charinput = ""
charPinyin = ""

def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s)

def getDbConnection():
    try:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

# Initialize database
def init_db():
    conn = getDbConnection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            title TEXT NOT NULL,
            pinyin TEXT NOT NULL,
            meaning TEXT NOT NULL,
            con TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

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
        
        connection = getDbConnection()
        cur = connection.cursor()
        cur.execute("INSERT INTO cards (title, pinyin, meaning, con) VALUES (?, ?, ?, ?)",
                    (formData['title'], formData['pinyin'], formData['meaning'], formData['con']))
        connection.commit()
        connection.close()
        
        logger.info(f"Successfully added card: {formData['title']}")
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"Error adding to db: {e}")
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
        conn = getDbConnection()
        cards = conn.execute('SELECT * from cards').fetchall()
        conn.close()
        
        if contains_chinese_characters(uinput):
            try:
                # Use OpenAI for character info
                from openai_service import OpenAIService
                openai_service = OpenAIService()
                
                if openai_service.is_available():
                    char_info = openai_service.get_character_info(uinput)
                    if char_info:
                        charPinyin = char_info['pinyin']
                        meaning = char_info['meaning']
                        result = f"\nYour character {uinput} is pronounced {charPinyin} and means {meaning}."
                        connections = getConnections(uinput, charPinyin, meaning)
                        
                        return jsonify({
                            "result": result, 
                            "meaning": meaning, 
                            "connections": connections, 
                            "pinyin": charPinyin, 
                            "cards": [dict(card) for card in cards]
                        })
                
                # Fallback to basic info
                charPinyin = pinyin.get(uinput)
                connections = getConnections(uinput, charPinyin, "character")
                result = f"\nYour character {uinput} is pronounced {charPinyin}."
                
                return jsonify({
                    "result": result,
                    "meaning": "character",
                    "connections": connections,
                    "pinyin": charPinyin,
                    "cards": [dict(card) for card in cards]
                })
                
            except Exception as e:
                logger.error(f"Error processing character {uinput}: {e}")
                return jsonify({
                    "error": "Unable to process character. Please try again later.",
                    "cards": [dict(card) for card in cards]
                }), 500
        else:
            return jsonify({
                "result": "The input does not contain any Chinese characters.",
                "connections": "",
                "cards": [dict(card) for card in cards]
            })
            
    except Exception as e:
        logger.error(f"Error in result endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/cards')
def getCards():
    try:
        conn = getDbConnection()
        cards = conn.execute('SELECT * from cards').fetchall()
        conn.close()
        return jsonify([dict(card) for card in cards])
    except Exception as e:
        logger.error(f"Error fetching cards: {e}")
        return jsonify({"error": "Unable to fetch cards"}), 500

@app.route('/api/status')
def getStatus():
    """Get system status including AI service availability"""
    try:
        from openai_service import OpenAIService
        
        openai_service = OpenAIService()
        
        return jsonify({
            "ai_services": ["OpenAI"] if openai_service.is_available() else [],
            "ai_available": openai_service.is_available(),
            "database": "sqlite",
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
        conn = getDbConnection()
        conn.execute('SELECT 1')
        conn.close()
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
    
    # Check AI service
    try:
        from openai_service import OpenAIService
        openai_service = OpenAIService()
        ai_status = "healthy" if openai_service.is_available() else "unhealthy"
    except Exception as e:
        logger.error(f"AI service health check failed: {e}")
        ai_status = "unhealthy"
    
    overall_status = "healthy" if all([db_status == "healthy", ai_status == "healthy"]) else "degraded"
    
    return jsonify({
        "status": overall_status,
        "services": {
            "database": db_status,
            "ai_service": ai_status
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

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "127.0.0.1")
    
    logger.info(f"Starting Flask app on {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)
