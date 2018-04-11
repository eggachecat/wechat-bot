from gsearch.googlesearch import search as google_search

import time
import subprocess

MAX_RESULT = 10

import os


def download_page_from_url(url, max_seconds=5):
    proc = subprocess.Popen(
        "python {} \"{}\"".format(os.path.join(os.path.dirname(os.path.realpath(__file__)), "html_to_image.py"), url),
        stdout=subprocess.PIPE)
    ctr = 0
    while ctr < max_seconds:
        time.sleep(1)
        if proc.poll() is None:
            ctr += 1
        else:
            rc = proc.returncode
            if int(rc) == 10:
                return 10
            else:
                return None
    proc.kill()
    return None


MAX_DOWNLOAD_TIME = 10


def search_google(query, callback, only_wiki=False):
    n_search = 1
    query = query.rstrip().lstrip()
    query = query.split(" ")
    if query[-1].isdigit():
        n_search = MAX_RESULT if int(query[-1]) > MAX_RESULT else int(query[-1])
        query = query[:-1]

    query = filter(lambda x: not x == " ", query)

    query = ' '.join(query)
    print("query is", query)
    if only_wiki:
        results = google_search(query + " site:wikipedia.org", num_results=2 * n_search)
        results = list(filter(lambda x: "wikipedia" in x[1], results))[:MAX_RESULT]
    else:
        results = google_search(query, num_results=2 * n_search)

    print(results)
    ctr = 0
    for result in results:
        if ctr >= n_search:
            return

        try:
            url = result[1]
            res = download_page_from_url(url)
            if res is not None:
                callback("./search-output.jpg")
                ctr += 1
            else:
                raise TimeoutError("too looooog to download {}".format(url))

        except Exception as e:
            print(e)
            pass


def search_wiki(query, callback):
    search_google(query, callback, only_wiki=True)


if __name__ == '__main__':
    # print(download_page_from_url("http://www.qq.com/"))
    print(search_google("腾讯", lambda x: 0))
    # print(search_google("日本动画2018 5", lambda x: time.sleep(5)))
