""" 翻译扩展 """

import os
import re
import json
import urllib.request
import urllib.parse
from albertv0 import *

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "中英翻译"
__version__ = "1.0"
__trigger__ = "tr "
__author__ = "Rectcircle"
__dependencies__ = []

googleIconPath = os.path.dirname(__file__)+"/google_translate.png"
baiduIconPath = os.path.dirname(__file__)+"/baidu_translate.jpg"
ua = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
googleurltmpl = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=%s&tl=%s&dt=t&q=%s"



def isEN(src):
    return re.search("""^[\x00-\xff]+$""", src) != None


def buildUrl(urltmpl, src):
    if(isEN(src)):
        return urltmpl % ("en", "zh", urllib.parse.quote(src))
    else:
        return urltmpl % ("zh", "en", urllib.parse.quote(src))

def googleTranslate(src):
    if src=="": return ""

    url = buildUrl(googleurltmpl, src)
    req = urllib.request.Request(url, headers={'User-Agent': ua})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        return data[0][0][0]

def bauduTranslate(src):
    if src=="": return ""

    url = buildUrl(baiduurltmp, src)
    req = urllib.request.Request(url, headers={'User-Agent': ua,
                                               'Referer': 'http://fanyi.baidu.com'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        return data["trans_result"]["data"][0]['dst']


def handleQuery(query):
    if query.isTriggered:
        results = []
        src = query.string.strip();
        googletranslateresult = googleTranslate(src)
        results.append(
            Item(
                id="translate_%d" % 0,	
                icon=googleIconPath,
                text=googletranslateresult,
                subtext="执行，将翻译结果复制到剪贴板",
                completion=query.rawString,
                actions=[ClipAction("Copy translation to clipboard", googletranslateresult)]
            )
        )
        baidutranslateresult = googleTranslate(src)
        results.append(
            Item(
                id="translate_%d" % 1,	
                icon=baiduIconPath,
                text=baidutranslateresult,
                subtext="执行，将翻译结果复制到剪贴板",
                completion=query.rawString,
                actions=[ClipAction("Copy translation to clipboard", googletranslateresult)]
            )
        )
        return results