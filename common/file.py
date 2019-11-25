# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-23 下午2:45
import base64
from _sha1 import sha1


def change_filename(filename):
    try:
        file_name = filename.split(".")[0]
        ext_name = filename.split(".")[-1]
    except:
        file_name = filename
        ext_name = 'jpg'
    else:
        if file_name == ext_name:
            ext_name = 'jpg'
    img_name = sha1(file_name.encode(encoding='utf-8')).hexdigest() + '.' + ext_name
    return img_name


def save_file(path, name, b_file, ):
    with open(path + name, 'wb') as f:
        f.write(b_file)
    f.close()


def bytes_to_base64(b_file):
    return base64.b64encode(b_file).decode()


def base64_to_bytes(s_file):
    return base64.b64decode(s_file)
