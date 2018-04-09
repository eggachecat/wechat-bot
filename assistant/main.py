import itchat
from itchat.content import *
import sched, time
from collections import OrderedDict
import prettytable as pt

EVENT_SCHEDULER = sched.scheduler(time.time, time.sleep)


def send_help(*args, **kwargs):
    tb = pt.PrettyTable()
    tb.field_names = ["name", "params"]
    for k, v in FILE_HELPER_EVENTS.items():
        tb.add_row([k, ", ".join(v["alias"])])
    tb.border = 0
    tb.align = 'l'

    itchat.send(tb.__str__(), toUserName="filehelper")
    return None


def send_msg_by_card(msg, state, *args, **kwargs):
    if msg.text == "ABORT":
        return None

    if state is None:
        state = {"staus": "begin", "wait-card": True, "wait-message": True}
    else:

        if msg["Type"] == "Card":
            state["wait-card"] = False
            state["toUserName"] = msg["Text"]["UserName"]
        else:
            state["wait-message"] = False
            state["Message"] = msg.text

    if (not state["wait-message"]) and (not state["wait-card"]):
        def call():
            print("call me!")
            itchat.send(state["Message"], toUserName=state["toUserName"])
        EVENT_SCHEDULER.enter(5, 1, call)
        EVENT_SCHEDULER.run()
        return None

    print(state)
    return state


def set_timing(cls, *args, **kwargs):
    pass


FILE_HELPER_EVENTS = OrderedDict({
    "send-help": {
        "alias": ["帮助", "-1", "h"],
        "func": send_help
    },
    "set-timing": {
        "alias": ["定时", "0", "t"],
        "func": set_timing
    },
    "chat-by-card": {
        "alias": ["名片发送", "2", "cc"],
        "func": send_msg_by_card
    }
})
FILE_HELPER_STATE = None


class middleware_filehelper:
    def __init__(self):
        self.state = None
        self.func = None

    def next(self, msg):
        if self.state is not None:
            self.state = self.func(msg=msg, state=self.state)
        else:
            if msg.ToUserName == "filehelper":
                try:
                    params = msg.text.split(" ")
                    order_type = params[0].lower()
                    for eventName, eventObj in FILE_HELPER_EVENTS.items():
                        if order_type in eventObj["alias"]:
                            self.func = eventObj["func"]
                            self.state = self.func(msg=msg, state=self.state)
                except Exception as e:
                    print(e)
            else:
                pass


mf = middleware_filehelper()


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    mf.next(msg)


itchat.auto_login(True)
itchat.run(True)
