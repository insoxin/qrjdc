源码@博客-陆比柒



1.把CSS js改回mdui官方 防止第三方失效,也避免第三方中间人攻击.

2.增加 Cookie获取成功的提示自定义.

3.增加背景图自定义 同时修正css自适应北背景 默认 每日bing    其他推荐: [更多随机壁纸](https://api.isoyu.com/#/%E5%A3%81%E7%BA%B8%E6%A8%A1%E5%9D%97?id=_0-%e5%a3%81%e7%ba%b8%e6%a8%a1%e5%9d%97 "更多随机壁纸")

![image.png](https://dd-static.jd.com/ddimg/jfs/t1/107425/9/25402/1328235/6241997eE95fa05bf/af3ec8f26e7d0173.png)


使用方法

```
docker pull insoxin/qrjdc:latest
```


```
docker run -dit --name qrjdc -p 5100:5100 -v $PWD/qrjdc/config:/qrjdc/config --restart unless-stopped insoxin/qrjdc:latest
```

浏览器访问

ip＋端口号(默认5100)


对接青龙面板

修改映射目录下的config.json配置文件后
```
{
  "Main": {
    "Title": "JD找豆豆",
    "Bg": "https://api.isoyu.com/bing_images.php",
    "okTips": "Cookie获取成功的提示，如:已开启自动上传Cookie,请等待五分钟后查询,未开启则让用户自己手动复制增加",
    "Mode": "RES"
  },
  "QL": {
    "Open": 1,
    "Client_ID": "Open选项：1是打开面板上传，其余任何数字都代表关闭面板上传",
    "Client_Secret": "aaa",
    "URL": "QL面板的连接地址（HTTP或者HTTPS开头,结尾不要有 /)"
  },
  "Notice": "如果需要公告,请在此配置项里面些内容。不需要公告请此配置项留空"
}
```

重启容器

```
docker restart qrjdc
```