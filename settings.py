# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-19 下午6:37
import os

# 当前项目位置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件目录
IMAGES_STORE = os.path.join(BASE_DIR, 'static')
# mysql数据库配置
DB_CONFIG = {
    'host': '122.112.231.109',
    'port': 3306,
    'user': 'team',
    'password': '123456',
    'db': 'myhealth',
    'charset': 'utf8'
}

# flask配置
HOST = '0.0.0.0'
# 设置端口
PORT = '5000'

# redis配置
RHOST = '122.112.231.109'
RPORT = 6379
RDB = 9
RPWD = '123456'
