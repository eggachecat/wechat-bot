import itchat
from itchat.content import *

from utils import *

import json

import sys

import sched, time
import itchat.utils
import os
from datetime import datetime

file_name = "info.json" if len(sys.argv) == 1 else sys.argv[1]
GLOBAL_scheduler = sched.scheduler(time.time, time.sleep)

with open(file_name, "r", encoding="utf-8") as fp:
    ROBBERY_CONFIG = json.load(fp)

WX_INFO = ROBBERY_CONFIG["info"]
TARGET_MP = None


def login_callback():
    global TARGET_MP
    target_mp_nickname = ROBBERY_CONFIG["mp"]
    for member in itchat.get_mps():
        if member["NickName"] == target_mp_nickname:
            TARGET_MP = member["UserName"]
            break

    def call():
        print("Sending message:[%s] at: %s" % (ROBBERY_CONFIG["message"], datetime.now()))
        itchat.send(msg=ROBBERY_CONFIG["message"], toUserName=TARGET_MP)

    if "clock" in ROBBERY_CONFIG:
        target = datetime.strptime(ROBBERY_CONFIG["clock"], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        delay = (target - now).total_seconds()
        GLOBAL_scheduler.enter(delay, 1, call)
        GLOBAL_scheduler.enter(delay + 1, 1, call)
        print("Will send msg in %s and %s seconds" % (delay, delay + 1))
        GLOBAL_scheduler.run()
    else:
        call()

    itchat.utils.clear_screen()
    if os.path.exists("./QR.png"):
        os.remove("./QR.png")


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isMpChat=True)
def text_reply(msg):
    res = replace_example(msg.text, WX_INFO["id"], WX_INFO["phone"], WX_INFO["size"])
    if res is not None:
        print("Legal message!")
        msg.user.send('%s' % res)


if __name__ == '__main__':
    itchat.auto_login(True, loginCallback=login_callback)
    itchat.run(True)
