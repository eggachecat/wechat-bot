from gsearch.googlesearch import search as google_search

import time
import subprocess

MAX_RESULT = 10

import os


def download_page_from_url(url, max_seconds=5):
    args = " ".join(
        ["python", "-u", "{}".format(os.path.join(os.path.dirname(os.path.realpath(__file__)), "html_to_image.py")),
         "\"{}\"".format(url)])
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)

    ctr = 0
    while ctr < max_seconds:
        time.sleep(1)

        if proc.poll() is None:
            ctr += 1
            data = proc.stdout.read()  # Note: it reads as binary, not text
            print(data)
        else:
            rc = proc.returncode
            print("rc code:", rc)
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
        results = google_search(query + " site:wikipedia.org", num_results=MAX_RESULT)
        results = list(filter(lambda x: "wikipedia" in x[1], results))[:MAX_RESULT]
    else:
        results = google_search(query, num_results=MAX_RESULT)

    print(results)
    ctr = 0
    for result in results:
        if ctr >= n_search:
            return

        try:
            url = result[1]
            print("downloading... {}".format(url))
            res = download_page_from_url(url)
            print("res is", res)
            if res is not None:
                callback("./search-output.jpg")
                ctr += 1
            else:
                raise TimeoutError("too looooog to download {}".format(url))

        except Exception as e:
            print(e)
            exit()
            pass


import requests
import json
import urllib.parse
import wikitextparser as wtp
import wikipediaapi


def structure_sections(sections, structure, level=0):
    structure[str(level)] = {}
    for i, s in enumerate(sections):
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))

        structure[str(level)][str(i + 1)] = {
            "title": s.title,
            "text": s.text
        }
        structure_sections(s.sections, structure[str(level)][str(i + 1)], level + 1)


def get_index(structure, prelevel=None):
    if isinstance(structure, str):
        return ""

    index_doc = ""
    for level in structure:
        print(level, structure)

        if "title" in structure[level]:
            if structure[level]["text"] == "":
                pass
            else:
                if prelevel is None:
                    index_doc += "{}:{}\n".format(level, structure[level]["title"])
                else:
                    index_doc += "{}.{}:{}\n".format(prelevel, level, structure[level]["title"])
        if prelevel is None:
            index_doc += get_index(structure[level], "{}".format(level))
        else:
            index_doc += get_index(structure[level], "{}.{}".format(prelevel, level))

    return index_doc


def search_wiki(query, callback, ids=None):
    n_search = 1
    query = query.rstrip().lstrip()
    query = query.split(" ")
    if query[-1].isdigit():
        n_search = MAX_RESULT if int(query[-1]) > MAX_RESULT else int(query[-1])
        query = query[:-1]

    query = filter(lambda x: not x == " ", query)

    query = ' '.join(query)
    print("query is", query)
    results = google_search(query + " site:wikipedia.org", num_results=MAX_RESULT)
    results = list(filter(lambda x: "wikipedia" in x[1], results))[:MAX_RESULT]
    print(results)
    prefix = ""
    suffix = ""
    ctr = 0
    for result in results:
        if ctr >= n_search:
            return
        url_parts = result[1].split("/")
        lang = url_parts[2].split(".")[0]
        print(lang, url_parts[-1], urllib.parse.unquote(url_parts[-1]))

        wiki_wiki = wikipediaapi.Wikipedia(lang)
        page = wiki_wiki.page(urllib.parse.unquote(url_parts[-1]))
        structure = {}
        index = {"content": ""}
        structure_sections(page.sections, structure)
        structure = structure["0"]
        print(get_index(structure))
        print(index)
        exit()
        print("Page - Exists: %s" % page.exists())

        print("Page - Summary: %s" % page.summary)
        exit()
        # url = "http://{}//w/api.php?action=query&prop=revisions&rvprop=content&format=json&&titles={}".format(
        #     url_parts[2], url_parts[-1])
        # r = requests.get(url)
        # result = json.loads(r.text)
        # pages = result["query"]["pages"]
        # page_id = list(pages.keys())[0]
        # content = pages[page_id]["revisions"][0]["*"]
        # parsed = wtp.parse(content)
        # print_sections(parsed.sections)

        # for section in parsed.sections:
        #     print(section.title)
        #     print("------------------")
        #     print(section.contents)
        #     print("===================")
        # print([])


def modify_dict(d):
    d += "a"


if __name__ == '__main__':
    # a = "b"
    # modify_dict(a)
    # print(a)
    # exit()
    # print(download_page_from_url("http://www.qq.com/"))
    print(search_wiki("腾讯", lambda x: 0))
    # print(search_google("日本动画2018 5", lambda x: time.sleep(5)))
