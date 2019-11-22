import random

from flask import Blueprint, jsonify, request

import db
from db.serializers import dumps
from models import Rotatiton, Infomation, DiscountGood

home_blue = Blueprint("home_blue", __name__)


@home_blue.route("/rotation/", methods=("GET",))
def rotation():
    querys = db.session.query(Rotatiton)
    if querys.count() != 0:
        query = dumps(querys.all())
        return jsonify({
            "status": 200,
            "msg": "获取轮播图数据成功",
            "data": {
                "urls": query
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据"
        })


@home_blue.route("/info/", methods=("GET",))
def info():
    querys = db.session.query(Infomation)
    if querys.count() != 0:
        query = random.choice(dumps(querys.all()))
        return jsonify({
            "status": 200,
            "msg": "获取资讯数据成功",
            "data": {
                "info": query
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据"
        })


@home_blue.route("/cheapgoods/", methods=("GET",))
def cheapgoods():
    count = request.args.get("count")
    querys = db.session.query(DiscountGood)
    if not count:
        if querys.count() != 0:
            query = dumps(querys.all())
            return jsonify({
                "status": 200,
                "msg": "获取打折商品数据成功",
                "data": {
                    "goods": query
                }
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "暂无数据"
            })
    else:
        if querys.count() != 0:
            query = dumps(querys.limit(count))
            return jsonify({
                "status": 200,
                "msg": "获取指定数量打折商品数据成功",
                "data": {
                    "goods": query
                }
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "暂无数据"
            })
