
所有源码均来自博客-陆比柒，也是科技玩家ID☀暖心情   

我把CSS js改回mdui官方 防止第三方失效
也避免第三方中间人攻击

# 说明
JDCookie获取Python 学习版

当前状态：测试版

没有写Selenium多实例管理，只支持同时间单用户使用

## 驱动

选择自己系统的驱动下载并解压到chromedriver目录里面

地址：https://npm.taobao.org/mirrors/chromedriver/

Tips：如果你的版本是Google Chrome 99.0.4844.xx， 那么你可以直接使用我压缩包内的驱动文件，无需重新下载（别忘记赋予775权限）

## 安装
运行环境(必须)：Python3.7 +

```text
# 上传源码

# 安装所需的库
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 启动
python3 app.py
```

体验地址：http://自己的IP:5100

## 配置文件
```json
{
  "Main": {
    "Title": "网站标题"
  },
  "QL": {
    "QL_Name": "QL面板名字",
    "Client_ID": "ID",
    "Client_Secret": "Secret",
    "URL": "QL面板地址（结尾不要有 /）"
  }
}
```

## 错误排查

看当前目录下的QRJDC说明书
