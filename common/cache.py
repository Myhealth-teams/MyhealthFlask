# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午11:10
from common import r15, r14


def add_token(phone,token):
    r15.set(phone,token)


def remove_token(token):
    r15.delete(token)


def valid_token(token):
    result = r15.get(token)
    if result:
        return True
    else:
        return False

def get_token(phone):
    # 获取token绑定的id
    token = r15.get(phone)
    return token


def set_code(phone, code):
    r14.set(phone, code, ex=120)


def valid_code(phone):
    result = r14.ttl(phone)
    if result:
        return True
    else:
        return False


def get_code(phone):
    code = r14.get(phone)
    return code
