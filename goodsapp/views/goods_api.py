from flask import jsonify, request
from flask import Blueprint

import db
from db.serializers import dumps
from models import Good, Medtype

goods_blue = Blueprint("goods_blue", __name__)


# @goods_blue.route("/allgoods/", methods=("GET",))
# def goods():
#     querys = db.session.query(Good)
#     if querys.count() != 0:
#         data = dumps(querys.all())
#         return jsonify({
#             "status": 200,
#             "msg": "查询所有商品成功",
#             "data": {
#                 "allgoods": data
#             }
#         })
#     else:
#         return jsonify({
#             "status": 300,
#             "msg": "暂无数据",
#         })

# 获取所有商品和商品类型的接口
@goods_blue.route('/goodstype/', methods=("GET",))
def all_goods_types():
    query_medtype = db.session.query(Medtype)
    query_goods = db.session.query(Good)
    if all((query_medtype.count() != 0, query_goods.count() != 0)):
        goods_type = dumps(query_medtype.all())
        all_goods = dumps(query_goods.all())
        for _good in all_goods:
            img_list = []
            imgs_str = _good["imgs"]
            for img_url in imgs_str.split(","):
                img_list.append(img_url)
            _good['imgs'] = img_list
        return jsonify({
            "status": 200,
            "msg": "获取所有商品类型成功",
            "data": {
                "goodstype": goods_type,
                "allgoods": all_goods
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

# 获取某商品信息的接口
@goods_blue.route('/goods_detail/', methods=("POST",))
def get_goods():
    try:
        req_data = request.get_json()
        g_id = req_data['goods_id']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(Good).filter(Good.goods_id== g_id)
        if query.count() != 0:
            data = dumps(query.first())
            return jsonify({
                "status": 200,
                "msg": "查询该分类所有商品成功",
                "data": {
                    "goods": data
                }
            })
        else:
            return jsonify({
                "status": 500,
                "msg": "查新商品失败",
            })