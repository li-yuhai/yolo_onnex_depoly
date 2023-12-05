# yolov5_onnx_server

## onnx介绍
ONNX 是一种用于表示机器学习的开放格式 模型。ONNX 定义了一组通用运算符（机器学习和深度学习模型的构建基块）和通用文件格式，使 AI 开发人员能够使用具有各种框架、工具、运行时和编译器的模型。  
官网地址：https://onnx.ai/
## yolov5_onnx_server功能
搭建onnx检测平台，并使用onnx格式模型文件检测目标，可本地使用，也可作为服务的方式，通过API向外部提供服务。

# 安装方式 
python版本：3.9（其他版本未做测试）
```
# clone本代码
git clone https://github.com/luosaidage/yolov5_onnx_server.git
# 安装依赖文件
pip install -r reuirements.txt

# 如需使用onnx硬件加速，需将reuirements里的onnxruntime替换为onnxruntime-gpu
```
## 单机运行
检测结果如下：
![检测结果](ReqFile/bus_detect.jpg)

## 服务部署
```
uvicorn main:app --reload --host 0.0.0.0
```
服务运行时显示如下：
然后打开浏览器访问：127.0.0.1:8000/docs
点击(try it out)，然后上传文件，点击Execute。
或者使用"python请求方式_demo.py"来执行文件

## 操作
使用的是时间戳来实现文件保存的名称唯一性。
1:模型加载一次操作 ，2:检测结果画出来，保存在det_img文件夹中 ，3:检测结果的json文件保存在det_json文件中，
4：上传检测的图片会保存在det_origin_img文件夹中，5：不同类别检测框的颜色不一样。6：只需载入一次模型即可。
7：添加跨域请求的处理

## 感谢原作者
感谢原作者提供的代码，本代码是在此 https://github.com/luosaidage/yolov5_onnx_server.git 基础上进行修改的。

## 问题与解决
1: 我将代码部署到云服务器上出现的问题是会出现502状态码，可能原因是负载均衡以及性能问题，我尝试使用nginx进行代理，没有效果，
最后通过使用pyhton的gunicorn(一个被广泛使用的高性能的Python WSGI UNIX HTTP服务器,使用非常简单，轻量级的资源消耗，以及高性能等特点)。
执行下述命令将开户 4 个工作进程，其中 UvicornWorker 的实现使用 uvloop 和httptools 实现。

https://fastapi.tiangolo.com/zh/deployment/server-workers/
https://github.com/tiangolo/fastapi/issues/680

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornH11Worker -b 0.0.0.0:8888 main:app
```


## linux操作
查看应用程序宽口，停止运行
```bash
sudo lsof -i -nP | grep LISTEN

kill -9 <pid>
```
