# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-25 下午8:53
from flask import Blueprint, request, jsonify

import db
from db.serializers import dumps
from models import Province, City, Hospital, Room, Doctor

doctors_blue = Blueprint("doctors_blue", __name__)


# 获取该地区所有医院的接口
@doctors_blue.route('/hospitals/', methods=("POST",))
def get_hospitals():
    try:
        req_data = request.get_json()
        c_id = req_data['cityid']
    except:
        return jsonify({
            'status': 400,
            'msg': "请求参数错误"
        })
    else:
        query = db.session.query(Hospital).filter(Hospital.cityid == c_id)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                'status': 200,
                'msg': "获取该地区医院数据成功",
                'data': {
                    'hospitals': data
                }
            })
        else:
            return jsonify({
                'status': 300,
                'msg': "暂无该地区医院数据"
            })

# 获取某医院所有科室的接口
@doctors_blue.route("/rooms/", methods=('POST',))
def get_rooms():
    try:
        req_data = request.get_json()
        h_id = req_data['h_id']
    except:
        return jsonify({
            'status': 400,
            'msg': "请求参数错误"
        })
    else:
        query = db.session.query(Room).filter(Room.h_id == h_id)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                'status': 200,
                'msg': "获取该医院科室数据成功",
                'data': {
                    'rooms': data
                }
            })
        else:
            return jsonify({
                'status': 300,
                'msg': "暂无该医院科室数据"
            })

# 获取某科室所有医生的接口
@doctors_blue.route("/doctors/", methods=('POST',))
def get_doctors():
    try:
        req_data = request.get_json()
        r_id = req_data['room_id']
    except:
        return jsonify({
            'status': 400,
            'msg': "请求参数错误"
        })
    else:
        query = db.session.query(Doctor).filter(Doctor.room_id == r_id)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                'status': 200,
                'msg': "获取该科室医生数据成功",
                'data': {
                    'rooms': data
                }
            })
        else:
            return jsonify({
                'status': 300,
                'msg': "暂无该科室医生数据"
            })