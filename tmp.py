from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
from os.path import basename
import json

folder = "search"
header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/43.0.2357.134 Safari/537.36"}

if not os.path.exists(folder):
    os.mkdir(folder)


def get_image(query):
    query = query.split()
    query = '+'.join(query)
    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"

    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    images = []
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        images.append((link, Type))
    print(images)
    for i, (link, Type) in enumerate(images):
        if Type == 'jpg':
            save_image(link)


def save_image(url):
    print("start saving")
    try:
        image_r = requests.get(url, headers=header)
        disassembled = urllib.parse.urlparse(url)
        filename = basename(disassembled.path)
        print(url, filename)
        f = open(os.path.join(os.getcwd(), folder, filename), 'wb')
        f.write(image_r.content)
        f.close()
    except ConnectionError as e:
        print('could not download %s' % url)


if __name__ == '__main__':
    query = "大胸"
    get_image(query)
