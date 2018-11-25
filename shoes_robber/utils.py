import re


def replace_size(string, size):
    print(string, size)
    largest_index = len(string) - 1
    for i, c in enumerate(string):
        is_size = True

        if not c.isalpha():
            is_size = False

        if c.isalpha():
            if 0 <= i - 1 <= largest_index:
                if string[i - 1].isalpha() or string[i - 1].isdigit():
                    is_size = False
            if 0 <= i + 1 <= largest_index:
                if string[i - 1].isalpha() or string[i - 1].isdigit():
                    is_size = False

        if is_size:
            return "".join([size if _i == i else _c for _i, _c in enumerate(string)])
    return string


def replace_example(msg, id_, phone, size):
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
                return replace_size(p1 + p2 + p3, size)
    except Exception as e:
        return msg


def demo_replace():
    print(replace_example("例如：15900000000,310221111111110000,Y", "310227199406260019", "15900749626", "D"))
    print(replace_example("例如：15900000000,310221111111110000,Y", "31022719940626001X", "15900749626", "D"))


if __name__ == '__main__':
    demo_replace()
