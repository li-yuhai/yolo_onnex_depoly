'''
直接将检测结果数据流返回，也不保存原始输入图像
'''
import base64
from PIL import Image
from flask import Flask

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def predict():
    return "hello"



if __name__ == '__main__':
    app.run()  # 运行app

