# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午9:52
import redis

from settings import RHOST, RPORT, RDB, RPWD

r = redis.Redis(host=RHOST, port=RPORT, db=RDB, password=RPWD, decode_responses=True)
