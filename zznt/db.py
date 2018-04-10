import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime

CRED = credentials.Certificate('./zznt-storage-firebase-adminsdk-8rdbv-60ed195429.json')
DEFAULT_APP = firebase_admin.initialize_app(CRED, {
    "databaseURL": "https://zznt-storage.firebaseio.com/",
    "projectId": 'zznt-storage'
})
DB_REFERENCE = db.reference()
DATABASE_OBJECT = DB_REFERENCE.get()

if DATABASE_OBJECT is None:
    DATABASE_OBJECT = {}


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
