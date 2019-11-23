# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午9:25
import os
import uuid
from _sha1 import sha1
from settings import BASE_DIR
from common.file import change_filename, base64_to_bytes, save_file
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
        u_phone, u_passwd, u_code = req_data['u_tel'], req_data['u_password'], req_data['u_code']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(User).filter(User.u_tel == u_phone)
        if query.count() == 0:
            result = r.ttl(u_phone)
            if not result:
                return jsonify({
                    'status': 300,
                    'msg': '验证码已过期'
                })
            else:
                code = r.get(u_phone)

                if code == u_code:
                    password = encode4md5(u_passwd)
                    new_user = User(u_tel=u_phone, u_password=password)
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


# 用户忘记密码的接口，即找回密码
@user_blue.route('/forget_pwd/', methods=('POST',))
def forget_pwd():
    try:
        req_data = request.get_json()
        u_phone, u_passwd, u_code = req_data['u_tel'], req_data['u_password'], req_data['u_code']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(User).filter(User.u_tel == u_phone)
        if query.count() != 0:
            result = r.ttl(u_phone)
            if not result:
                return jsonify({
                    'status': 300,
                    'msg': '验证码已过期'
                })
            else:
                code = r.get(u_phone)
                if code == u_code:
                    new_password = encode4md5(u_passwd)
                    user = query.first()
                    user.u_password = new_password
                    db.session.commit()
                    return jsonify({
                        'status': 200,
                        'msg': '修改密码成功'
                    })
                else:
                    return jsonify({
                        'status': 400,
                        'msg': '验证码错误'
                    })
        else:
            return jsonify({
                'status': 300,
                'msg': '该手机号未注册'
            })


# 用户修改密码的接口，即更新密码
@user_blue.route('/new_pwd/', methods=('POST',))
def new_pwd():
    try:
        req_data = request.get_json()
        u_id, u_passwd, new_password = req_data['u_id'], req_data['u_password'], req_data['new_password']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(User).filter(User.id == u_id)
        old_password = encode4md5(u_passwd)
        user = query.first()
        if old_password != user.u_password:
            return jsonify({
                'status': 400,
                'msg': '旧密码错误'
            })
        else:
            new_pwd = encode4md5(new_password)
            user.u_password = new_pwd
            db.session.commit()
            return jsonify({
                'status': 200,
                'msg': '修改密码成功'
            })


# 用户更新头像的接口
@user_blue.route('/head/', methods=('POST',))
def head_image():
    try:
        data = request.get_json()
        u_id = data.get('u_id')
        upload_file = data.get('files')
        print(u_id)
        print(upload_file)
    except:

        return jsonify({
            "status": 400,
            'msg': "请求参数错误"
        })
    else:
        try:
            savepath = "/static/imgs/"
            uuid_str = uuid.uuid4().hex
            filename = change_filename(uuid_str)
            filepath = BASE_DIR + savepath + filename
            file = base64_to_bytes(upload_file)
            save_file(filepath,filename,file)
            print(file,'\n',filepath,'\n',filename)
        except:
            return jsonify({
                'status': 500,
                'msg': "上传失败，请重新上传"
            })
        else:
            query = db.session.query(User).filter(User.id == u_id)
            if query.count() != 0:
                user = query.first()
                user.u_image = savepath + filename
                db.session.commit()
                return jsonify({
                    "status": 200,
                    'msg': "修改头像成功",
                    'data': {
                        'u_image': savepath + filename
                    }
                })
            else:
                return jsonify({
                    "status": 300,
                    'msg': "查无此用户"
                })