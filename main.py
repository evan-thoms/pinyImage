import pinyin
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from requests_html import HTMLSession
from selenium.webdriver.common.by import By
session = HTMLSession()

PYPPETEER_CHROMIUM_REVISION = '1263111'

uinput = ""
def getPinyin():
        uinput = input("Input a character to get a pinyin and an image")
        uinput = "读"
        pinput = pinyin.get(uinput)
        print(pinput)
def scrape():
     url = "https://www.tofulearn.com/dictionary/chinese/"+uinput
     url = "https://www.tofulearn.com/dictionary/chinese/%/E8%AF%BB"
     url = "https://www.tofulearn.com/dictionary/chinese/Front"
     driver =webdriver.Chrome()
     driver.get(url)
     print(driver.title)
     defs = driver.find_element(by=By.CLASS_NAME, value='style-scope tofu-chunk107')
     print("dfsdf, ",defs, " dfs")
    #  driver.quit()
    

    #  page = session.get(url)
    #  page.html.render()
    #  #print(page.text)
    #  print(page.html)
    #  print(page.html.html)
    # #  soup = BeautifulSoup(page.content, 'html.parser')
    # #  print(soup.prettify())
    #  definition = soup.find_all("div")
    #  print(definition)
        
# def scrape():
#     url = "https://www.tofulearn.com/dictionary/chinese/%E8%AF%BB"
#     page = urlopen(url)
#     print(page)
#     html_bytes = page.read()
#     html = html_bytes.decode("utf-8")
#     print(html)
#     start_index = html.find("<title>") + len("<title>")
#     end_index = html.find("</title>")
#     title = html[start_index:end_index]
#     print(title)

def main():
    getPinyin()
    scrape()



if __name__ == "__main__":
    main()

