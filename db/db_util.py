# !/usr/bin/env python
# -*-coding:UTF-8-*-
# __author__ = pighui
# __time__ = 2019-11-26 下午7:57
import pymysql


def get_conn():
    conn = pymysql.connect(
        host="122.112.231.109",
        user="team",
        password="123456",
        port=3306,
        database="myhealth",
        charset="utf8"
    )
    return conn


def search_all(sql_g, sql_d, sql_h):
    conn = get_conn()
    try:
        cursor_g = conn.cursor()
        cursor_d = conn.cursor()
        cursor_h = conn.cursor()
        cursor_g.execute(sql_g)
        cursor_d.execute(sql_d)
        cursor_h.execute(sql_h)
        item_g = cursor_g.fetchall()
        item_d = cursor_d.fetchall()
        item_h = cursor_h.fetchall()
        return item_g, item_d, item_h
    except Exception as e:
        conn.rollback()
        return [], [], []
    finally:
        cursor_h.close()
        cursor_d.close()
        cursor_g.close()
        conn.close()


def make_sql(str):
    str_sec = "'%" + str + "%'"
    sql_g = "select goods_id,goods_name from goods where goods_name like {} limit 5;".format(str_sec)
    sql_d = "select d_id,d_name from doctors where d_name like {} limit 5;".format(str_sec)
    sql_h = "select h_id,hname from hospitals where hname like {} limit 5;".format(str_sec)
    gs, ds, hs = search_all(sql_g, sql_d, sql_h)
    goods, doctor, hostipal = package_search(gs, ds, hs)
    return goods, doctor, hostipal


def package_search(gs, ds, hs, ):
    g = ["goods_id", "goods_name"]
    d = ["h_id", "hname"]
    h = ["d_id", "d_name"]
    goods = []
    doctor = []
    hostipal = []
    for i in range(len(gs)):
        sublist = {}
        for j in range(len(g)):
            sublist[g[j]] = gs[i][j]
        goods.append(sublist)
    for i in range(len(ds)):
        sublist = {}
        for j in range(len(d)):
            sublist[d[j]] = ds[i][j]
        doctor.append(sublist)

    for i in range(len(hs)):
        sublist = {}
        for j in range(len(h)):
            sublist[h[j]] = hs[i][j]
        hostipal.append(sublist)

    return goods, doctor, hostipal
