import itchat
from itchat.content import *
from db import *
# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     if msg.isAt:
#         res = entrance(msg.text.split("\u2005")[1].split(" "))
#         if res is None:
#             return
#         else:
#             return res
#
#         itchat.send()
#
# @itchat.msg_register(TEXT, isMpChat=True)
# def simple_reply(msg):
#     AI = itchat.search_mps('小冰')[0]["UserName"]
#     itchat.send(msg.text, AI)
#     print(msg)
#     print('I received: %s' % msg.text)
from collections import deque

GLOBAL_USER_QUEUE = []
GLOBAL_MESSAGE_QUEUE = deque(maxlen=100)


# @itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
# def text_reply(msg):
#     GLOBAL_MESSAGE_QUEUE.append(msg)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isGroupChat=True)
def text_reply(msg):
    GLOBAL_MESSAGE_QUEUE.append(msg)
    text = msg.text
    print(text, msg.isAt)

    aliasMap = dict([(obj["DisplayName"], obj["NickName"]) for obj in msg["User"]["MemberList"]])
    print(aliasMap)

    if msg.isAt:
        print("raw", text)
        text = "\u2005".join(msg.text.split("\u2005")[1:])
        print("text", text)

        if text[:2] == "保存" or text[:2] == "学习":
            save_data(GLOBAL_MESSAGE_QUEUE, text[2:])
        elif text[0] == "s":
            save_data(GLOBAL_MESSAGE_QUEUE, text[1:])
        elif text[:2] == "读取" or text[:2] == "复习":
            if "\u2005" in text[2:]:
                name = text[2:].split("\u2005")[0].replace("@", "").replace(" ", "")
                if name in aliasMap:
                    text_ = read_data(aliasMap[name])
                else:
                    text_ = read_data(name)

                return "@{}\u2005金句 punchlines:\n".format(name) + text_
            else:
                return read_data(text[2:])
        elif text[0] == "r":
            if "\u2005" in text[1:]:
                name = text[1:].split("\u2005")[0].replace("@", "").replace(" ", "")
                if name in aliasMap:
                    text_ = read_data(aliasMap[name])
                else:
                    text_ = read_data(name)

                return "@{}\u2005金句 punchlines:\n".format(name) + text_
            else:
                return read_data(text[1:])
        else:
            AI = itchat.search_mps('小冰')[0]["UserName"]
            _ = itchat.send(text, AI)
            GLOBAL_USER_QUEUE.append(msg.FromUserName)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    print(msg)
    AI = itchat.search_mps('小冰')[0]["UserName"]
    if msg.FromUserName == AI:
        user = GLOBAL_USER_QUEUE.pop(0)
        _ = itchat.send(msg.text, user)
        print(_)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')

    return '@%s@%s' % (typeSymbol, msg.fileName)


itchat.auto_login(True)
itchat.run(True)
