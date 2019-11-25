from flask import Blueprint, request, jsonify
import db

from models import Cart

shopcar_blue = Blueprint("shopcar_blue", __name__)


@shopcar_blue.route('/addcart/', methods=('POST',))
def add_cart():
    try:
        request_data = request.get_json()
        u_id = request_data["u_id"]
        g_id = request_data["goods_id"]
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    try:
        cart = db.session.query(Cart).filter(Cart.u_id == u_id, Cart.goods_id == g_id)
        if cart.count() == 0:
            g_num = 1
            is_select = False
            new_cart = Cart(u_id=u_id, goods_id=g_id, c_goods_num=g_num, c_is_selected=is_select)
            db.session.add(new_cart)
            db.session.commit()
        else:
            current_cart = cart.first()
            current_cart.c_goods_num += 1
            db.session.add(current_cart)
            db.session.commit()
        return jsonify({
            'status': 200,
            'msg': '添加购物车成功'
        })
    except:
        return jsonify({
            'status': 300,
            'msg': "添加购物车失败"
        })


@shopcar_blue.route('/subcart/', methods=('POST',))
def sub_cart():
    try:
        request_data = request.get_json()
        u_id = request_data["u_id"]
        g_id = request_data["goods_id"]
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        try:
            cart = db.session.query(Cart).filter(Cart.u_id == u_id, Cart.goods_id == g_id)
            current_cart = cart.first()
            if current_cart.c_goods_num > 1:
                current_cart.c_goods_num -= 1
                db.session.add(current_cart)
                db.session.commit()
            else:
                db.session.delete(current_cart)
                db.session.commit()
            return jsonify({
                'status': 200,
                'msg': '删除购物车成功'
            })
        except:
            return jsonify({
                'status': 300,
                'msg': "删除购物车失败"
            })
