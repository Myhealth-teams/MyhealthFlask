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
def desc_table():
    conn = get_conn()
    sql_goods = "desc goods;"
    sql_doctor = "desc doctors;"
    sql_hostial = "desc hospitals;"
    try:
        cursor_g = conn.cursor()
        cursor_d = conn.cursor()
        cursor_h = conn.cursor()

        cursor_g.execute(sql_goods)
        cursor_d.execute(sql_doctor)
        cursor_h.execute(sql_hostial)
        item_g = cursor_g.fetchall()
        print(item_g)
        item_d = cursor_d.fetchall()
        item_h = cursor_h.fetchall()
        return item_g,item_d,item_h
    except:
        conn.rollback()
        return [],[],[]
    finally:
        cursor_h.close()
        cursor_d.close()

        cursor_g.close()
        conn.close()

def search_all(sql_g,sql_d,sql_h):
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
    except:
        conn.rollback()
        return [], [], []
    finally:
        cursor_h.close()
        cursor_d.close()
        cursor_g.close()
        conn.close()




def make_sql(g,d,h,str):
    g_str = ""
    d_str = ""
    h_str = ""

    for i in g:
        g_str += i[0] + " like '%"+str+"%' or "
    g_str1 = g_str[:-3]

    for j in d:
        d_str += j[0] + " like '%"+str+"%' or "
    d_str1 = d_str[:-3]

    for k in h:
        h_str += k[0] + " like '%"+str+"%' or "
    h_str1 = h_str[:-3]
    sql_g ="select * from goods where {};".format(g_str1)
    sql_d ="select * from doctors where {};".format(d_str1)
    sql_h ="select * from hospitals where {};".format(h_str1)
    gs,ds,hs = search_all(sql_g,sql_d,sql_h)
    goods,doctor,hostipal = package_search(gs,ds,hs,g,d,h)

    return goods,doctor,hostipal

def package_search(gs,ds,hs,g,d,h):
    goods = []
    doctor = []
    hostipal = []
    for i in range(len(gs)):
        sublist = {}
        for j in range(len(g)):
            sublist[g[j][0]]=gs[i][j]
        goods.append(sublist)

    for i in range(len(ds)):
        sublist = {}
        for j in range(len(d)):
            sublist[d[j][0]]=ds[i][j]
        doctor.append(sublist)

    for i in range(len(hs)):
        sublist = []
        for j in range(len(h)):
            sublist[h[j][0]]= hs[i][j]
        hostipal.append(sublist)

    return goods,doctor,hostipal





