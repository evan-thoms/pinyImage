from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from connections import getConnections
from werkzeug.exceptions import abort
import pinyin
import requests
import re
import json 
import sqlite3
import os
import initdb
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

initdb.init_db()


app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)  # Enable CORS for all routes

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
                info = getCharInfo(uinput)
                result = f"\nYour character {uinput} is pronounced {info[1]} and means {info[2]}. \nYour character uses radical #{info[3]}: {info[4]}, which means {info[5]}."
                connections = getConnections(charinput, charPinyin, info[2])
                
                return jsonify({
                    "result": result, 
                    "meaning": info[2], 
                    "connections": connections, 
                    "pinyin": charPinyin, 
                    "cards": [dict(card) for card in cards]
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
                        "cards": [dict(card) for card in cards]
                    })
                except Exception as fallback_error:
                    logger.error(f"Fallback also failed: {fallback_error}")
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
        url = f"http://ccdb.hemiola.com/characters/string/{uinput}?fields=kDefinition,kMandarin,kRSKangXi"
        response = requests.get(url, headers={"User-Agent": "XY"}, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            raise ValueError("No character data found")
        
        definition = data[0]['kDefinition']
        radNum = data[0]["kRSKangXi"]
        radNum = radNum.split('.')[0]
        charPinyin = pinyin.get(uinput)
        
        rad = getRads(radNum)
        if not rad:
            raise ValueError("Radical not found")
            
        radChar = rad['radical'].strip()
        english = rad['english']
        radNum = str(radNum)
        
        return uinput, charPinyin, definition, radNum, radChar.strip(), english
        
    except requests.RequestException as e:
        logger.error(f"Network error getting character info: {e}")
        raise
    except (KeyError, IndexError) as e:
        logger.error(f"Data parsing error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting character info: {e}")
        raise

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

def getDbConnection():
    try:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

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
    
