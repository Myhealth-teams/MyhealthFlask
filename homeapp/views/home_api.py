import random

from flask import Blueprint, jsonify

import db
from db.serializers import dumps
from models import Rotatiton, Infomation

home_blue = Blueprint("home_blue", __name__)


@home_blue.route("/rotation/", methods=("GET",))
def rotation():
    querys = db.session.query(Rotatiton).all()
    if querys.count() != 0:
        query = dumps(querys)

        return jsonify({
            "status": 200,
            "msg": "发送轮播图成功",
            "data": {
                "urls": query
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据"
        })

@home_blue.route("/info/",methods=("GET",))
def info():
    querys =db.session.query(Infomation).all()
    if querys.count() != 0:
        query = random.choice(dumps(querys))
        return jsonify({
            "status": 200,
            "msg": "发送咨询成功",
            "data": {
                "info": query
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据"
        })

@home_blue.route("/cheapgoods/",methods=("GET",))
def info():
    querys =db.session.query().all()
    if querys.count() != 0:
        query = dumps(querys)
        return jsonify({
            "status": 200,
            "msg": "发送打折商品数据成功",
            "data": {
                "goods": query
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据"
        })