# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午11:10
from common import r
def add_token(token, user_id):
    r.set(token, user_id)


def remove_token(token):
    r.delete(token)


def valid_token(token):
    result = r.get(token)
    if result:
        return True

def get_token(token):
    # 获取token绑定的id
    id = r.get(token)
    return id