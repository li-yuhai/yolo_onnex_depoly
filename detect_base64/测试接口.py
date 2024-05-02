from PIL import Image
from io import BytesIO
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

# 读取图像文件
image_path = "bus.jpg"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()
base64_encoded = base64.b64encode(image_data).decode('utf-8')

data_to_send = { "data": [ {'name':'test.jpg', 'img': base64_encoded}] }

# 定义接口的 URL
url = "http://127.0.0.1:5000/predict"
response = requests.post(url, json=data_to_send, timeout=30)
if response.status_code == 200:
    predictions = response.json()
    print("Predictions:", predictions)
else:
    print("Error:", response.status_code, response.text)

# for item in predictions:
#     image_data = item['image']
#     image_name = item['imgname']
#     # 保存检测后图像
#     decoded_data = base64.b64decode(image_data)
#     image = Image.open(BytesIO(decoded_data))
#     if image.mode == 'RGBA':
#         image = image.convert('RGB')
#     image.save('test_img/' + image_name)

