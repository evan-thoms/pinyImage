import pinyin
import requests


definition = ""
uinput = ""
charPinyin = ""
def getPinyin():
        # 
        pinput = "running"
        print(pinput)
def getCharInfo():
     uinput = input("Input a character to get a pinyin and an image")
     #uinput = "读"
     url = "http://ccdb.hemiola.com/characters/string/"+uinput+"?fields=kDefinition,kMandarin"
     response = requests.get(url, headers={"User-Agent": "XY"})
     definition = response.json()[0]['kDefinition']
     charPinyin = pinyin.get(uinput)
     print("\nYour character", uinput, "is pronounced", charPinyin, "and means", definition, ". ")

   
def main():
    getCharInfo()




if __name__ == "__main__":
    main()

