import imgkit
import os
import time


def download_web_to_image(url):
    try:
        imgkit.from_url(url, "./search-output.jpg",
                        options={"width": 800, "quality": 50, "load-error-handling": "skip"})
        print("hello")
        return 1
    except Exception as e:
        print(e)
        return 0


if __name__ == '__main__':
    print(os.sys.argv[1])
    if 1 == download_web_to_image(os.sys.argv[1]):
        exit(10)
    else:
        exit(5)
