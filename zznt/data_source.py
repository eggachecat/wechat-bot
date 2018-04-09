import requests
import json
import prettytable as pt


def request_football(league, *args, **kwargs):
    print(league, *args)

    payload = {'dtype': 'json', 'league': league, 'key': "f56664adf87b8f37f0b3d132604dcd0f"}
    r = requests.get('http://op.juhe.cn/onebox/football/league', params=payload)
    result = json.loads(r.text)["result"]

    if len(args) > 0:
        if args[0] == "射手" or args[0] == "射手榜":
            tb = pt.PrettyTable()
            tb.field_names = ["player", "goals"]
            for item in result["views"]["sheshoubang"]:
                tb.add_row([item["c2"], item["c4"]])
            tb.border = 0
            tb.align = 'l'

            return tb.__str__()

    else:
        tb = pt.PrettyTable()
        tb.field_names = ["played", "points", "club"]
        for item in result["views"]["jifenbang"]:
            tb.add_row([item["c3"], item["c6"], item["c2"]])
        tb.border = 0
        tb.align = 'l'

        return tb.__str__()


RESERVED_MAP = {
    "football": {
        "func": request_football,
        "params": {
            "league": {
                "英超": "英超",
                "中超": "中超",
                "西甲": "西甲",
                "德甲": "德甲",
                "意甲": "意甲"
            }
        }
    }
}


def entrance(keyword):
    for apiName, api in RESERVED_MAP.items():
        for paramName, param in api["params"].items():
            if keyword[0] in param:
                func = api["func"]
                return func(*keyword)

    return None


from collections import deque

d = deque(maxlen=10)
for _ in range(100):
    d.append(_)
    print(d, d[-1])

# entrance("@瓦力\u2005英超 射手榜".split("\u2005")[1].split(" "))

#
# res = {
#     "key": "英超",
#     "tabs": {
#         "saicheng1": "第33轮赛程",
#         "saicheng2": "第34轮赛程",
#         "jifenbang": "积分榜",
#         "sheshoubang": "射手榜"
#     },
#     "views": {
#         "saicheng1": [
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "19:30",
#                 "c4T1": "埃弗顿",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=73",
#                 "c4R": "0-0",
#                 "c4T2": "利物浦",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=53",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164623",
#                 "c52": "全场战报",
#                 "c52Link": "http://sports.sina.com.cn/g/pl/2018-04-07/doc-ifyvtmxc6047838.shtml?cre=360.ala.yc.sc",
#                 "liveid": "919217"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "22:00",
#                 "c4T1": "伯恩茅斯",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=7146",
#                 "c4R": "2-2",
#                 "c4T2": "水晶宫",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=292",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164620",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164620",
#                 "liveid": "919213"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "22:00",
#                 "c4T1": "布莱顿",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=2285",
#                 "c4R": "1-1",
#                 "c4T2": "哈德斯菲尔德",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=273",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164621",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164621",
#                 "liveid": "919215"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "22:00",
#                 "c4T1": "莱斯特城",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=92",
#                 "c4R": "1-2",
#                 "c4T2": "纽卡斯尔",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=63",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164624",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164624",
#                 "liveid": "919218"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "22:00",
#                 "c4T1": "斯托克城",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=2297",
#                 "c4R": "1-2",
#                 "c4T2": "热刺",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=66",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164626",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164626",
#                 "liveid": "919220"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "22:00",
#                 "c4T1": "沃特福德",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=276",
#                 "c4R": "1-2",
#                 "c4T2": "伯恩利",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=280",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164627",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164627",
#                 "liveid": "919221"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-07周六",
#                 "c3": "22:00",
#                 "c4T1": "西布朗",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=278",
#                 "c4R": "1-1",
#                 "c4T2": "斯旺西",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=7145",
#                 "c51": "全场统计",
#                 "c51Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164628",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164628",
#                 "liveid": "919222"
#             },
#             {
#                 "c1": "已结束",
#                 "c2": "04-08周日",
#                 "c3": "00:30",
#                 "c4T1": "曼城",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=216",
#                 "c4R": "2-3",
#                 "c4T2": "曼联",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=52",
#                 "c51": "视频集锦",
#                 "c51Link": "http://video.sina.com.cn/p/sports/pl/v/doc/2018-04-08/043968147897.html?cre=360.ala.yc.sc",
#                 "c52": "图文数据",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164625",
#                 "liveid": "919219"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-08周日",
#                 "c3": "21:15",
#                 "c4T1": "阿森纳",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=61",
#                 "c4R": "VS",
#                 "c4T2": "南安普敦",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=94",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164619",
#                 "liveid": "919214"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-08周日",
#                 "c3": "23:30",
#                 "c4T1": "切尔西",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=60",
#                 "c4R": "VS",
#                 "c4T2": "西汉姆联",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=98",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164622",
#                 "liveid": "919216"
#             }
#         ],
#         "saicheng2": [
#             {
#                 "c1": "未开赛",
#                 "c2": "04-14周六",
#                 "c3": "19:30",
#                 "c4T1": "南安普敦",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=94",
#                 "c4R": "VS",
#                 "c4T2": "切尔西",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=60",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164635",
#                 "liveid": "919229"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-14周六",
#                 "c3": "22:00",
#                 "c4T1": "伯恩利",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=280",
#                 "c4R": "VS",
#                 "c4T2": "莱斯特城",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=92",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164629",
#                 "liveid": "919223"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-14周六",
#                 "c3": "22:00",
#                 "c4T1": "水晶宫",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=292",
#                 "c4R": "VS",
#                 "c4T2": "布莱顿",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=2285",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164630",
#                 "liveid": "919224"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-14周六",
#                 "c3": "22:00",
#                 "c4T1": "哈德斯菲尔德",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=273",
#                 "c4R": "VS",
#                 "c4T2": "沃特福德",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=276",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164631",
#                 "liveid": "919225"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-14周六",
#                 "c3": "22:00",
#                 "c4T1": "斯旺西",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=7145",
#                 "c4R": "VS",
#                 "c4T2": "埃弗顿",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=73",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164636",
#                 "liveid": "919230"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-15周日",
#                 "c3": "00:30",
#                 "c4T1": "利物浦",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=53",
#                 "c4R": "VS",
#                 "c4T2": "伯恩茅斯",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=7146",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164632",
#                 "liveid": "919226"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-15周日",
#                 "c3": "02:45",
#                 "c4T1": "热刺",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=66",
#                 "c4R": "VS",
#                 "c4T2": "曼城",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=216",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164637",
#                 "liveid": "919231"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-15周日",
#                 "c3": "20:30",
#                 "c4T1": "纽卡斯尔",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=63",
#                 "c4R": "VS",
#                 "c4T2": "阿森纳",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=61",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164634",
#                 "liveid": "919228"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-15周日",
#                 "c3": "23:00",
#                 "c4T1": "曼联",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=52",
#                 "c4R": "VS",
#                 "c4T2": "西布朗",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=278",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164633",
#                 "liveid": "919227"
#             },
#             {
#                 "c1": "未开赛",
#                 "c2": "04-17周二",
#                 "c3": "03:00",
#                 "c4T1": "西汉姆联",
#                 "c4T1URL": "http://match.sports.sina.com.cn/football/team.php?id=98",
#                 "c4R": "VS",
#                 "c4T2": "斯托克城",
#                 "c4T2URL": "http://match.sports.sina.com.cn/football/team.php?id=2297",
#                 "c51": "视频暂无",
#                 "c51Link": "",
#                 "c52": "前瞻预测",
#                 "c52Link": "http://match.sports.sina.com.cn/livecast/g/live.php?id=164638",
#                 "liveid": "919232"
#             }
#         ],
#         "jifenbang": [
#             {
#                 "c1": "1",
#                 "c2": "曼城",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=216",
#                 "c3": "32",
#                 "c41": "27",
#                 "c42": "3",
#                 "c43": "2",
#                 "c5": "66",
#                 "c6": "84"
#             },
#             {
#                 "c1": "2",
#                 "c2": "曼联",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=52",
#                 "c3": "32",
#                 "c41": "22",
#                 "c42": "5",
#                 "c43": "5",
#                 "c5": "38",
#                 "c6": "71"
#             },
#             {
#                 "c1": "3",
#                 "c2": "利物浦",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=53",
#                 "c3": "33",
#                 "c41": "19",
#                 "c42": "10",
#                 "c43": "4",
#                 "c5": "40",
#                 "c6": "67"
#             },
#             {
#                 "c1": "4",
#                 "c2": "热刺",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=66",
#                 "c3": "32",
#                 "c41": "20",
#                 "c42": "7",
#                 "c43": "5",
#                 "c5": "37",
#                 "c6": "67"
#             },
#             {
#                 "c1": "5",
#                 "c2": "切尔西",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=60",
#                 "c3": "31",
#                 "c41": "17",
#                 "c42": "5",
#                 "c43": "9",
#                 "c5": "23",
#                 "c6": "56"
#             },
#             {
#                 "c1": "6",
#                 "c2": "阿森纳",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=61",
#                 "c3": "31",
#                 "c41": "15",
#                 "c42": "6",
#                 "c43": "10",
#                 "c5": "17",
#                 "c6": "51"
#             },
#             {
#                 "c1": "7",
#                 "c2": "伯恩利",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=280",
#                 "c3": "32",
#                 "c41": "13",
#                 "c42": "10",
#                 "c43": "9",
#                 "c5": "3",
#                 "c6": "49"
#             },
#             {
#                 "c1": "8",
#                 "c2": "莱斯特城",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=92",
#                 "c3": "32",
#                 "c41": "11",
#                 "c42": "10",
#                 "c43": "11",
#                 "c5": "3",
#                 "c6": "43"
#             },
#             {
#                 "c1": "9",
#                 "c2": "埃弗顿",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=73",
#                 "c3": "33",
#                 "c41": "11",
#                 "c42": "8",
#                 "c43": "14",
#                 "c5": "-15",
#                 "c6": "41"
#             },
#             {
#                 "c1": "10",
#                 "c2": "纽卡斯尔",
#                 "c2L": "http://match.sports.sina.com.cn/football/team.php?id=63",
#                 "c3": "32",
#                 "c41": "10",
#                 "c42": "8",
#                 "c43": "14",
#                 "c5": "-8",
#                 "c6": "38"
#             }
#         ],
#         "sheshoubang": [
#             {
#                 "c1": "1",
#                 "c2": "萨拉赫",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=118748",
#                 "c3": "利物浦",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=53",
#                 "c4": "29",
#                 "c5": "1"
#             },
#             {
#                 "c1": "2",
#                 "c2": "凯恩",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=78830",
#                 "c3": "热刺",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=66",
#                 "c4": "24",
#                 "c5": "2"
#             },
#             {
#                 "c1": "3",
#                 "c2": "阿圭罗",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=37572",
#                 "c3": "曼城",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=216",
#                 "c4": "21",
#                 "c5": "4"
#             },
#             {
#                 "c1": "4",
#                 "c2": "斯特林",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=103955",
#                 "c3": "曼城",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=216",
#                 "c4": "16",
#                 "c5": "1"
#             },
#             {
#                 "c1": "5",
#                 "c2": "瓦尔迪",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=101668",
#                 "c3": "莱斯特城",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=92",
#                 "c4": "16",
#                 "c5": "4"
#             },
#             {
#                 "c1": "6",
#                 "c2": "卢卡库",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=66749",
#                 "c3": "曼联",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=52",
#                 "c4": "15",
#                 "c5": "0"
#             },
#             {
#                 "c1": "7",
#                 "c2": "菲尔米诺",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=92217",
#                 "c3": "利物浦",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=53",
#                 "c4": "14",
#                 "c5": "1"
#             },
#             {
#                 "c1": "8",
#                 "c2": "孙兴民",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=85971",
#                 "c3": "热刺",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=66",
#                 "c4": "12",
#                 "c5": "0"
#             },
#             {
#                 "c1": "9",
#                 "c2": "莫拉塔",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=88482",
#                 "c3": "切尔西",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=60",
#                 "c4": "11",
#                 "c5": "0"
#             },
#             {
#                 "c1": "10",
#                 "c2": "阿扎尔",
#                 "c2L": "http://match.sports.sina.com.cn/football/player.php?id=42786",
#                 "c3": "切尔西",
#                 "c3L": "http://match.sports.sina.com.cn/football/team.php?id=60",
#                 "c4": "11",
#                 "c5": "2"
#             }
#         ]
#     }
# }







# entrance("英超")
