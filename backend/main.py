from flask import Flask, request, render_template, send_from_directory, jsonify
from connections import getConnections
from werkzeug.exceptions import abort
import pinyin
import requests
import re
import json 
import sqlite3
import os
import sqlite3
import initdb

initdb.init_db()


app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
charinput = ""
charPinyin = ""

def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s) 


@app.route('/api/post', methods=["POST", "GET"])
def addToDb():
     print("addToDb")
     formData = request.get_json()
     print("formdata, ", formData)
     try:
        connection = getDbConnection()
        cur = connection.cursor()
        cur.execute("INSERT INTO cards (title, pinyin, meaning, con) VALUES (?, ?, ?, ?)",
                    (formData['title'], formData['pinyin'], formData['meaning'], formData['con']))
        print(formData['meaning'], "MESDKFLSD")
        connection.commit()
        cards = cur.execute('SELECT * FROM cards').fetchall()
        connection.close()
        return jsonify({"status": "success"}), 200
     except Exception as e:
        print("Error adding to db: ", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/result", methods=["POST", "GET"])
def result():
    print("result function called")
    global charinput, charPinyin
    conn = getDbConnection()
    cards = conn.execute('SELECT * from cards').fetchall()
    conn.close()
    formData= request.get_json()
    if 'user_input' in formData:
        uinput = formData['user_input']
        if contains_chinese_characters(uinput):
                info = getCharInfo(uinput)
                result = "\nYour character "+uinput+ " is pronounced "+info[1]+" and means "+info[2]+ ". "+"\nYour character uses radical #"+info[3]+": "+info[4]+", which means "+info[5]+". "
                connections = getConnections(charinput, charPinyin)
        else:
            result = "The input does not contain any Chinese characters."
            connections = ""
        print(result)
        return jsonify(result=result, meaning = info[2], connections=connections, pinyin=charPinyin, cards=[dict(card) for card in cards])
    return jsonify( result=None,  cards=[dict(card) for card in cards])

@app.route('/api/cards')
def getCards():
    conn = getDbConnection()
    cards = conn.execute('SELECT * from cards').fetchall()
    conn.close()
    return jsonify([dict(card) for card in cards])

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def getCharInfo(uinput):
     global charinput, charPinyin
     charinput=uinput
     print("ran")
     url = "http://ccdb.hemiola.com/characters/string/"+uinput+"?fields=kDefinition,kMandarin,kRSKangXi"
     response = requests.get(url, headers={"User-Agent": "XY"})
     definition = response.json()[0]['kDefinition']
     radNum = response.json()[0]["kRSKangXi"]
     radNum = radNum.split('.')[0]
     charPinyin = pinyin.get(uinput)
     rad = getRads(radNum)
     radChar = rad['radical'].strip()
     english = rad['english']
     radNum = str(radNum)
     char  = "\nYour character "+uinput+ " is pronounced "+charPinyin+" and means "+definition+ ". "
     rad = "\nYour character uses radical #"+radNum+": "+radChar.strip()+", which means "+english+". "
     return uinput, charPinyin, definition, radNum, radChar.strip(), english

def getRads(radNumC):
     print("current number ", radNumC)
     radNumC = int(radNumC)
     with open("radicals.json", "r", encoding="utf-8") as f:
        data = json.load(f)
     rad=None
     for item in data:
        if item['id'] == radNumC:
            rad = item
            break
     print("Found item:", rad)
     return rad
def getDbConnection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
def get_card(card_id):
    conn = getDbConnection()
    card = conn.execute('SELECT * FROM cards WHERE id = ?', (card_id)).fetchone()
    conn.close()
    if card is None:
        abort(404)
    return card
     

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
    
