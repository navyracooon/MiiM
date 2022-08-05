#利用するライブラリ(モジュール)をインポート

import requests
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os

#google画像検索にアクセス
options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
url = "https://www.google.co.jp/imghp?hl=ja"
browser.get(url)


#まずは特定の画像を検索する

kw_search = browser.find_element_by_css_selector("#sbtc > div > div.a4bIc > input")

from selenium.webdriver.common.keys import Keys
actor_name = input("画像検索したいものや人のKWを入力してください！：")

kw_search.send_keys(str(actor_name))
kw_search.send_keys(Keys.ENTER)


#BeautifulSoupで画像検索したページの画像を取得する

cur_url = browser.current_url
res = requests.get(cur_url)
soup = BeautifulSoup(res.text,"html.parser")

img_tags = soup.find_all("img",limit = 100)
img_urls = []

for img_tag in img_tags:
  url_a = img_tag.get("src")
  if url != None:
    img_urls.append(url_a)
    
#取得した画像のデータを保存する


save_dir = "img/meme_samples/"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
a=1
for elem_url in img_urls:
    try:

        r = requests.get(elem_url)
        with open(save_dir + str(actor_name) +str(a)+".jpg","wb") as fp:
            fp.write(r.content)
        a += 1
        sleep(0.1)
    except:
        pass

browser.quit()