from flask import Flask, request, render_template


import pinyin
import requests
import re

app = Flask(__name__)

uinput = ""
def contains_chinese_characters(s):
    return re.search(r'[\u4e00-\u9fff]', s)

@app.route("/", methods=["POST", "GET"])
def result():
    #书
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
def getPinyin():
        # 
        pinput = "running"
        print(pinput)
def getCharInfo(uinput):
     #uinput = input("Input a character to get a pinyin and an image")
     #uinput = "读"
     url = "http://ccdb.hemiola.com/characters/string/"+uinput+"?fields=kDefinition,kMandarin"
     response = requests.get(url, headers={"User-Agent": "XY"})
     definition = response.json()[0]['kDefinition']
     charPinyin = pinyin.get(uinput)
     output = "\nYour character "+uinput+ " is pronounced "+charPinyin+" and means "+definition+ ". "
     return output


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
