import random

from flask import Blueprint, jsonify, request

import db
from db.db_util import make_sql
from db.serializers import dumps
from models import Rotatiton, RotationSelect, Infomation, DiscountGood, Notice, FollowDoc, FollowGood

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

# 获取打折商品信息
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
            data = dumps(querys.limit(count).all())
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

# 搜索接口
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

# 获取用户关注的３个医生
@home_blue.route("/follow_doctor/", methods=("POST",))
def get_doctor():
    try:
        req_data = request.get_json()
        u_id = req_data["u_id"]
    except:
        return jsonify({
            "status":400,
            "msg":"请求参数错误"
        })
    else:
        query = db.session.query(FollowDoc).filter(FollowDoc.u_id==u_id).limit(3)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                "status":200,
                "msg":"获取用户关注的三个医生成功",
                "data":data
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "该用户暂未关注任何医生"
            })

# 获取用户关注的３个商品
@home_blue.route("/follow_goods/", methods=("POST",))
def get_goods():
    try:
        req_data = request.get_json()
        u_id = req_data["u_id"]
    except:
        return jsonify({
            "status": 400,
            "msg": "请求参数错误"
        })
    else:
        query = db.session.query(FollowGood).filter(FollowGood.u_id == u_id).limit(3)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                "status": 200,
                "msg": "获取用户关注的三个商品成功",
                "data": data
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "该用户暂未关注任何商品"
            })