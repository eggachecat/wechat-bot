import editdistance
import json
import time
import requests
from bs4 import BeautifulSoup
import os

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

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bus.json"), "r", encoding="utf-8") as fp:
    BUS_ALL_BUS_NAMES = json.load(fp)["ALL_BUS_NAMES"]


def match_bus_name(bus_name, return_index=False):
    ed_arr = [editdistance.eval(bus_name, name) for name in BUS_ALL_BUS_NAMES]
    min_index = ed_arr.index(min(ed_arr))
    if return_index:
        return min_index
    return BUS_ALL_BUS_NAMES[min_index]


def match_stop_name(stop_name, stops_arr, return_index=False):
    ed_arr = []
    for i, stop in enumerate(stops_arr):
        ed_arr.append(editdistance.eval(stop_name, stop[1]))
        if stop_name in stop[1]:
            if return_index:
                return i

    min_index = ed_arr.index(min(ed_arr))
    if return_index:
        return min_index
    return stops_arr[min_index]


def convert_result_to_string(result, keep_bus_name=False):
    print(result)
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

    template_str = "还有[{sd}]站进站. 距离车站[{d}]米, 预计[{tm}]进站. 牌照[{t}]."

    result = template_str.format(t=result["terminal"], sd=result["stopdis"], d=result["distance"],
                                 tm=time.strftime("%H{H}%M{M}%S{S}",
                                                  time.gmtime(int(result["time"]))).format(H="时", M="分", S="秒"))
    if keep_bus_name:
        result = "最近一辆[{}]: ".format(["@attributes"]["cod"]) + result

    return result


def request_time(stoptype, stopid, sid):
    r = requests.post("http://shanghaicity.openservice.kankanews.com/public/bus/Getstop",
                      data="stoptype={}&stopid={}&sid={}".format(stoptype, stopid, sid), headers=BUS_HEADERS)
    result = eval(r.text)
    if isinstance(result, dict):
        return convert_result_to_string(result)
    else:
        return convert_result_to_string(result[0])


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


def request_bus(params):
    params = params.rstrip().lstrip()
    params = params.split(" ")
    bus_name = match_bus_name(params[0])
    print("Match bus name: {}".format(bus_name))

    if len(params) == 1:

        def _request_full_table(bus_name_, response_, direction_):
            direction_, stops_arr_, sid_ = request_stops(bus_name_, direction=direction_)
            response_ += "方向[{}]\n".format(direction_)
            for stop_ in stops_arr_:
                response_ += "{} {}\n".format(stop_[0], stop_[1])
            return response_

        try:
            response = ""
            response = _request_full_table(bus_name, response, 0)
            response += "\n"
            response = _request_full_table(bus_name, response, 1)
            return response
        except Exception as e:
            print(e)
            return "巴士名称错误(要全称啦)"

    if len(params) == 2:
        stop_name = params[1]

        response = ""

        def summary(bus_name_, stop_name_, response_, direction_):
            direction_, stops_arr_, sid_ = request_stops(bus_name_, direction=direction_)
            min_index_ = match_stop_name(stop_name_, stops_arr_, return_index=True)
            stop_id__, stop_name__ = stops_arr_[min_index_][0], stops_arr_[min_index_][1]
            print("Match bus name: {}".format(stop_name__))

            start_stop = stops_arr_[0][1]
            terminal_stop = stops_arr_[-1][1]
            response_ += "[{b}], 方向[{o} -> {t}]\n[{s}]站信息: \n".format(b=bus_name, o=start_stop, t=terminal_stop,
                                                                   s=stop_name__)
            response_ += request_time(direction_, stop_id__, sid_)
            return response_ + "\n"

        response = summary(bus_name, stop_name, response, 0)
        response += "\n"
        response = summary(bus_name, stop_name, response, 1)
        return response

    if len(params) == 3:
        stop_id = params[1] if "." in params[1] else params[1] + "."
        direction = int(params[2])

        direction, stops_arr, sid = request_stops(bus_name, direction=direction)
        return request_time(direction, stop_id, sid)

    return "巴士参数错误"


if __name__ == '__main__':
    print(request_bus("85路 17. 0"))
    print(request_bus("85路 居家桥"))
    print(request_bus("85 居家桥"))
