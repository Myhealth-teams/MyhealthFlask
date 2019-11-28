import random

from flask import Blueprint, jsonify, request

import db
from db.db_util import make_sql
from db.serializers import dumps
from models import Rotatiton, Infomation, DiscountGood, RotationSelect, Good, Hospital, Notice

home_blue = Blueprint("home_blue", __name__)


@home_blue.route("/rotation/", methods=("GET",))
def rotation():
    querys = db.session.query(Rotatiton)
    select = db.session.query(RotationSelect).filter(RotationSelect.is_select == 1)
    if querys.count() != 0:
        data = dumps(querys.all())
        return jsonify({
            "status": 200,
            "msg": "获取轮播图数据成功",
            "data": {
                "urls": data,
                'state': select.first().name
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
        data = random.choice(dumps(querys.all()))
        return jsonify({
            "status": 200,
            "msg": "获取资讯数据成功",
            "data": {
                "info": data
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
            data = dumps(querys.all())
            return jsonify({
                "status": 200,
                "msg": "获取打折商品数据成功",
                "data": {
                    "goods": data
                }
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "暂无数据"
            })
    else:
        if querys.count() != 0:
            data = random.choices(dumps(querys.all()), k=int(count))
            return jsonify({
                "status": 200,
                "msg": "获取指定数量打折商品数据成功",
                "data": {
                    "goods": data
                }
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "暂无数据"
            })


@home_blue.route("/search/", methods=("POST",))
def search():
    data = request.get_json()
    search_str = data["search"]
    goods, doctor, hostipal = make_sql(search_str)
    return jsonify({
        'status': 200,
        'msg': "查询成功",
        "data": {
            "goods": goods,
            "doctor": doctor,
            "hospital": hostipal,
        }
    })

# 获取主页公告信息的接口
@home_blue.route("/notice/", methods=("GET",))
def get_notice():
    query = db.session.query(Notice).filter(Notice.is_use==True)
    if query.count() != 0:
        data = dumps(query.first())
        return jsonify({
            "status":200,
            "msg":"获取公告信息成功",
            "data":data
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无公告信息"
        })