import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
from os.path import basename
import json

CRED = credentials.Certificate('./zznt-storage-firebase-adminsdk-8rdbv-60ed195429.json')
DEFAULT_APP = firebase_admin.initialize_app(CRED, {
    "databaseURL": "https://zznt-storage.firebaseio.com/",
    "projectId": 'zznt-storage'
})
DB_REFERENCE = db.reference()
DATABASE_OBJECT = DB_REFERENCE.get()

if DATABASE_OBJECT is None:
    DATABASE_OBJECT = {}

folder = "search"
header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/43.0.2357.134 Safari/537.36"}

if not os.path.exists(folder):
    os.mkdir(folder)

MAX_N_IMAGES = 20


def search_image(query, callback):
    max_images = 1
    query = query.rstrip().lstrip()
    query = query.split(" ")
    if query[-1].isdigit():
        max_images = MAX_N_IMAGES if int(query[-1]) > MAX_N_IMAGES else int(query[-1])
        query = query[:-1]
    if max_images == 0:
        max_images = MAX_N_IMAGES
    query = filter(lambda x: not x == " ", query)

    query = '+'.join(query)
    print(query, max_images)

    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"

    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    images = []
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        images.append((link, Type))

    ctr = 0
    for i, (link, Type) in enumerate(images):
        if ctr >= max_images:
            break
        if Type == 'jpg' or Type == 'png':
            fileName = save_image(link)
            if fileName is not None:
                print(fileName)
                callback(fileName)
                ctr += 1


def save_image(url):
    try:
        image_r = requests.get(url, headers=header)
        disassembled = urllib.parse.urlparse(url)
        filename = basename(disassembled.path)
        filename = os.path.join(os.getcwd(), folder, filename)
        f = open(filename, 'wb')
        f.write(image_r.content)
        f.close()
        print(filename)
        return filename
    except Exception as e:
        print('could not download %s' % url)
        return None


def read_data(name):
    name = name.replace(" ", "")
    res = DB_REFERENCE.child(name).get()

    if res is None:
        return "Nothing"
    else:
        print("name: ", name)
        response = ""
        for k, v in res.items():
            response += "\n\n"
            date = datetime.datetime.strptime(k, "%Y-%m-%d %H:%M:%S")
            response += "{} 发表重要讲话: \"{}\";".format(
                date.strftime("%Y{Y}%m{m}%d{d}%H{H}%M{M}%S{S}").format(Y='年', m='月', d='日', H='时', M='分', S='秒'), v)
        return response


def save_data(message_queue, params, msg):
    messages = []
    room_id = msg["User"]["EncryChatRoomId"]
    for i in params.split(" "):
        if i.isdigit():
            msgObj_ = message_queue[room_id][-1 * (int(i) + 1)]
            if msgObj_.Type == "Text":
                messages.append(msgObj_)

    for msgObj in messages:
        print("saving..", msgObj.text)
        aliasMap = dict([(obj["DisplayName"], obj["NickName"]) for obj in msgObj["User"]["MemberList"]])
        name = msgObj["ActualNickName"]
        if name in aliasMap:
            name = aliasMap[name]

        time_ = datetime.datetime.fromtimestamp(msgObj.CreateTime).strftime("%Y-%m-%d %H:%M:%S")
        if name not in DATABASE_OBJECT:
            DATABASE_OBJECT[name] = {}

        DATABASE_OBJECT[name][time_] = msgObj.text
        DB_REFERENCE.update(DATABASE_OBJECT)


import wikipedia
from hanziconv import HanziConv


def search_wiki(keyword, idx=None):
    if idx is None:
        try:
            wikipedia.set_lang("zh")
            content = HanziConv.toSimplified(wikipedia.summary(keyword))
        except:
            try:
                wikipedia.set_lang("en")
                content = HanziConv.toSimplified(wikipedia.summary(keyword))
            except:
                return wikipedia.search(keyword)
        return content

    else:
        keyword_ = wikipedia.search(keyword)[idx]
        try:
            wikipedia.set_lang("zh")
            content = HanziConv.toSimplified(wikipedia.summary(keyword_))
        except:
            try:
                wikipedia.set_lang("en")
                content = HanziConv.toSimplified(wikipedia.summary(keyword_))
            except:
                return None
        return content
