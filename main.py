from flask import Flask, request, render_template


import pinyin
import requests
import re
import json

app = Flask(__name__)

uinput = ""
def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s) 

@app.route("/", methods=["POST", "GET"])
def result():
    form_data= request.form.to_dict()
    if 'user_input' in form_data:
        uinput = request.form.to_dict()['user_input']
        if contains_chinese_characters(uinput):
                result = getCharInfo(uinput)
        else:
            result = "The input does not contain any Chinese characters."
        print(result)
        return render_template('home.html', result = result)
    return render_template("home.html", result=None )


def testreturn(uinput):
     return uinput

definition = ""

charPinyin = ""
def getCharInfo(uinput):
     #uinput = input("Input a character to get a pinyin and an image")
    #  uinput = "读"
     url = "http://ccdb.hemiola.com/characters/string/"+uinput+"?fields=kDefinition,kMandarin,kRSKangXi"
     response = requests.get(url, headers={"User-Agent": "XY"})
     definition = response.json()[0]['kDefinition']
     radNum = response.json()[0]["kRSKangXi"]
     print(response.json()[0])
     print(response.json()[0], " response")
     print("originial rad ", radNum)
     radNum = radNum.split('.')[0]
     print(radNum, "sdf")
     charPinyin = pinyin.get(uinput)
     rad = getRads(radNum)
     print(rad)
     radChar = rad['radical']
     english = rad['english']
     radNum = str(radNum)
     char  = "\nYour character "+uinput+ " is pronounced "+charPinyin+" and means "+definition+ ". "
     rad = "\nYour character uses radical #"+radNum+": "+radChar+", which means "+english+". "
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
     

     


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    # getCharInfo(3)
