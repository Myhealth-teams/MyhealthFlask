import json

from flask import Blueprint, jsonify

import db
from db.serializers import dumps
from homeapp.models import Rotatiton

home_blue = Blueprint("home_blue", __name__)


@home_blue.route("/rotation/", methods=("GET",))
def rotation():
    querys = db.session.query(Rotatiton).all()
    query = dumps(querys)

    return jsonify({
        "status": 209,
        "msg": "传送轮播图成功",
        "data": {
            "url": query
        }
    })

