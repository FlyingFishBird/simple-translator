# -*- coding: utf-8 -*-

from hashlib import md5
from random import randint
from utils import *
import json

_COUNTRY = {'uk': u'英', 'usa': u'美'}


def _uuid():
    t = 0
    line_n = (8, 12, 16, 20)
    r = []

    while t < 32:
        if t in line_n:
            r.append('-')
        e = randint(0, 15)
        if t == 12:
            n = 4
        elif t == 16:
            n = 3 & e | 8
        else:
            n = e
        r.append(hex(n)[2:])

        t += 1

    return ''.join(r)


def _format(data):
    try:
        d = json.loads(data)
    except Exception as _:
        return WARN_NOT_FIND

    if d['status'] != 0:
        return WARN_NOT_FIND
    res = d['data']
    trans = res['translate']

    phonetic = get_val(res, 'common_dict.oxford.dict.0.content.0.phonetic')

    ret = []
    if phonetic:
        ps = [trans['text']]
        for k in phonetic:
            c = k['type']
            ps.append('%s: %s' % (_COUNTRY.get(c, c), k['text']))
        if ps:
            ret.append(' | '.join(ps))
    else:
        ret.append(trans['text'])
    ret.append(trans['dit'])
    return ' # '.join(ret)


def translate(text):
    text = text.strip()
    if not text:
        return ''

    lan_from, lan_to = 'auto', 'zh-CHS'
    m = md5()
    m.update((lan_from + lan_to + text +
              '41ee21a5ab5a13f72687a270816d1bfd').encode())
    s = m.hexdigest()

    text = url_quote(text).replace('%20', '+')

    payload = {
        'from': lan_from,
        'to': lan_to,
        'client': 'pc',
        'fr': 'browser_pc',
        'needQc': 1,
        'uuid': _uuid(),
        'pid': 'sogou-dict-vr',
        'oxford': 'on',
        'useDetect': 'off',
        'useDetectResult': 'off',
        'isReturnSugg': 'off',
        's': s
    }

    url = 'https://fanyi.sogou.com/reventondc/translateV1'
    data = urlencode(payload) + '&text=' + text
    req = Request(url, data.encode())
    try:
        resp = urlopen(req)
    except Exception as e:
        return NETWORK_ERROR

    if resp.getcode() != 200:
        return ERROR_QUERY

    res = resp.read()

    return _format(res)
