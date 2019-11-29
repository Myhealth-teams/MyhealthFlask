# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午9:53
import base64
import hashlib

SECRET_KEY = 'a&Kiu#g32'


def encode4md5(txt):
    md5_ = hashlib.md5(txt.encode('utf-8'))
    md5_.update(SECRET_KEY.encode('utf-8'))
    return md5_.hexdigest()


if __name__ == '__main__':
    passwd = encode4md5('19951203')
    print(passwd)
