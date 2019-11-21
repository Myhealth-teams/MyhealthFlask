#!/usr/bin/python3
# coding: utf-8


def dumps(obj):
    if isinstance(obj, list):
        # 多个数据模型类对象的实例
        return [
            _clear_state(item.__dict__)
            for item in obj
        ]

    return _clear_state(obj.__dict__)
    # 普通的模型类的实例对象e(obj.__dict__)


def _clear_state(instance: dict):
    instance.pop('_sa_instance_state')
    return instance