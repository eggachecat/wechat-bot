import requests
import _thread
import time

headers = {
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,zh-CN;q=0.6,ja;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "bianke.cnki.net",
    "Origin": "http://bianke.cnki.net",
    "Pragma": "no-cache",
    "Referer": "http://bianke.cnki.net/CollectContest/List/2.html?ct=ZHB02",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

global_ctr = 0

import time


def vote(threadName):
    global global_ctr
    while True:
        try:
            requests.post(
                "http://bianke.cnki.net/api/WebApi/AddVote?jsoncallback=jQuery18206404818998973534_1523460427183",
                headers=headers, data="ContestId=11408")
        except Exception as e:
            continue
        global_ctr += 1
        if global_ctr % 100 == 0:
            print(threadName, global_ctr)


try:
    for i in range(50):
        _thread.start_new_thread(vote, ("Thread-{}".format(i),))

except:
    print("Error: 无法启动线程")

while 1:
    pass
