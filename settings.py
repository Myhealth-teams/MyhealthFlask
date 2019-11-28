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
RDB15 = 15
RDB14 = 14
RPWD = '123456'

# 订单状态
ORDERS_STATE_NOPAY = 0  # 已下单未付款
ORDERS_STATE_NOSEND = 1  # 已付款未发货
ORDERS_STATE_NOREACH = 2  # 已发货未到达
ORDERS_STATE_NORECEIVE = 3  # 已到达未签收
ORDERS_STATE_NOASSESS = 4  # 已签收未评价