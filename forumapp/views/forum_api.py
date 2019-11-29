# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-28 上午10:09
from flask import Blueprint, request, jsonify

import db
from db.serializers import dumps
from models import Forum

forum_blue = Blueprint("forum_blue", __name__)


# 获取论坛所有信息的接口
@forum_blue.route('/all/', methods=("GET",))
def get_all():
    query = db.session.query(Forum)
    if query.count() != 0:
        data = dumps(query.all())
        return jsonify({
            "status": 200,
            "msg": "获取所有帖子成功",
            "data": data
        })
    else:
        return jsonify({
            "status": 300,
            "msg": "暂无帖子数据"
        })


# 用户发帖的接口
@forum_blue.route('/send/', methods=("POST",))
def send():
    try:
        req_data = request.get_json()
        u_id = req_data["u_id"]
        title = req_data["title"]
        content = req_data["content"]
    except:
        return jsonify({
            'status': 400,
            'msg': "请求参数错误"
        })
    else:
        add_text = Forum(u_id=u_id, f_title=title, f_content=content)
        db.session.add(add_text)
        db.session.commit()
        return jsonify({
            "status": 200,
            "msg": "发送帖子成功",
        })
