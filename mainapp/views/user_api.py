# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午9:25

import uuid

from common.cache import set_code, valid_code, get_code, remove_token, add_token
from db.serializers import dumps
from settings import BASE_DIR
from common.file import change_filename, base64_to_bytes, save_file
from common.token_ import new_token
from models import User, UserAddres, FollowGood, FollowDoc
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
        set_code(phone, code)
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
            result = valid_code(u_phone)
            if not result:
                return jsonify({
                    'status': 300,
                    'msg': '验证码已过期'
                })
            else:
                code = get_code(u_phone)
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

# 用户登录的接口
@user_blue.route('/login/', methods=('POST',))
def login():
    # 获取请求上传的json数据
    try:
        req_data = request.get_json()
        phone, pwd = req_data['u_tel'], req_data['u_password']
        if any((len(pwd.strip()), len(phone.strip()))) == 0:
            raise Exception()
    except:
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
                add_token(phone,token)
                return jsonify({
                    'status': 200,
                    'msg': '登录成功',
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

# 用户登出的接口
@user_blue.route('/logout/', methods=('POST',))
def logout():
    try:
        data = request.get_json()
        u_phone = data['u_tel']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        remove_token(u_phone)
        return jsonify({
            'status':200,
            'msg': '退出登录成功'
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
                        'msg': '重置密码成功'
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
        u_id = data['u_id']
        upload_file = data['files']
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
            filepath = BASE_DIR + savepath
            file = base64_to_bytes(upload_file)
            save_file(filepath, filename, file)
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


# 获取用户所有收货地址的接口
@user_blue.route('/all_address/', methods=('GET',))
def get_address():
    u_id = request.args.get("id")
    if not u_id:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query_user = db.session.query(User).filter(User.id == u_id)
        if query_user.count() != 0:
            query = db.session.query(UserAddres).filter(UserAddres.id == u_id)
            if query.count() != 0:
                all_addr = dumps(query.all())
                return jsonify({
                    'status': 200,
                    'msg': '获取用户所有收货地址成功',
                    'data': all_addr
                })
            else:
                return jsonify({
                    'status': 300,
                    "msg": '该用户暂无收货地址'
                })
        else:
            return jsonify({
                'status': 500,
                "msg": '查无此用户'
            })


# 用户添加收货地址的接口
@user_blue.route('/add_address/', methods=('POST',))
def add_address():
    try:
        data = request.get_json()
        u_id, p_id, c_id, d_addr, u_name, u_tel, is_default = data['u_id'], data['provinceid'], data['cityid'], data[
            'detail_address'], data['user_name'], data['user_tel'], data['is_default']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(User).filter(User.id == u_id)
        if query.count() != 0:
            new_address = UserAddres(id=u_id, provinceid=p_id, cityid=c_id, user_name=u_name, user_tel=u_tel,
                                     detail_address=d_addr, is_default=is_default)
            db.session.add(new_address)
            db.session.commit()
            return jsonify({
                'status': 200,
                'msg': "添加收货地址成功"
            })
        else:
            return jsonify({
                'status': 300,
                'msg': '查无此用户'
            })


# 用户修改收货地址的接口
@user_blue.route('/alter_address/', methods=('POST',))
def alter_address():
    try:
        data = request.get_json()
        a_id, u_id, p_id, c_id, d_addr, u_name, u_tel, is_default = data['a_id'], data['u_id'], data['provinceid'], data[
            'cityid'], data['detail_address'], data['user_name'], data['user_tel'], data['is_default']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(UserAddres).filter(UserAddres.a_id == a_id)
        if query.count() != 0:
            addr = query.first()
            addr.update({UserAddres.province: p_id, UserAddres.cityid: c_id, UserAddres.detail_address: d_addr,
                         UserAddres.user_name: u_name, UserAddres.user_tel: u_tel, UserAddres.is_default: is_default})
            db.session.commit()
            return jsonify({
                'status': 200,
                'msg': "修改收货地址成功"
            })
        else:
            return jsonify({
                'status': 300,
                'msg': '记录不存在'
            })

# 用户添加关注药品的接口
@user_blue.route('/follow_goods/', methods=('POST',))
def follow_goods():
    try:
        req_data = request.get_json()
        u_id, g_id = req_data['u_id'], req_data['goods_id']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        new_follow_goods = FollowGood(u_id=u_id,goods_id=g_id)
        db.session.add(new_follow_goods)
        db.session.commit()
        return jsonify({
            'status':200,
            'msg': "关注药品成功"
        })

# 用户取消关注药品接口
@user_blue.route('/disfollow_goods/', methods=('POST',))
def disfollow_goods():
    try:
        req_data = request.get_json()
        u_id, g_id = req_data['u_id'], req_data['goods_id']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(FollowGood).filter(u_id==u_id,FollowGood.goods_id==g_id)
        if query.count()!=0:
            db.session.delete()
            db.session.commit()
            return jsonify({
                'status':200,
                'msg': "取消关注药品成功"
            })
        else:
            return jsonify({
                'status':300,
                'msg':"查无此记录"
            })
# 用户添加关注医生的接口
@user_blue.route('/follow_doctor/', methods=('POST',))
def follow_doctor():
    try:
        req_data = request.get_json()
        u_id, d_id = req_data['u_id'], req_data['d_id']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        new_follow_doctor = FollowDoc(u_id=u_id,d_id=d_id)
        db.session.add(new_follow_doctor)
        db.session.commit()
        return jsonify({
            'status':200,
            'msg': "关注医生成功"
        })
# 用户取消关注医生接口
@user_blue.route('/disfollow_doctor/', methods=('POST',))
def disfollow_doctor():
    try:
        req_data = request.get_json()
        u_id, d_id = req_data['u_id'], req_data['d_id']
    except:
        return jsonify({
            'status': 400,
            'msg': '请求参数错误'
        })
    else:
        query = db.session.query(FollowDoc).filter(d_id==d_id,u_id==u_id)
        if query.count()!=0:
            db.session.delete()
            db.session.commit()
            return jsonify({
                'status':200,
                'msg': "取消关注医生成功"
            })
        else:
            return jsonify({
                'status':300,
                'msg':"查无此记录"
            })
