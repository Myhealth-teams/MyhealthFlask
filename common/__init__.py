# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午9:52
import redis

from settings import RHOST, RPORT, RDB15,RDB14, RPWD

r15 = redis.Redis(host=RHOST, port=RPORT, db=RDB15, password=RPWD, decode_responses=True)
r14 = redis.Redis(host=RHOST, port=RPORT, db=RDB14, password=RPWD, decode_responses=True)
