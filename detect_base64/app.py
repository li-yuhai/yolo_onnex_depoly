'''
直接将检测结果数据流返回，也不保存原始输入图像
'''
import base64
from PIL import Image
from flask import Flask, request
from io import BytesIO
import time
from pest_detector import PestDetector

app = Flask(__name__)

# 定义一个全局变量
app.config['detector'] = PestDetector()
# detector = PestDetector()

@app.route('/predict', methods=['POST'])
def predict():
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
    data = request.json['data']
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
        image_pred, predicted =  app.config['global_variable'].predict(image, img_name)  # 使用全局变量来做
        # 将预测结果转换为JPEG编码的字节流
        buffer = BytesIO()
        image_pred.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        # print(image_base64)
        # 将当前图像的预测结果（包括预测的图像本身）添加到预测结果数组中
        predictions.append({'imgname':img_name,'pred_info': predicted, 'image': image_base64})

    end = time.time()
    print(end-starttime)
    return predictions



if __name__ == '__main__':
    app.run()  # 运行app
