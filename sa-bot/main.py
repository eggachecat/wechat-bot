from datetime import datetime
import json
import sched
import time

import itchat

GLOBAL_scheduler = sched.scheduler(time.time, time.sleep)

with open("./config.json", "r", encoding='UTF-8') as fp:
    CONFIG = json.load(fp)
    PREFIX = CONFIG["prefix"]

    CHAT_ROOM_NAME = CONFIG["chat-room-name"]
    MESSAGE = CONFIG["message"]
    CLOCK = datetime.strptime(CONFIG["clock"], "%Y-%m-%d %H:%M:%S")


def login_callback():
    global CLASS_SIX_ROOM

    for member in itchat.get_chatrooms():
        if PREFIX in member['NickName']:
            CLASS_SIX_ROOM = member["UserName"]

    def call():
        print("Sending to [%s] message:[%s] at: %s" % (CLASS_SIX_ROOM, MESSAGE, datetime.now()))
        if MESSAGE != "":
            itchat.send(msg=MESSAGE, toUserName=CLASS_SIX_ROOM)
        itchat.set_chatroom_name(CLASS_SIX_ROOM, CHAT_ROOM_NAME)

    now = datetime.now()
    delay = (CLOCK - now).total_seconds()
    print("delay in {} seconds".format(delay))
    GLOBAL_scheduler.enter(delay, 1, call)
    GLOBAL_scheduler.run()


if __name__ == '__main__':
    itchat.auto_login(loginCallback=login_callback, hotReload=True, enableCmdQR=2)
    itchat.run(True)
