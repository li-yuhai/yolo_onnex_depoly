### 1.onnx介绍
ONNX 是一种用于表示机器学习的开放格式 模型。ONNX 定义了一组通用运算符（机器学习和深度学习模型的构建基块）和通用文件格式，使 AI 开发人员能够使用具有各种框架、工具、运行时和编译器的模型。  
官网地址：https://onnx.ai/


### 2.yolo_onnx_server功能
搭建onnx检测平台，并使用onnx格式模型文件检测目标，可本地使用，也可作为服务的方式，通过API向外部提供服务。

### 3.安装方式 
python版本：3.9（其他版本未做测试）
```
# clone本代码
git clone https://github.com/luosaidage/yolov5_onnx_server.git

# 安装依赖文件
pip install -r reuirements.txt

# 如需使用onnx硬件加速，需将reuirements里的onnxruntime替换为onnxruntime-gpu
```

###  4.服务部署
```
uvicorn main:app --reload --host 0.0.0.0

请求接口的数据格式
    "data": [
        {'name':'test1.jpg', 'img': base64_encoded},
        {'name':'test2.jpg', 'img': base64_encoded}
        ## 添加更多图像数据
    ]
    
接口返回数据格式
    [
        {
            imgname: 'testxx.jpg',  
            pre_info: [{"x1":70,"y1":137,"x2":459,"y2":200,"score":0.92,"class_id":1,"class_name":"二化螟"}], 
            image: base64_encoded # 返回检测结果图像
        },
         {
            imgname: 'testxx.jpg',  
            pre_info: [{"x1":70,"y1":137,"x2":459,"y2":200,"score":0.92,"class_id":1,"class_name":"二化螟"}], 
            image: base64_encoded # 返回检测结果图像
        },
    ]
```


###  4.感谢原作者
感谢原作者提供的代码，本代码是在此 https://github.com/luosaidage/yolov5_onnx_server.git 基础上进行修改的。

### 6.问题与解决
1: 我将代码部署到云服务器上出现的问题是会出现502状态码，可能原因是负载均衡以及性能问题，我尝试使用nginx进行代理，没有效果，
最后通过使用pyhton的gunicorn(一个被广泛使用的高性能的Python WSGI UNIX HTTP服务器,使用非常简单，轻量级的资源消耗，以及高性能等特点)。
执行下述命令将开户 4 个工作进程，其中 UvicornWorker 的实现使用 uvloop 和httptools 实现。
(注意关闭云服务器的防火墙  )。注意在部署后，代码中不要还有print等语句，会出错。
```bash
//临时关闭
systemctl stop firewalld

//禁止开机启动
systemctl disable firewalld
```

https://fastapi.tiangolo.com/zh/deployment/server-workers/
https://github.com/tiangolo/fastapi/issues/680

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker -b 0.0.0.0:8888 main:app
```


### 7.linux操作
查看应用程序宽口，停止运行
```bash
sudo lsof -i -nP | grep LISTEN

# 关闭端口号为7777的应用程序
ps -ef | grep 7777 | grep -v grep | cut -c 9-15 | xargs kill -9

kill -9 <pid>
```
