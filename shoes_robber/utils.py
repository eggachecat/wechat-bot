import re


def middleware_filehelper(msg):
    if msg.FromUserName == "filehelper":
        print(msg)


def replace_example(msg, id_, phone):
    print(msg, id_, phone)
    id_pattern = re.compile(r"[0-9]{18}")
    phone_pattern = re.compile(r"[0-9]{11}")
    try:
        for s in msg.splitlines():
            s = s.strip()
            if "例如：" in s:
                s = s.replace("例如：", "")
                id_pos = id_pattern.search(s).span()
                p1 = phone_pattern.sub(phone, s[:id_pos[0]])
                p2 = id_pattern.sub(id_, s[id_pos[0]:id_pos[1]])
                p3 = phone_pattern.sub(phone, s[id_pos[1]:])
                return p1 + p2 + p3
    except:
        return msg


def test_replace():
    print(replace_example("例如：15900000000,310221111111110000,asd", "310227199406260019", "15900749626"))


if __name__ == '__main__':
    test_replace()
