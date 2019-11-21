# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-19 下午6:51
from flask_cors import CORS

from goodsapp.views import goods_api
from homeapp.views import home_api
from mainapp import app
from settings import HOST, PORT
from mainapp.views import user_api


app.register_blueprint(user_api.user_blue, url_prefix='/user')
app.register_blueprint(goods_api.goods_blue, url_prefix='/goods')
app.register_blueprint(home_api.home_blue, url_prefix='/home')
CORS(app)
app.run(host=HOST, port=PORT)