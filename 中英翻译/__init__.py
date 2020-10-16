""" 翻译扩展 """

import os
import re
import json
import urllib.request
import urllib.parse
import logging


from albertv0 import *

# logPath = "{}/translate.log".format(os.path.dirname(__file__))
# logging.basicConfig(level=logging.INFO, filename=logPath, encoding='utf-8',filemode="w")

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "中英翻译"
__version__ = "1.0.1"
__trigger__ = "tr "
__author__ = "Rectcircle"
__dependencies__ = []

googleIconPath = os.path.dirname(__file__) + "/google_translate.png"
baiduIconPath = os.path.dirname(__file__) + "/baidu_translate.jpg"
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
googleurltmpl = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}"
baiduurltmp = "https://fanyi.baidu.com/v2transapi?from={}&to={}"


def isEN(src):
    return re.search("""^[\x00-\xff]+$""", src) != None


def buildUrl(urltmpl, src):
    if isEN(src):
        return urltmpl.format("en", "zh", urllib.parse.quote(src))
    else:
        return urltmpl.format("zh", "en", urllib.parse.quote(src))


def googleTranslate(src):
    if src == "":
        return ""

    url = buildUrl(googleurltmpl, src)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data[0][0][0]
    except Exception as identifier:
        return src


def baiduTranslate(src):
    if src == "":
        return []
    url = "https://fanyi.baidu.com/sug"
    data = urllib.parse.urlencode({"kw": src})  # 将参数进行转码
    try:
        req = urllib.request.Request(
            url,
            data=bytes(data, encoding="utf-8"),
            headers={"User-Agent": ua, "Referer": "https://fanyi.baidu.com"},
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8")
            # json格式化
            html = json.loads(html)
            return html["data"]
    except Exception as identifier:
        return []


def handleQuery(query):
    if query.isTriggered:
        results = []
        src = query.string.strip()
        googletranslateresult = googleTranslate(src)
        results.append(
            Item(
                id="translate_%d" % 0,
                icon=googleIconPath,
                text=googletranslateresult,
                subtext="执行，将翻译结果复制到剪贴板",
                completion=query.rawString,
                actions=[
                    ClipAction("Copy translation to clipboard", googletranslateresult)
                ],
            )
        )
        baidutranslateresult = baiduTranslate(src)
        for index, res in enumerate(baidutranslateresult, 1):
            text = '{} {}'.format(res["k"], res["v"])
            results.append(
                Item(
                    id="translate_%d" % index,
                    icon=baiduIconPath,
                    text=text,
                    subtext="执行，将翻译结果复制到剪贴板",
                    completion=query.rawString,
                    actions=[ClipAction("Copy translation to clipboard", text)],
                )
            )
        return results