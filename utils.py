# -*- coding: utf-8 -*-

import sys
import re

IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.parse import quote, urlencode
    from urllib.request import Request, urlopen
else:
    from urllib import quote, urlencode
    from urllib2 import Request, urlopen

WARN_NOT_FIND = ' 找不到释义'
ERROR_QUERY = ' 翻译查询出错'
NETWORK_ERROR = ' 无法连接翻译服务器'

QUERY_BLACK_LIST = [
    '.', '|', '^', '$', '\\', '[', ']', '{', '}', '*', '+', '?', '(', ')', '&',
    '=', '\'', '\'', '\t'
]


def str_encode(word):
    if IS_PY3:
        return word
    else:
        return word.encode('utf-8')


def str_decode(word):
    if IS_PY3:
        return word
    else:
        return word.decode('utf-8')


def bytes_decode(word):
    if IS_PY3:
        return word.decode()
    else:
        return word


def url_quote(word):
    if IS_PY3:
        return quote(word)
    else:
        return quote(word.encode('utf-8'))


def preprocess_word(word):
    word = word.strip()
    for i in QUERY_BLACK_LIST:
        word = word.replace(i, ' ')
    array = word.split('_')
    word = []
    p = re.compile('[a-z][A-Z]')
    for piece in array:
        lastIndex = 0
        for i in p.finditer(piece):
            word.append(piece[lastIndex:i.start() + 1])
            lastIndex = i.start() + 1
        word.append(piece[lastIndex:])
    return ' '.join(word).strip()


def get_val(data, keys):
    for k in keys.split('.'):
        if not isinstance(data, dict) and not isinstance(data, list):
            return None
        try:
            k = int(k)
        except Exception as _:
            pass

        try:
            data = data[k]
        except Exception as _:
            return None

    return data
