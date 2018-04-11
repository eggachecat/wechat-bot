import imgkit
import os
import time


def download_web_to_image(url):
    imgkit.from_url(url, "./search-output.jpg", options={"width": 800, "quality": 50})
    exit(10)


if __name__ == '__main__':
    download_web_to_image(os.sys.argv[1])
