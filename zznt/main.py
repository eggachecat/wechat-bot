import itchat
from itchat.content import *
from db import *

from collections import deque
import os

if not os.path.exists("./files/"):
    os.makedirs("./files/")

GLOBAL_USER_QUEUE = []
GLOBAL_MESSAGE_QUEUE = {}

is_at_config = {
    "save-data": {
        "alias": ["保存", "学习", "s", "S"],
        "func": save_data
    },
    "read-data": {
        "alias": ["读取", "复习", "r", "R"],
        "func": read_data
    }
}


def is_at_next(msg):
    aliasMap = dict([(obj["DisplayName"], obj["NickName"]) for obj in msg["User"]["MemberList"]])

    text = msg.text
    atFlag = "\u2005"

    text = text.split(atFlag if atFlag in text else " ", 1)[1]

    response = None

    for eventName, eventObj in is_at_config.items():
        for alias in eventObj["alias"]:
            try:
                idx = text.index(alias)
            except ValueError as e:
                continue
            if idx == 0:
                print("Match alias", alias)

                func = eventObj["func"]
                text = text[len(alias):]
                if eventName == "read-data":
                    name = text.split(atFlag if atFlag in text else " ")[0].replace("@", "").replace(" ", "")
                    if name in aliasMap:
                        response = func(aliasMap[name])
                    else:
                        response = func(name)
                    response = "@{}".format(name) + atFlag + "同志语录:\n" + response
                else:
                    func(GLOBAL_MESSAGE_QUEUE, text, msg)
                return response

    AI = itchat.search_mps('小冰')[0]["UserName"]
    itchat.send(text, AI)
    GLOBAL_USER_QUEUE.append(msg.FromUserName)

    return response


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def GROUP_TEXT_HANDLER(msg):
    print("Receive text message:", msg.text)

    room_id = msg["User"]["EncryChatRoomId"]
    if room_id not in GLOBAL_MESSAGE_QUEUE:
        GLOBAL_MESSAGE_QUEUE[room_id] = deque(maxlen=100)
    GLOBAL_MESSAGE_QUEUE[room_id].append(msg)

    if msg.isAt:
        response = is_at_next(msg)
        if response is not None:
            return response


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def GROUP_FILES_HANDLER(msg):
    room_id = msg["User"]["EncryChatRoomId"]
    if room_id not in GLOBAL_MESSAGE_QUEUE:
        GLOBAL_MESSAGE_QUEUE[room_id] = deque(maxlen=100)
    GLOBAL_MESSAGE_QUEUE[room_id].append(msg)
    fileName = "./files/" + msg.fileName
    msg.download(fileName)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def AI_TEXT_HANDLER(msg):
    AI = itchat.search_mps('小冰')[0]["UserName"]
    if msg.FromUserName == AI:
        user = GLOBAL_USER_QUEUE.pop(0)
        itchat.send(msg.text, user)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
def AI_FILES_HANDLER(msg):
    AI = itchat.search_mps('小冰')[0]["UserName"]
    if msg.FromUserName == AI:
        user = GLOBAL_USER_QUEUE.pop(0)
    fileName = "./files/" + msg.fileName
    msg.download(fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')

    itchat.send('@%s@%s' % (typeSymbol, fileName), toUserName=user)


itchat.auto_login(True)
itchat.run(True)


# text = "\u2005".join(msg.text.split("\u2005")[1:])
#
# if text[:2] == "保存" or text[:2] == "学习":
#     save_data(GLOBAL_MESSAGE_QUEUE, text[2:])
# elif text[0] == "s":
#     save_data(GLOBAL_MESSAGE_QUEUE, text[1:])
# elif text[:2] == "读取" or text[:2] == "复习":
#     if "\u2005" in text[2:]:
#         name = text[2:].split("\u2005")[0].replace("@", "").replace(" ", "")
#         if name in aliasMap:
#             text_ = read_data(aliasMap[name])
#         else:
#             text_ = read_data(name)
#
#         return "@{}\u2005金句 punchlines:\n".format(name) + text_
#     else:
#         return read_data(text[2:])
# elif text[0] == "r":
#     if "\u2005" in text[1:]:
#         name = text[1:].split("\u2005")[0].replace("@", "").replace(" ", "")
#         if name in aliasMap:
#             text_ = read_data(aliasMap[name])
#         else:
#             text_ = read_data(name)
#
#         return "@{}\u2005金句 punchlines:\n".format(name) + text_
#     else:
#         return read_data(text[1:])
