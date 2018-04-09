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
import prettytable as pt


def read_data(name):
    print("name: ", name)
    name = name.replace(" ", "")
    res = DB_REFERENCE.child(name).get()
    if res is None:
        return "Nothing"
    else:
        tb = pt.PrettyTable()
        tb.field_names = ["讲话内容", "发表于"]
        for k, v in res.items():
            tb.add_row([v, k[:10]])
        tb.border = 0
        tb.align = 'l'

        return tb.__str__()


def save_data(message_queue, params):
    messages = []
    for i in params.split(" "):
        if i.isdigit():
            messages.append(message_queue[-1 * (int(i) + 1)])

    for msgObj in messages:

        # print([(obj["DisplayName"], obj["NickName"]) for _, obj in msgObj["User"].items()])

        aliasMap = dict([(obj["DisplayName"], obj["NickName"]) for obj in msgObj["User"]["MemberList"]])
        name = msgObj["ActualNickName"]
        if name in aliasMap:
            name = aliasMap[name]

        time_ = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        if name not in DATABASE_OBJECT:
            DATABASE_OBJECT[name] = {}

        DATABASE_OBJECT[name][time_] = msgObj.text
        DB_REFERENCE.update(DATABASE_OBJECT)


print(read_data("苏脑"))
