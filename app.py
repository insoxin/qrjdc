# -*- coding: utf-8 -*-
# @Time    : 2021/12/14 10:23
# @Author  : Nuanxinqing
# @Email   : nuanxinqing@gmail.com
# @File    : app.py

import json
import requests
from panel import qinglong as ql
from pyselenium import QRSelenium as qps
from flask import Flask, render_template, jsonify, request, redirect
from flask_cors import cross_origin
from gevent import pywsgi

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    # 读取JSON文件
    with open("./config/config.json", encoding="utf-8") as file:
        configJson = json.load(file)

    Title = configJson["Main"]["Title"]
    Bg    = configJson["Main"]["Bg"]
    if configJson['Notice'] == "":
        Notice = ""
        return render_template("index.html", Title=Title, Bg=Bg, Notice=Notice)
    else:
        Notice = configJson['Notice']
        return render_template("index_2.html", Title=Title, Bg=Bg, Notice=Notice)


@app.route("/api/LoginCode", methods=['POST'])
@cross_origin(supports_credentials=True)
def logincode():
    data = request.get_json(force=True)
    code = data.get("code")
    if len(code) == 6:
        num = qps.QRPhoneCode(code)
        if num == 1002:
            return jsonify(code=1002, msg="Cookie获取失败，请重新获取")
        else:
            return jsonify(code=1001, msg="Cookie获取成功", ck=num)
    else:
        return jsonify(code=1002, msg="请输入正确的验证码")


@app.route('/QRLogin')
def qrLogin():
    with open("./config/config.json", encoding="utf-8") as file:
        configJson = json.load(file)

    Title = configJson["Main"]["Title"]
    Bg    = configJson["Main"]["Bg"]
    okTips    = configJson["Main"]["okTips"]
    return render_template("qrLogin.html", Bg=Bg, okTips=okTips, Title=Title)


@app.route('/api/GetQR', methods=['POST'])
@cross_origin(supports_credentials=True)
def getQR():
    num = qps.QRStart()
    if num == 1001:
        return jsonify(code=1001)
    else:
        return jsonify(code=1002)


@app.route('/api/LoginQR', methods=['POST'])
@cross_origin(supports_credentials=True)
def QRLogin():
    num = qps.QRStart2()
    if num == 1002:
        return jsonify(code=1002, msg="Cookie获取失败，请重新获取")
    elif num == 1010:
        return jsonify(code=1010, msg="需要二次短信验证码")
    else:
        return jsonify(code=1001, msg=num)


@app.route('/img/<id>')
@cross_origin(supports_credentials=True)
def img(id):
    print("ID值为：" + id)
    return redirect("/static/QR/2.png", code=302)


@app.route('/quit', methods=['POST'])
def quit_B():
    qps.quitBrowser()
    return jsonify(code=1001)


@app.errorhandler(404)
def r404():
    return jsonify(code=404, msg="请求页面不存在，404错误")


if __name__ == '__main__':
    login = """
            
            Welcome to JDC
                        
                        By：nuanxinqing
            
    """
    print(login)

    # 读取JSON文件
    with open("./config/config.json", encoding="utf-8") as f:
        config_json = json.load(f)

    # 检查是否开启QL上传
    if config_json["QL"]["Open"] == 1:
        # 打开QL上传, 检查面板连通性
        try:
            res = ql.Get_token_start()
            if res['code'] == "400":
                logging.log(logging.ERROR, res['message'])
                print(res['message'])
            else:
                print("面板连接成功")

        except requests.exceptions.ConnectionError:
            print("面板连接超时,请检查面板地址是否正确")
        except requests.exceptions.InvalidURL:
            print("请检查URL地址是否书写正确")

    if config_json["Main"]["Mode"] == "DEBUG":
        app.debug = True
        server = pywsgi.WSGIServer(('0.0.0.0', 5100), app)
        server.serve_forever()
    else:
        app.debug = False
        server = pywsgi.WSGIServer(('0.0.0.0', 5100), app)
        server.serve_forever()
