from flask import jsonify, request
from flask import Blueprint

import db
from db.serializers import dumps
from models import Good, Medtype

goods_blue = Blueprint("goods_blue", __name__)


@goods_blue.route("/allgoods/", methods=("GET",))
def goods():
    querys = db.session.query(Good)
    if querys.count() != 0:
        data = dumps(querys.all())
        return jsonify({
            "status": 200,
            "msg": "查询所有商品成功",
            "data": {
                "allgoods": data
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据",
        })


@goods_blue.route('/goodstype/', methods=("GET",))
def types():
    querys = db.session.query(Medtype)
    if querys.count() != 0:
        data = dumps(querys.all())
        return jsonify({
            "status": 200,
            "msg": "获取所有商品类型成功",
            "data": {
                "goodstype": data
            }
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无数据",
        })


@goods_blue.route('/choicetype/', methods=("POST",))
def choice():
    try:
        req_data = request.get_json()
        typenum = req_data['typenum']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(Good).filter(Good.medtype == typenum)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                "status": 200,
                "msg": "查询该分类所有商品成功",
                "data": {
                    "goods": data
                }
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "暂无数据",
            })
