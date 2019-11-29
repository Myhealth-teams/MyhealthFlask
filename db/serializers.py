# #!/usr/bin/python3
# # coding: utf-8
#
#
# def dumps(obj):
#     if isinstance(obj, list):
#         # 多个数据模型类对象的实例
#         return [
#             _clear_state(item.__dict__)
#             for item in obj
#         ]
#
#     return _clear_state(obj.__dict__)
#     # 普通的模型类的实例对象e(obj.__dict__)
#
#
# def _clear_state(instance: dict):
#     instance.pop('_sa_instance_state')
#     return instance
# !/usr/bin/python3
# coding: utf-8
from datetime import datetime

from models import Base


def dumps(obj):
    if isinstance(obj, list):
        # 多个数据模型类对象的实例
        data = []
        for item in obj:
            data.append(covert_instance(item))
        # print(data)
        return data

    return covert_instance(obj)


def covert_instance(item):
    item_dict = item.__dict__
    if '_sa_instance_state' in item_dict.keys():
        item_dict.pop('_sa_instance_state')
    instance = {}
    for key, value in item_dict.items():
        if isinstance(value, Base):
            instance[key] = dumps(value)
        elif isinstance(value, datetime):
            instance[key] = '%s-%s-%s' % (value.year, value.month, value.day)
        else:
            instance[key] = value
    return instance


def _clear_state(instance: dict):
    instance.pop('_sa_instance_state')
    return instance
