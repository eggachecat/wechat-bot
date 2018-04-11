import asyncio
import aiohttp
import argparse
import os
import requests

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

url = "http://bianke.cnki.net/api/WebApi/AddVote?jsoncallback=jQuery18206404818998973534_1523460427183"


def vote_():
    r = requests.post(
        "http://bianke.cnki.net/api/WebApi/AddVote?jsoncallback=jQuery18206404818998973534_1523460427183",
        headers=headers, data="ContestId=11408")
    print(r.text)


vote_()


async def vote():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data="ContestId=11408", headers=headers) as response:
            pass


futures = []
for _ in range(200):
    futures.append(vote())
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
vote_()
