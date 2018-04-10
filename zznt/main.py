import itchat
from itchat.content import *
from db import *

from collections import deque
import os

if not os.path.exists("./files/"):
    os.makedirs("./files/")

GLOBAL_USER_QUEUE = []
GLOBAL_MESSAGE_QUEUE = {}


def print_help(config):
    response = "参考:"
    for k, v in config.items():
        response += "\n"
        response += v["help"].format("/".join(v["alias"]))

    return response


is_at_config = {
    "save-data": {
        "alias": ["保存", "学习", "s", "S"],
        "func": save_data,
        "help": "功能: 保存重要讲话\n使用方法\nat瓦力 {} *数字\n 备注: *数字=[代表前几句]"
    },
    "read-data": {
        "alias": ["读取", "复习", "r", "R"],
        "func": read_data,
        "help": "功能: 复习重要讲话\n使用方法\nat瓦力 {} at用户"
    },
    "search-images": {
        "alias": ["求图", "求图片", "p", "P"],
        "func": search_image,
        "help": "功能: 搜索图片\n使用方法\nat瓦力 {} *关键字 *数字\n: 备注: *关键字=[空格分割的汉字], *数字=[多少张图片,最多20]"
    },
    "wiki": {
        "alias": ["维基", "wiki", "w", "W"],
        "func": search_wiki,
        "help": "功能: 搜索维基百科\n使用方法\nat瓦力 {} *关键字\n: 备注: *关键字=[空格分割的汉字]"
    },
    "help": {
        "alias": ["帮助", "help", "h", "H"],
        "func": print_help,
        "help": "功能: 获得参考\n使用方法\nat瓦力 {}"
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
                    response = "@{}".format(name) + atFlag + "同志语录:" + response
                    return response

                elif eventName == "save-data":
                    func(GLOBAL_MESSAGE_QUEUE, text, msg)
                    return None
                elif eventName == "search-images":
                    func(text, lambda x: itchat.send('@%s@%s' % ("img", x), toUserName=msg.FromUserName))

                    return None
                elif eventName == "wiki":
                    query = text.split(" ")
                    idx = None
                    if query[-1].isdigit():
                        idx = int(query[-1].isdigit() - 1)
                        query = query[:-1]
                    return func(" ".join(query), idx)
                elif eventName == "help":
                    return func(is_at_config)

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
