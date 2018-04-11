import imgkit
from gsearch.googlesearch import search as google_search

MAX_RESULT = 5
import time
import os
from imgkit.config import Config as iConfig

CONFIG = iConfig()


def search_wiki(query, callback):
    max_research = 1
    query = query.rstrip().lstrip()
    query = query.split(" ")
    if query[-1].isdigit():
        max_research = MAX_RESULT if int(query[-1]) > MAX_RESULT else int(query[-1])
        query = query[:-1]

    query = filter(lambda x: not x == " ", query)

    query = ' '.join(query)

    results = google_search(query + " site:wikipedia.org", num_results=max_research)
    results = list(filter(lambda x: "wikipedia" in x[1], results))[:MAX_RESULT]
    for result in results:
        try:
            url = result[1]
            url = url.replace(".wikipedia", ".m.wikipedia")
            imgkit.from_url(url, "./search-output.jpg", options={"width": 400, "quality": 50})
            callback("./search-output.jpg")
        except Exception as e:
            print(e)
            pass


def search_google(query, callback):
    max_research = 1
    query = query.rstrip().lstrip()
    query = query.split(" ")
    if query[-1].isdigit():
        max_research = MAX_RESULT if int(query[-1]) > MAX_RESULT else int(query[-1])
        query = query[:-1]

    query = filter(lambda x: not x == " ", query)

    query = ' '.join(query)
    print("query is", query)
    results = google_search(query, num_results=max_research)
    for result in results:
        try:
            print(result[1])
            imgkit.from_url(result[1], "./search-output.jpg", options={'format': 'png'})
            callback("./search-output.jpg")
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    print(search_wiki("尤文图斯", lambda x: 0))
    # print(search_google("日本动画2018 5", lambda x: time.sleep(5)))
