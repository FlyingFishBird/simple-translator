# -*- coding: utf-8 -*-

from hashlib import md5
from utils import *
import json
import os
import time

_CONF_FILE = os.path.join(os.environ.get('HOME'), '.sogoufanyi.json')

_CONF_KEY_PID = 'pid'
_CONF_KEY_KEY = 'key'


# 加载翻译配置
def _load_conf():
    try:
        with open(_CONF_FILE) as fp:
            return json.load(fp)
    except:
        return {}


_SOGOU_CONF = _load_conf()


def _format(data):
    try:
        d = json.loads(data)
    except Exception as _:
        return WARN_NOT_FIND
    if d['errorCode'] != '0':
        return WARN_NOT_FIND

    return d['query'] + ' # ' + d['translation']


def translate(text):
    # 判断配置文件是否正确
    pid, key = _SOGOU_CONF.get(_CONF_KEY_PID), _SOGOU_CONF.get(_CONF_KEY_KEY)
    if not pid or not key:
        return ERROR_SOGOU_CONFIG + ' ' + _CONF_FILE

    text = text.strip()
    if not text:
        return ''
    # 生成 sign
    salt = str(int(time.time()))
    m = md5()
    m.update((pid + text + salt + key).encode())
    s = m.hexdigest()

    payload = {
        'q': text,
        'from': 'auto',
        'to': 'zh-CHS',
        'pid': pid,
        'salt': salt,
        'sign': s,
    }
    url = 'http://fanyi.sogou.com/reventondc/api/sogouTranslate'
    data = urlencode(payload)
    req = Request(url, data.encode(), headers={'Accept': 'application/json'})
    try:
        resp = urlopen(req, None)
    except Exception as e:
        return NETWORK_ERROR

    if resp.getcode() != 200:
        return ERROR_QUERY

    res = resp.read()
    return _format(res)
