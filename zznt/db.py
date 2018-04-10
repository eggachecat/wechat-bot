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


def search_image(query, max_len=1):
    query = query.rstrip()
    if query[-1].isdigit():
        max_len = int(query[-1])
        query = query[:-1]
    query = filter(lambda x: not x == " ", query.split(" "))
    query = '+'.join(query)
    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"

    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    images = []
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        images.append((link, Type))

    image_names = []
    for i, (link, Type) in enumerate(images):
        if i >= max_len:
            break
        if Type == 'jpg' or Type == 'png' or Type == 'jpeg':
            print(link)
            image_names.append(save_image(link))
    return image_names


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
    except ConnectionError as e:
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
            response += "{} 发表重要讲话: \"{}\"".format(
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
