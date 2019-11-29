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
            for i,doctor in enumerate(data):
                doctor.update({"d_index": i})
            return jsonify({
                'status': 200,
                'msg': "获取该科室医生数据成功",
                'data': {
                    'doctors': data
                }
            })
        else:
            return jsonify({
                'status': 300,
                'msg': "暂无该科室医生数据"
            })


# 获取医生详情
@doctors_blue.route("/doctordetail/", methods=('POST',))
def get_doctordetail():
    try:
        req_data = request.get_json()
        r_id = req_data['d_id']
    except:
        return jsonify({
            'status': 400,
            'msg': "请求参数错误"
        })
    else:
        query = db.session.query(Doctor).filter(Doctor.d_id == r_id)
        if query.count() != 0:
            data = dumps(query.all())
            return jsonify({
                'status': 200,
                'msg': "获取医生详情成功",
                'data': {
                    'doctordetail': data
                }
            })
        else:
            return jsonify({
                'status': 300,
                'msg': "暂无该医生数据"
            })


# 获取默认地区医院医生数据
@doctors_blue.route('/default/', methods=("GET",))
def get_default():
    hospital = db.session.query(Hospital).filter(Hospital.cityid == 110100).first()
    room1 = db.session.query(Room).filter(Room.h_id==hospital.h_id)[1]
    room0 = db.session.query(Room).filter(Room.h_id==hospital.h_id).first()
    query0 = db.session.query(Doctor).filter(Doctor.room_id== room0.room_id)
    query1 = db.session.query(Doctor).filter(Doctor.room_id== room1.room_id)
    if any((query0.count() != 0,query1.count()!=0)):
        data = dumps(query0.all()+query1.all())
        for i, doctor in enumerate(data):
            doctor.update({"d_index": i})
        return jsonify({
            'status': 200,
            'msg': "获取默认医生数据成功",
            'data': {
                'doctors': data
            }
        })
    else:
        return jsonify({
            'status': 300,
            'msg': "暂无医生数据"
        })
