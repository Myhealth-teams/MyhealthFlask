# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午9:25


from common.token_ import new_token
from models import User
from common.encrypt import encode4md5
import db
from flask import Blueprint, jsonify, request
from common.aliyun_sms import send_code
from common import r

user_blue = Blueprint("user_blue", __name__)


@user_blue.route('/phone/', methods=('POST',))
def send():
    try:
        req_data = request.get_json()
        phone = req_data['u_tel']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        code = send_code(phone)
        r.set(phone, code, ex=120)
        return jsonify({
            'status': 200,
            'msg': '获取验证码成功'
        })


@user_blue.route('/register/', methods=('POST',))
def register():
    try:
        req_data = request.get_json()
        phone, passwd, code = req_data['u_tel'], req_data['u_password'], req_data['u_code']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(User).filter(User.u_tel == phone)
        if query.count() == 0:
            result = r.ttl(phone)
            if not result:
                return jsonify({
                    'status': 300,
                    'msg': '验证码已过期'
                })
            else:
                code = r.get(phone)

                if code == code:
                    password = encode4md5(passwd)
                    new_user = User(u_tel=phone, u_password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    return jsonify({
                        'status': 200,
                        'msg': '注册成功'
                    })
                else:
                    return jsonify({
                        'status': 400,
                        'msg': '验证码错误'
                    })
        else:
            return jsonify({
                'status': 300,
                'msg': '手机号已存在'
            })


@user_blue.route('/login/', methods=('POST',))
def login():
    # 获取请求上传的json数据
    try:
        req_data = request.get_json()
        phone, pwd = req_data['u_tel'], req_data['u_password']
        if any((len(pwd.strip()), len(phone.strip()))) == 0:
            raise Exception()
    except Exception as e:
        print(e)
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(User).filter(User.u_tel == phone)
        if query.count() == 0:
            return jsonify({
                'status': 300,
                'msg': '查无此用户'
            })
        else:
            login_user = query.first()
            if encode4md5(pwd) == login_user.u_password:
                token = new_token()
                #
                return jsonify({
                    'status': 200,
                    'msg': '登陆成功',
                    'token': token,
                    'data': {
                        'u_id': login_user.id,
                        'u_name': login_user.u_name,
                        'u_tel': login_user.u_tel,
                        'u_image': login_user.u_image
                    }
                })
            else:
                return jsonify({
                    'status': 500,
                    'msg': '登录失败，用户名或密码错误'
                })
