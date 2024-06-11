import pinyin
import requests



uinput = ""
def getPinyin():
        # uinput = input("Input a character to get a pinyin and an image")
        # uinput = "读"
        # pinput = pinyin.get(uinput)
        pinput = "running"
        print(pinput)
def retrieve():
     #url = "https://randomuser.me/api"
     url = "http://ccdb.hemiola.com/characters/string/%E8%AF%BB?fields=kDefinition,kMandarin"
     #url="http://ccdb.hemiola.com/characters"
     print(url)
     response = requests.get(url, headers={"User-Agent": "XY"})
     print("CODE ", response.status_code)
     print(response)
     data = response.json()
     print(data)

   
def main():
    getPinyin()
    retrieve()



if __name__ == "__main__":
    main()

