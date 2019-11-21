from flask import jsonify, request
from flask import Blueprint

import db
from db.serializers import dumps
from goodsapp.models import Good, Medtype

goods_blue = Blueprint("goods_blue",__name__)


@goods_blue.route("/allgoods/", methods=("GET",))
def goods():
    querys = db.session.query(Good).all()
    query = dumps(querys)

    return jsonify({
        "status":200,
        "msg":"查询所有商品成功",
        "data":{
            "allgoods": query
        }
    })

@goods_blue.route('/goodstype/',methods=("GET",))
def types():
    querys = db.session.query(Medtype).all()
    query = dumps(querys)

    return jsonify({
        "status": 200,
        "msg":"返回所有商品的类型",
        "data": {
            "goodstype": query
        }
    })

@goods_blue.route('/choicetype/',methods=("POST",))
def choice():
    data = request.get_json()
    typeid = data.get("typeid")
    querys = db.session.query(Good).filter(Good.medtype==typeid).all()
    query = dumps(querys)


    return jsonify({
        "status":200,
        "msg":"返回该类型商品！",
        "data":{
            "goods":query
        }
    })
