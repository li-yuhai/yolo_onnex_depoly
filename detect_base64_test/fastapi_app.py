'''
直接将检测结果数据流返回，也不保存原始输入图像
'''
import base64


from PIL import Image
from io import BytesIO
import time
from pest_detector import PestDetector
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

app = FastAPI()

origins = ["*"]

#  配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/hello')
def hello():
    return "hello"


@app.post("/process-json")
async def process_json(request: Request):
    # 使用 request.json() 方法获取 JSON 数据
    json_data = await request.json()

    # 处理 JSON 数据
    # 例如，假设 JSON 中有一个键为 "message"

    message = json_data.get("data", "No message provided")

    # 返回处理结果
    return {"result": f"Received JSON: {message}"}


# 定义全局变量
g_detector = PestDetector()

@app.post('/predict')
async def predict( request: Request ):
    '''
        {
          "data": [
            "<base64-encoded-image-data-1>",
            "<base64-encoded-image-data-2>",
            "<base64-encoded-image-data-3>",
            ...
          ]
        }
        返回的图片是base64编码
    '''
    # 从请求中检索出Base64编码的图像数据
    json_data = await request.json()
    data = json_data['data']
    # 初始化一个空数组以存储每个图像的预测结果
    predictions = []
    starttime = time.time()
    for item in data:
        img_name = item['name']
        image_data = item['img']
        # 解码Base64编码的图像数据并转换为NumPy数组
        decoded_data = base64.b64decode(image_data)
        image = Image.open(BytesIO(decoded_data))
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        # detector = PestDetector()
        # image_pred, predicted = detector.predict(image, img_name)
        global g_detector

        image_pred, predicted =  g_detector.predict(image, img_name)  # 使用全局变量来做
        # 将预测结果转换为JPEG编码的字节流
        buffer = BytesIO()
        image_pred.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        # print(image_base64)
        # 将当前图像的预测结果（包括预测的图像本身）添加到预测结果数组中
        predictions.append({'imgname':img_name,'pred_info': predicted, 'image': image_base64})

    end = time.time()
    # print(end-starttime)
    return predictions



if __name__ == '__main__':
    uvicorn.run(app =app, host = '0.0.0.0', port=9999)



