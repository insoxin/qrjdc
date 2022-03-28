# -*- coding: utf-8 -*-
# @Time    : 2022/2/8 17:15
# @Author  : Nuanxinqing
# @Email   : nuanxinqing@gmail.com
# @File    : qinglong.py

import requests
import json
import re

with open("./config/config.json", encoding="utf-8") as f:
    config_json = json.load(f)

URL = config_json['QL']['URL']
Client_ID = config_json['QL']['Client_ID']
Client_Secret = config_json['QL']['Client_Secret']


def Get_token_start():
    url = URL + '/open/auth/token?client_id={}&client_secret={}'.format(Client_ID, Client_Secret)
    result = requests.get(url)
    result = result.json()
    return result


# 获取青龙面板token
def get_token():
    url = URL + '/open/auth/token?client_id={}&client_secret={}'.format(Client_ID, Client_Secret)
    result = requests.get(url)
    result = result.json()
    return result["data"]


# 获取全部Cookie
def FindCookie(ck):
    # Token
    tk = get_token()
    token = tk['token']
    expiration = tk['expiration']

    # 字符串合并
    bearer = "Bearer {}".format(token)
    params = 't={}'.format(expiration)

    # 请求信息
    url = URL + "/open/envs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.198 Mobile Safari/537.36",
        "Authorization": bearer,
        "content-type": "application/json"
    }

    # 获取并打印结果
    result = requests.get(url, headers=headers, params=params)
    result = result.text
    result_json = json.loads(result)
    # 判断是新增还是更新
    ResCode, mode = ReCookie(result_json, ck)
    if ResCode == 0:
        # 新增
        add_Cookie(func=0, _id=0, ck=ck, token=token, expiration=expiration)
    else:
        # 更新
        add_Cookie(func=1, _id=ResCode, ck=ck, token=token, expiration=expiration, mode=mode)


# 正则匹配：更新 & 新增
def ReCookie(result_json, ck):
    x = 0
    y = 0
    mode = ""
    # 正则匹配：pt_pin=([^;=\s]+)
    for i in result_json['data']:
        if re.search(r'pt_pin=([^;=\s]+)', i['value']) is None:
            continue
        else:
            if re.search(r'pt_pin=([^;=\s]+)', i['value']).group() == re.search(r'pt_pin=([^;=\s]+)', ck).group():
                x += 1

                if '_id' in i:
                    y = i['_id']
                    mode = "n"
                else:
                    y = i['id']
                    mode = "o"
                # 跳出
                break

    if x == 0:
        # 新增
        return 0, 0
    else:
        # 更新（_id：n， id：o）
        return y, mode


# 添加CK到面板
def add_Cookie(func, _id, ck, token, expiration, mode = ""):
    # 字符串合并
    bearer = "Bearer {}".format(token)
    params = 't={}'.format(expiration)

    # 请求信息
    url = URL + "/open/envs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.198 Mobile Safari/537.36",
        "Authorization": bearer,
        "content-type": "application/json"
    }

    # 获取并打印结果
    if func == 0:
        # 新增
        data = [{'value': str(ck), 'name': "JD_COOKIE"}]
        result = requests.post(url, data=json.dumps(data), headers=headers, params=params)
    else:
        # 更新
        if mode == "n":
            data = {'_id': _id, 'value': str(ck), 'name': "JD_COOKIE"}
            result = requests.put(url, data=json.dumps(data), headers=headers, params=params)
        else:
            data = {'id': _id, 'value': str(ck), 'name': "JD_COOKIE"}
            result = requests.put(url, data=json.dumps(data), headers=headers, params=params)

    result = result.text
    print(result)
