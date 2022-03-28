// QRJDC傻妞辅助插件
// [rule:QQ]
// [rule:qq]
// [rule:Qq]
// [rule:QQ扫码]
// [rule:qq扫码]
// [rule:Qq扫码]

// 插件参数
// url替换为自己的QRJDC地址，结尾不要带斜杠：/
// 举例：http://192.168.1.1:5100
let url = "";

// 以下内容不要动
let num = "";
let code = ""

// Main 入口
function main() {
    if (url == "") {
        sendText("JDC对接地址为空，请对接后使用")
        return;
    }
    // 启动提示语
    sendText("欢迎使用QR扫码登录插件【回复“q”、“Q”即可退出】。回复数字“1”，获取登录二维码");
    // 获取内容
    num = input();
	if(num == "q" || num == "Q"){
		sendText("已退出")
		return;
	}else{
        sendText("正在获取登录二维码,请耐心等待.如果二维码提示过期,请先使用'Q'退出后重新获取");
        getQR();
	}
}

// getQR 申请QR
function getQR() {
    // api/GetQR  获取二维码
    let GetQRUrl = url + "/api/GetQR"

    // 发送请求
    let result = request({
        "url": GetQRUrl, //请求链接
        "method": "post", //请求方法
        "dataType": "json",
        "timeout": 60*1000,
    });

    if (!result) {
        sendText("运行出错, 请尝试升级到(1647961947311)或以上版本");
        return;
    }

    // 判断状态
    if (result.code == 1001) {
        numRandom = Math.round(Math.random()*10000);
        console.log(url + "/img/" + String(numRandom));
        let ImgUrl = url + "/img/" + String(numRandom) + ".png"
        sendImage(ImgUrl);

        sendText("QR获取成功, 扫码登陆后请回复：“2”");
        num = input();
        if(num == "q" || num == "Q"){
            quitQRJDC();
            sendText("已退出");
            return;
        }else if(num == "2"){
            // 发送登录请求
            LoginQR();
        } else {
            sendText("请勿乱回复，已自动退出");
            quitQRJDC();
            return;
        }
    } else {
        sendText("服务出错，请联系管理员");
        return;
    }
}

function LoginQR() {
    // api/LoginQR  扫码登录
    let LoginQRUrl = url + "/api/LoginQR"

    // 发送请求
    let result = request({
        "url": LoginQRUrl, //请求链接
        "method": "post", //请求方法
        "dataType": "json",
        "timeout": 60*1000,
    });

    if (!result) {
        quitQRJDC();
        sendText("获取超时,请重新申请登录");
        return;
    }

    // 判断状态
    if (result.code == 1001) {
        // 获取成功
        sendText("Cookie获取成功");
        sendText(result.msg);
    } else if(result.code == 1010) {
        // 需要二次验证
        sendText("需要二次验证,请输入收到的短信验证码：");
        LoginCode();
    } else {
        sendText("Cookie获取失败，请重新获取");
        return;
    }
}

function LoginCode() {
    // api/LoginCode  二次验证登录
    let LoginCodeUrl = url + "/api/LoginCode"
    code = input();

    if(code == "q" || code == "Q"){
        quitQRJDC();
        sendText("已退出");
        return;
    } else {
        // 发送请求
        let body = {"code":code}
        let result = request({
            "url": LoginCodeUrl, //请求链接
            "method": "post", //请求方法
            "dataType": "json",
            "body": body,
            "timeout": 60*1000,
        });
        
        if (!result) {
            quitQRJDC();
            sendText("获取超时,请重新申请登录");
            return;
        }

        // 判断状态
        if (result.code == 1001) {
            // 获取成功
            sendText("Cookie获取成功");
            sendText(result.ck);
        } else {
            quitQRJDC();
            sendText("Cookie获取失败，请检查验证码是否正确后重新登录");
            return;
        }
    }

}

// 退出QRJDC
function quitQRJDC(){
    let quitQRUrl = url + "/quit"
    request({
        "url": quitQRUrl, //请求链接
        "method": "post", //请求方法
        "timeout": 60*1000,
    });
}

main()