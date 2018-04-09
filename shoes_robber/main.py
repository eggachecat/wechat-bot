import itchat
from itchat.content import *

from shoes_robber.utils import *

WX_INFO = {
    "phone": "15900749626",
    "id": "310210199406150010",
    "size": "D"
}





@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    msg.user.send('%s' % (replace_example(msg.text, WX_INFO["id"], WX_INFO["phone"])))
    msg.user.send('%s: %s' % (msg.type, replace_example(msg.text, WX_INFO["id"], WX_INFO["phone"])))


# @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
# def download_files(msg):
#     msg.download(msg.fileName)
#     typeSymbol = {
#         PICTURE: 'img',
#         VIDEO: 'vid', }.get(msg.type, 'fil')
#     return '@%s@%s' % (typeSymbol, msg.fileName)
#
#
# @itchat.msg_register(FRIENDS)
# def add_friend(msg):
#     msg.user.verify()
#     msg.user.send('Nice to meet you!')
#
#
# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     if msg.isAt:
#         msg.user.send(u'@%s\u2005I received: %s' % (
#             msg.actualNickName, msg.text))


if __name__ == '__main__':
    itchat.auto_login(True)
    itchat.run(True)
