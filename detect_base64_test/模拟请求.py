
import base64
from PIL import Image
from io import BytesIO


# 读取图像文件
image_path = "img/test3.jpeg"  # 替换成实际的图像文件路径
with open(image_path, "rb") as image_file:
    # 将图像数据读取为字节流
    image_data = image_file.read()

# 将字节流编码为 Base64
base64_encoded = base64.b64encode(image_data).decode('utf-8')

# 打印 Base64 编码
# print("Base64 Encoded:", base64_encoded)

import requests
import base64

# 构造要发送的数据，包含多个 Base64 编码的图像数据
# data_to_send = {
#     "data": [
#         "<base64-encoded-image-data-1>",
#         "<base64-encoded-image-data-2>",
#         "<base64-encoded-image-data-3>",
#         # 添加更多图像数据
#     ]
# }

data_to_send = {
    "data": [
        {'name':'test.jpg', 'img': base64_encoded}
        # 添加更多图像数据
    ]
}


# 定义接口的 URL
url = " http://127.0.0.1:5000/predict"  # 替换成实际的服务器地址

# 发送 POST 请求
response = requests.post(url, json=data_to_send)

# 检查请求是否成功
if response.status_code == 200:
    # 解析响应结果
    predictions = response.json()
    print("Predictions:", predictions)
else:
    print("Error:", response.status_code, response.text)

print(type(predictions))

for item in predictions:
    image_data = item['image']
    image_name = item['imgname']

    decoded_data = base64.b64decode(image_data)
    image = Image.open(BytesIO(decoded_data))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(image_name)
