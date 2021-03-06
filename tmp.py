from bs4 import BeautifulSoup
import requests
import os
import urllib.parse
from os.path import basename
import json

folder = "search"
header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/43.0.2357.134 Safari/537.36"}

if not os.path.exists(folder):
    os.mkdir(folder)


def get_image(query):
    query = query.split()
    query = '+'.join(query)
    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"

    req = requests.get(url, headers=header)
    soup = BeautifulSoup(req.text, 'html.parser')
    images = []
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        images.append((link, Type))
    print(images)
    for i, (link, Type) in enumerate(images):
        if Type == 'jpg':
            save_image(link)


def save_image(url):
    print("start saving")
    try:
        image_r = requests.get(url, headers=header)
        disassembled = urllib.parse.urlparse(url)
        filename = basename(disassembled.path)
        print(url, filename)
        f = open(os.path.join(os.getcwd(), folder, filename), 'wb')
        f.write(image_r.content)
        f.close()
    except ConnectionError as e:
        print('could not download %s' % url)


import wikipedia
from hanziconv import HanziConv


def search_wiki(keyword, idx=None):
    if idx is None:
        try:
            wikipedia.set_lang("zh")
            content = HanziConv.toSimplified(wikipedia.summary(keyword))
        except:
            try:
                wikipedia.set_lang("en")
                content = HanziConv.toSimplified(wikipedia.summary(keyword))
            except:
                return wikipedia.search(keyword)
        return content

    else:
        keyword_ = wikipedia.search(keyword)[idx]
        try:
            wikipedia.set_lang("zh")
            content = HanziConv.toSimplified(wikipedia.summary(keyword_))
        except:
            try:
                wikipedia.set_lang("en")
                content = HanziConv.toSimplified(wikipedia.summary(keyword_))
            except:
                return None
        return content


import json
import time


def convert_result_to_string(result, t_id=0):
    if result is None:
        return "等待发车"

    if "error" in result:
        if result["error"] == "-2":
            return "等待发车"
        else:
            return None

    if "time" not in result:
        return "等待发车"

    if "distance" in result:
        if result["distance"] == "-":
            return "等待发车"

    template_str = "牌照[{}], 还有[{}]站进站, 距离[{}]米, 预计[{}]到达."
    result = template_str.format(result["@attributes"]["cod"], result["terminal"],
                                 result["stopdis"], result["distance"],
                                 time.strftime("%H{H}%M{M}%S{S}",
                                               time.gmtime(int(result["time"]))).format(H="时", M="分", S="秒"))
    if t_id == 0:
        result = "最近一辆[{}]: ".format(["@attributes"]["cod"]) + result

    return result


from bs4 import BeautifulSoup

BUS_HEADERS = {
    "host": "shanghaicity.openservice.kankanews.com",
    "Connection": "keep-alive",
    "Origin": "http://shanghaicity.openservice.kankanews.com",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255",
    "Referer": "http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/41d12e5c3dbbeae16f7f6c1f19f813e0",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "Hm_1vt_6f69830ae7173059e935b61372431b35=eSgsNFrM3iJZtQehEqC/Ag==; Hm_p1vt_6f69830ae7173059e935b61372431b35=eSgsNFrM8DFZbQefEzfEAg==; _gat=1; HH=37e5a34524966caeed267faaf9cb6b9b3df271b0; HK=1930a7f9970cfd304bb7efb2ea27996bc33cfd42; HG=cb379b613181d6e70c5e7be3204883755ef4dbbe; HA=4fa5ee076bed260fa5d3f4a29ce94f495c31b228; HB=NGZhNWVlMDc2YmVkMjYwZmE1ZDNmNGEyOWNlOTRmNDk1YzMxYjIyOA==; HC=6372010139c977b8c6a19510c47539969a9b14a4; HD=MjAxODA0MTE=; HY=MjAxODA0MTE=1930a7f9970cfd304bb7efb2ea27996bc33cfd42cb379b613181d6e70c5e7be3204883755ef4dbbeb9df7e461971221502fafb14768f0390fd670e84; HO=TWpBeE9EQTBNVEU9MDFNamN5TkRZPTIyVFc5NmFXeHNZUzgxTGpBZ0tFeHBiblY0T3lCQmJtUnliMmxrSURndU1Ec2dRVk5WVTE5YU1ERTNSRUVnUW5WcGJHUXZUMUJTTVM0eE56QTJNak11TURJMk95QjNkaWtnUVhCd2JHVlhaV0pMYVhRdk5UTTNMak0ySUNoTFNGUk5UQ3dnYkdsclpTQkhaV05yYnlrZ1ZtVnljMmx2Ymk4MExqQWdRMmh5YjIxbEx6VTNMakF1TWprNE55NHhNeklnVFZGUlFuSnZkM05sY2k4MkxqSWdWRUpUTHpBME16a3dOaUJOYjJKcGJHVWdVMkZtWVhKcEx6VXpOeTR6TmlCTmFXTnliMDFsYzNObGJtZGxjaTgyTGpZdU15NHhNalF3S0RCNE1qWXdOakF6TXprcElFNWxkRlI1Y0dVdk5FY2dUR0Z1WjNWaFoyVXZlbWhmUTA0PWI5ZGY3ZTQ2MTk3MTIyMTUwMmZhZmIxNDc2OGYwMzkwZmQ2NzBlODQ=; Hm_lvt_6f69830ae7173059e935b61372431b35=1523375681; Hm_lpvt_6f69830ae7173059e935b61372431b35=1523381378; _ga=GA1.2.1606788422.1523375681"
}


def request_time(stoptype, stopid, sid):
    r = requests.post("http://shanghaicity.openservice.kankanews.com/public/bus/Getstop",
                      data="stoptype={}&stopid={}&sid={}".format(stoptype, stopid, sid), headers=BUS_HEADERS)
    print("stoptype={}&stopid={}&sid={}".format(stoptype, stopid, sid))
    result = eval(r.text)
    if isinstance(result, dict):
        print(convert_result_to_string(result))
    else:
        print(convert_result_to_string(result[0]))


def request_stops(bud_id, direction=0):
    bus_id_request = requests.post("http://shanghaicity.openservice.kankanews.com/public/bus/get", data={
        "idnum": bud_id
    }, headers=BUS_HEADERS)
    result = eval(bus_id_request.text)
    sid = result["sid"]

    if direction == 0:
        stops_request = requests.get(
            "http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/{}".format(result["sid"]))
    else:
        stops_request = requests.get(
            "http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/{}/stoptype/1".format(result["sid"]))

    html = stops_request.text.encode('latin-1').decode('utf8', 'ignore')

    soup = BeautifulSoup(html, "html.parser")
    stationBox = soup.find("div", attrs={"class": "stationBox"})
    stop_divs = stationBox.find_all("div", attrs={"class": "stationCon"})

    stops_arr = []
    for stop_div in stop_divs:
        name = stop_div.find("span", attrs={"class": "name"}).contents
        num = stop_div.find("span", attrs={"class": "num"}).contents
        stops_arr.append([num[0], name[0]])

    return direction, stops_arr, sid


import editdistance


def request_bus(params):
    params = params.rstrip().lstrip()
    params = params.split(" ")
    print(len(params))
    if len(params) == 1:
        bus_name = params[0]
        print("bus_name", bus_name)
        try:
            response = ""
            direction = 0
            direction, stops_arr, sid = request_stops(bus_name, direction=direction)
            response += "方向[{}]\n".format(direction)
            for stop in stops_arr:
                response += "{} {}\n".format(stop[0], stop[1])
            response += "\n"
            direction = 1
            direction, stops_arr, sid = request_stops(bus_name, direction=direction)
            response += "方向[{}]\n".format(direction)
            for stop in stops_arr:
                response += "{} {}\n".format(stop[0], stop[1])

            return response
        except:
            return "巴士名称错误(要全称啦)"

    if len(params) == 2:
        bus_name = params[0]
        stop_name = params[1]

        response = ""

        def summary(response, direction):
            direction, stops_arr, sid = request_stops(bus_name, direction=direction)
            match_arr = [editdistance.eval(stop_name, stop[0]) for stop in stops_arr]
            match_index = match_arr.index(min(match_arr))
            response += "[{}]: [{}] -> [{}] 方向, 站头[{}], 信息: ".format()
            response += convert_result_to_string(0, stops_arr[match_index][1], sid)
            return response

        response = summary(response, 0)
        response = summary(response, 1)
        return response

    if len(params) == 3:
        bus_name = params[0]
        direction = int(params[1])
        stop_id = params[2] if "." in params[2] else params[2] + "."
        direction, stops_arr, sid = request_stops(bus_name, direction=direction)
        return request_time(direction, stop_id, sid)

    print(params)
    return "巴士参数错误"


from io import StringIO

url = 'https://upload.wikimedia.org/wikipedia/commons/3/3d/LARGE_elevation.jpg'
url = 'https://pbs.twimg.com/profile_images/875749462957670400/T0lwiBK8_400x400.jpg'
image_r = requests.get(url, stream=True)
maxsize = 20000  # 2mb
content = b''
for chunk in image_r.iter_content(2048):
    content += chunk
    print(chunk)
    print(len(chunk))
    if len(content) > maxsize:
        image_r.close()
        raise ValueError('Response too large')
print(len(content))
disassembled = urllib.parse.urlparse(url)
filename = basename(disassembled.path)
filename = os.path.join(os.getcwd(), folder, filename)
f = open(filename, 'wb')
f.write(content)
f.close()
print(filename)
exit()
if __name__ == '__main__':
    request_bus("85 居家桥")

    direction, stops_arr, sid = request_stops("301路", direction=0)
    direction, stops_arr, sid = request_stops("301路", direction=1)
    print(request_time(direction, "23.", sid))

    # request_time()
    exit()
    print(search_wiki("围棋"))
    exit()
    query = "大胸"
    get_image(query)
