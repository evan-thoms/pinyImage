from flask import Flask, request, render_template
from connections import getConnections

import pinyin
import requests
import re
import json 
import sqlite3

app = Flask(__name__, static_folder='static')

charinput = ""
charPinyin = ""

def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s) 

@app.route("/", methods=["POST", "GET"])
def result():
    global charinput, charPinyin
    conn = getDbConnection()
    cards = conn.execute('SELECT * from cards').fetchall()
    conn.close()
    form_data= request.form.to_dict()
    if 'user_input' in form_data:
        uinput = request.form.to_dict()['user_input']
        if contains_chinese_characters(uinput):
                result = getCharInfo(uinput)
                connections = getConnections(charinput, charPinyin)
        else:
            result = "The input does not contain any Chinese characters."
            connections = ""
        print(result)
        return render_template('home.html', result = result, connections=connections, cards=cards)
    return render_template("home.html", result=None,  cards=cards)

def getCharInfo(uinput):
     global charinput, charPinyin
     charinput=uinput
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
     return char + rad
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
    
    # Debugging output to verify the correct item was found
     print("Found item:", rad)
     return rad
def getDbConnection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn
     

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    
