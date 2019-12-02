import datetime
import uuid

from flask import Blueprint, request, jsonify
import db
from db.serializers import dumps

from models import Cart, Orderlist, UserAddres, Orderdetail, Good
from settings import ORDERS_STATE_NOPAY

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
            if cart.count() !=0:
                current_cart = cart.first()
                if current_cart.c_goods_num > 1:
                    current_cart.c_goods_num -= 1
                    db.session.commit()
                    return jsonify({
                        'status': 200,
                        'msg': '购物车商品数量减少成功'
                    })
                else:
                    db.session.delete(current_cart)
                    db.session.commit()
                    return jsonify({
                        'status': 200,
                        'msg': '删除购物车商品成功'
                    })
            else:
                return jsonify({
                    'status': 300,
                    'msg': '购物车记录不存在'
                })
        except:
            return jsonify({
                'status': 500,
                'msg': "删除购物车失败"
            })

# 删除购物车商品接口
@shopcar_blue.route('/delcart/', methods=('POST',))
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
            if cart.count()!=0:
                current_cart = cart.first()
                db.session.delete(current_cart)
                db.session.commit()
                return jsonify({
                    'status': 200,
                    'msg': '删除购物车商品成功'
                })
            else:
                return jsonify({
                    'status': 300,
                    'msg': '购物车记录不存在'
                })
        except:
            return jsonify({
                'status': 500,
                'msg': "删除购物车商品失败"
            })

# 获取用户购物车所有商品
@shopcar_blue.route('/cart_allgoods/', methods=("POST",))
def cart_allgoods():
    try:
        req_data = request.get_json()
        u_id = req_data["u_id"]
    except:
        return jsonify({
            "status": 400,
            "msg": "请求参数错误"
        })
    else:
        query = db.session.query(Cart).filter(Cart.u_id == u_id)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                "status": 200,
                "msg": "获取用户购物车成功",
                "data": data
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "用户购物车为空"
            })

        # 生成订单
        '''
            {
                "u_id": 6,
                "price": 20,
                "nums": 3,
                "goods": [
                    {
                        "goods_id": 1,
                        "goods_num": 1
                    },
                    {
                        "goods_id": 2,
                        "goods_num": 2
                    }
                ]
            }
        '''


@shopcar_blue.route('/order/', methods=("POST",))
def go_order():
    try:

        req_data = request.get_json()
        u_id = req_data["u_id"]
        o_price = req_data["price"]
        o_num = req_data["nums"]
        o_goods = req_data["goods"]
    except:
        return jsonify({
            "status": 400,
            "msg": "请求参数错误"
        })
    else:
        try:
            # 生成订单
            o_identifier = uuid.uuid4().hex
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            a_id = db.session.query(UserAddres).filter(UserAddres.id == u_id,
                                                       UserAddres.is_default == True).first().a_id
            new_order = Orderlist(o_identifier=o_identifier, u_id=u_id, o_price=o_price, o_time=now_time, o_nums=o_num,
                                  o_state=ORDERS_STATE_NOPAY, a_id=a_id)
            db.session.add(new_order)
            # db.session.commit()
            # 生成订单详情
            o_id = db.session.query(Orderlist).filter(Orderlist.o_identifier == o_identifier).first().o_id
            for good in o_goods:
                g_id = good["goods_id"]
                g_num = good["goods_num"]
                new_order_detail = Orderdetail(o_id=o_id, goods_id=g_id, goods_num=g_num)
                db.session.add(new_order_detail)
                # db.session.commit()
                # 删除购物车记录
                for good in o_goods:
                    g_id = good["goods_id"]
                    cart = db.session.query(Cart).filter(Cart.u_id == u_id, Cart.goods_id == g_id).first()
                    db.session.delete(cart)
        except:
            db.session.rollback()
            return jsonify({
                "status": 500,
                "msg": "添加订单失败"
            })
        else:
            db.session.commit()
            return jsonify({
                "status": 200,
                "msg": "添加订单成功"
            })


# 获取用户所有订单
@shopcar_blue.route('/all_order/', methods=("POST",))
def get_all_order():
    try:
        req_data = request.get_json()
        u_id = req_data["u_id"]
    except:
        return jsonify({
            "status": 400,
            "msg": "请求参数错误"
        })
    else:
        query = db.session.query(Orderlist).filter(Orderlist.u_id == u_id)
        if query.count() != 0:
            all_order = dumps(query.all())
            for order in all_order:
                o_id = order["o_id"]
                all_od = dumps(db.session.query(Orderdetail).filter(Orderdetail.o_id == o_id).all())
                o_detail = []
                for od in all_od:
                    goods_id = od["goods_id"]
                    goods = dumps(db.session.query(Good).filter(Good.goods_id == goods_id).first())
                    od.update({"goods": goods})
                    o_detail.append(od)
                order.update({"order_detail": o_detail})
            data = all_order
            return jsonify({
                "status": 200,
                "msg": "获取用户所有订单成功",
                "data": data
            })
        else:
            return jsonify({
                "status": 300,
                "msg": "该用户暂无订单"
            })
