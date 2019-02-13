# -*- coding: utf-8 -*-

import collections
import xml.etree.ElementTree as ET
from utils import *
import json


def translate(word):
    if not word:
        return ''
    try:
        r = urlopen('http://dict.youdao.com' + '/fsearch?q=' + url_quote(word))
    except IOError:
        return NETWORK_ERROR
    if r.getcode() == 200:
        doc = ET.fromstring(r.read())

        phrase = doc.find(".//return-phrase").text
        p = re.compile(r"^%s$" % word, re.IGNORECASE)
        if p.match(phrase):
            info = collections.defaultdict(list)

            if not len(doc.findall(".//content")):
                return WARN_NOT_FIND

            for el in doc.findall(".//"):
                if el.tag in ('return-phrase', 'phonetic-symbol'):
                    if el.text:
                        info[el.tag].append(el.text)
                elif el.tag in ('content', 'value'):
                    if el.text:
                        info[el.tag].append(el.text)

            for k, v in info.items():
                info[k] = ' | '.join(v) if k == "content" else ' '.join(v)
                info[k] = info[k]

            tpl = ' %(return-phrase)s'
            if info["phonetic-symbol"]:
                tpl = tpl + ' [%(phonetic-symbol)s]'
            tpl = tpl + ' %(content)s'

            return tpl % info
        else:
            try:
                r = urlopen(
                    "http://fanyi.youdao.com" + "/translate?i=" +
                    url_quote(word),
                    timeout=5)
            except IOError:
                return NETWORK_ERROR

            p = re.compile(r"global.translatedJson = (?P<result>.*);")

            r_result = bytes_decode(r.read())
            s = p.search(r_result)
            if s:
                r_result = json.loads(s.group('result'))
                if r_result is None:
                    return str_decode(s.group('result'))

                error_code = r_result.get("errorCode")
                if error_code is None or error_code != 0:
                    return str_decode(s.group('result'))

                translate_result = r_result.get("translateResult")
                if translate_result is None:
                    return str_decode(s.group('result'))

                translate_result_tgt = ''
                for i in translate_result:
                    translate_result_tgt = translate_result_tgt + i[0].get(
                        "tgt") + "\n"

                return translate_result_tgt
            else:
                return ERROR_QUERY
    else:
        return ERROR_QUERY
