from fastapi import FastAPI, UploadFile, File

from io import BytesIO
from PIL import Image,ImageDraw
from utils.operation import YOLO
import uvicorn


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置允许域名
origins = [
    "http://localhost:8080",
    "http://localhost:1024",
]

# origins = ["*"]  # 允许所有的请求

#  配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======= 静态资源写法
from fastapi.staticfiles import StaticFiles
app.mount("/static/det_img", StaticFiles(directory="det_img"), name="det_img")  # 目标检测的检测图
app.mount("/static/det_origin_img", StaticFiles(directory="det_origin_img"), name="det_origin_img") # 目标检测的原图
app.mount("/static/det_json", StaticFiles(directory="det_json"), name="det_json") # 目标检测后的json文件


from detect import detect as img_detect
from tool import generate_unique_id ,RandomColorGenerator
# def detect(onnx_path='ReqFile/yolov5n-7-k5.onnx',img=r'ReqFile/bus.jpg',show=True):
#     '''
#     检测目标，返回目标所在坐标如：
#     {'crop': [57, 390, 207, 882], 'classes': 'person'},...]
#     :param onnx_path:onnx模型路径
#     :param img:检测用的图片
#     :param show:是否展示
#     :return:
#     '''
#     yolo = YOLO(onnx_path=onnx_path)  # 加载yolo类
#     det_obj = yolo.decect(img)  # 检测
#
#     # 打印检测结果
#     print (det_obj)
#
#     # 画框框
#     if show:
#         img = Image.open(img)
#         draw = ImageDraw.Draw(img)
#
#         for i in range(len(det_obj)):
#             draw.rectangle(det_obj[i]['crop'],width=3)
#         img.show()  # 展示
#     return det_obj
#

@app.post("/detect/")
async def create_upload_file(file: UploadFile = File(...)):
    # contents = await file.read()  # 接收浏览器上传的图片
    # im1 = BytesIO(contents)  # 将数据流转换成二进制文件存在内存中

    id = generate_unique_id()  # 获取唯一id数值，图片明
    img_name_path = 'det_origin_img/' + id + '.jpg'  # 保存的图像路径
    contents = await file.read()
    with open(img_name_path, 'wb') as f:
        f.write(contents)

    # 返回结果
    return img_detect(onnx_path='ReqFile/yolov5n-7-k5.onnx', img_path=img_name_path, show=False)

 # [{"crop":[57,390,207,882],"classes":"person"},{"crop":[220,411,348,855],"classes":"person"},{"crop":[672,394,810,874],"classes":"person"},{"crop":[2,237,799,770],"classes":"bus"}]

if __name__ == '__main__':
    uvicorn.run(app =app, host = '0.0.0.0', port=8000)


