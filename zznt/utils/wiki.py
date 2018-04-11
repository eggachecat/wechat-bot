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
