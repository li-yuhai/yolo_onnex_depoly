from PIL import Image,ImageDraw
from utils.operation import YOLO
import os

from tool import generate_unique_id ,RandomColorGenerator


'''
1:模型加载一次操作
2:检测结果画出来，保存在det_img文件夹中
3:检测结果的json文件保存在det_json文件中

'''

yolo_model = None
def detect(onnx_path='ReqFile/yolov5n-7-k5.onnx',img_path=r'ReqFile/bus.jpg',show=False):
    '''
    检测目标，返回目标所在坐标如：
    {'crop': [57, 390, 207, 882], 'classes': 'person'},...]
    :param onnx_path:onnx模型路径
    :param img:检测用的图片
    :param show:是否展示
    :return:
    '''
    # import time
    # t1 = time.perf_counter()

    # 一次加载model模型
    global yolo_model
    yolo = yolo_model
    if yolo is None:
        yolo = YOLO(onnx_path=onnx_path)
        yolo_model = yolo

    det_obj = yolo.decect(img_path) # det_obj是一个list的类型

    # onnex的检测结果，没找到显示置信度的方式
    # 根据文件路径获取文件名称
    id  = os.path.basename(img_path).split(".")[0]

    # 保存json文件
    import json
    json_file_path = 'det_json/'+  id + '.json'
    # 写入数据到 JSON 文件
    with open(json_file_path, "w") as json_file:
        # json.dump(det_obj, json_file, indent=4)
        json.dump(det_obj, json_file)

    # 画出检测框，并且保存图片
    import cv2
    import matplotlib.pyplot as plt
    img_bgr = cv2.imread(img_path)
    num_bbox = len(det_obj)
    color_generator = RandomColorGenerator()  # 创建颜色生成器，不同类别不同颜色
    bbox_thickness = 4  # 框的线宽

    # 框类别文字
    bbox_labelstr = {
        'font_size': 1,  # 字体大小
        'font_thickness': 2,  # 字体粗细
        'offset_x': 0,  # X 方向，文字偏移距离，向右为正
        'offset_y': -5,  # Y 方向，文字偏移距离，向下为正
    }
    for idx in range(num_bbox):  # 遍历每个框
        # 预测的类别
        bbox_label = det_obj[idx]['classes']
        bbox_color = color_generator.get_color(bbox_label)
        bbox_xyxy = det_obj[idx]['crop']
        # 画框
        img_bgr = cv2.rectangle(img_bgr, (bbox_xyxy[0], bbox_xyxy[1]), (bbox_xyxy[2], bbox_xyxy[3]), bbox_color,
                                bbox_thickness)

        # 写框类别文字：图片，文字字符串，文字左上角坐标，字体，字体大小，颜色，字体粗细
        img_bgr = cv2.putText(img_bgr, bbox_label,
                              (bbox_xyxy[0] + bbox_labelstr['offset_x'], bbox_xyxy[1] + bbox_labelstr['offset_y']),
                              cv2.FONT_HERSHEY_SIMPLEX, bbox_labelstr['font_size'], bbox_color,
                              bbox_labelstr['font_thickness'])

    # 保存检测效果的图片
    det_img_path = 'det_img/' + id + '.jpg'
    cv2.imwrite(det_img_path, img_bgr)
    # t2 = time.perf_counter()
    # print(f'识别过程耗时：{t2 - t1}秒')

    # 封装数据数据，返回给前台
    return {'filename':id + '.jpg',
            'result': det_obj,
            'det_img_path': det_img_path,
            'det_origin_img': 'det_origin_img/' + id + '.jpg',
            'det_json': json_file_path}

    # return det_obj

# def detect(onnx_path='ReqFile/yolov5n-7-k5.onnx',img_path=r'ReqFile/bus.jpg',show=True):
#     '''
#     检测目标，返回目标所在坐标如：
#     {'crop': [57, 390, 207, 882], 'classes': 'person'},...]
#     :param onnx_path:onnx模型路径
#     :param img:检测用的图片
#     :param show:是否展示
#     :return:
#     '''
#     yolo = YOLO(onnx_path=onnx_path)
#     det_obj = yolo.decect(img_path)
#
#     # 结果
#     print (det_obj)
#
#     # 画框框
#     if show:
#         img = Image.open(img_path)
#         draw = ImageDraw.Draw(img)
#
#         for i in range(len(det_obj)):
#             draw.rectangle(det_obj[i]['crop'],width=3)
#         img.show()  # 展示

# if __name__ == "__main__":
#     detect()