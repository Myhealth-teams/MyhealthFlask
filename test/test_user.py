# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-20 上午11:17
import base64
from unittest import TestCase

import requests

base_url = 'http://122.112.231.109:5000/user/'


class TestUser(TestCase):
    def test_phone(self):
        url = base_url + 'phone/'
        data = {
            'u_tel': '15609318020'
        }
        resp = requests.get(url, json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('status'), 201)
        print(resp.json())
    def test_register(self):
        url = base_url+'register/'
        data = {
            'u_tel': '15609318020',
            'u_password': '123456',
            'u_code': 5655
        }
        resp = requests.post(url, json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('status'), 202)
        print(resp.json())
    def test_login(self):
        url = base_url + "login/"
        data = {
            'u_tel': '15609318020',
            'u_password': '123456'
        }
        resp = requests.post(url, json=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().get('status'), 203)
        print(resp.json())
    def test_head(self):
        url = base_url + 'head/'
        with open('mei.jpg', 'rb') as f:
            file = f.read()  # 二进制字节
        print(file)
        bytes_to_base64 = base64.b64encode(file).decode() # 将二进制字节编码为base64字符串
        print(bytes_to_base64)
        base64_to_bytes = base64.b64decode(bytes_to_base64) #将base64字符串解码为二进制字节
        print(base64_to_bytes)
        data = {
            "u_id":5,
            'files': bytes_to_base64
        }
        response = requests.post(url,json=data)
        print(response.json())