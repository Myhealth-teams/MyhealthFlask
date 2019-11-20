# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午10:37

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://team:123456@122.112.231.109:3306/myhealth')
engine.connect()

# 基于engine生成数据库会话的Session类
_Session = sessionmaker(bind=engine)
session = _Session()