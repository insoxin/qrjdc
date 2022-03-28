# -*- coding: utf-8 -*-
# @Time    : 2021/12/14 10:28
# @Author  : Nuanxinqing
# @Email   : nuanxinqing@gmail.com
# @File    : cookie.py
import json
from panel import qinglong as ql


# Cookie提取
def clear(ck):
    pt_pin, pt_key = None, None
    for i in ck:
        if i['name'] == 'pt_pin':
            pt_pin = i["value"]

        if i['name'] == 'pt_key':
            pt_key = i['value']

    ck = merge(key=pt_key, pin=pt_pin)
    return ck


# Cookie合并
def merge(key, pin):
    cookie = "pt_key={}; pt_pin={};".format(key, pin)
    # logging.log(logging.INFO, )
    print("已获取Cookie：" + cookie)

    with open("./config/config.json", encoding="utf-8") as f:
        config_json = json.load(f)
    # 是否上传QL面板
    if config_json["QL"]["Open"] == 1:
        # 上传
        ql.FindCookie(cookie)

    return cookie
