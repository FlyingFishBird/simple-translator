# -*- coding: utf-8 -*-

import sys
from utils import preprocess_word, str_encode
from os.path import abspath, splitext, dirname


def load_translate_mod(name):
    pkg_path = dirname(abspath(__file__))
    sys.path.insert(0, pkg_path)

    try:
        pkg = __import__(name)
        return getattr(pkg, 'translate')
    except Exception as e:
        print('翻译插件 %s 不存在' % name)
        sys.exit(1)


def main():
    argv = sys.argv

    if len(argv) < 3:
        sys.exit(0)

    # 加载模块路径
    translate = load_translate_mod(argv[1])

    # 执行翻译
    res = translate(preprocess_word(' '.join(argv[2:])))
    sys.stdout.write(str_encode(res))


if __name__ == "__main__":
    main()
