import imgkit
from gsearch.googlesearch import search as google_search

MAX_RESULT = 5
import time
import os


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
            imgkit.from_url(result[1], "./search-output.jpg")
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
    print(query)
    results = google_search(query, num_results=max_research)
    for result in results:
        try:
            imgkit.from_url(result[1], "./search-output.jpg")
            callback("./search-output.jpg")
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    print(search_google("日本动画2018", lambda x: time.sleep(5)))
    # print(search_google("日本动画2018 5", lambda x: time.sleep(5)))
