# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午11:07
import base64
import uuid


def new_token():
    return base64.b64encode(uuid.uuid4().hex.encode('utf-8')).decode("utf-8")
