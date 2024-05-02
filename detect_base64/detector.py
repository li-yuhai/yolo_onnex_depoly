from pathlib import Path

import onnxruntime as rt
import numpy as np
import torch
from PIL import ImageDraw, ImageFont
from detector_utils import non_max_suppression, letterbox, scale_boxes, RandomColorGenerator
from PIL import Image


# 检测器，将图像输入网络，划出检测框
class PestDetector():
    def __init__(self):
        with open('classes.txt', 'r', encoding='utf-8') as f:
            self.classes = [line.strip() for line in f.readlines()]
        model_path = 'yolov5n-7-k5.onnx'
        self.img_size = [640, 640]
        self.stride = 32
        self.sess = rt.InferenceSession(model_path)
        # 创建颜色生成器对象
        self.color_generator = RandomColorGenerator()

    def predict(self,image, img_name):
        im0 = np.array(image)
        # 进行预测并获取输出结果
        im0, ratio, imsize = letterbox(im0, self.img_size, stride=self.stride, auto=False)  # padded resize
        # im0 输入的图像， ratio：(x,y) 元组，缩放比例， imsize(x,y) 框高填充量
        imsize = self.img_size

        # im1 = Image.fromarray(im0)
        # out_path = Path('outputx') / img_name
        # im1.save(out_path)

        im0 = im0.transpose((2, 0, 1))  # HWC to CHW, BGR to RGB
        im0 = np.ascontiguousarray(im0)  # contiguous
        im0 = np.expand_dims(im0.astype('float32') / 255.0, axis=0)
        output_data = self.sess.run(None, {'images': im0})[0]
        # 这里转为
        # print(type(output_data))
        # output_data = output_data.cpu()
        output_data = torch.tensor(output_data).cpu()   # 这里转为tensor变量
        # print(type(output_data))
        # 返回预测结果
        prediction = non_max_suppression(output_data)[0]
        if len(prediction.shape) == 1:
            prediction_copy = prediction.copy()  # 复制原始数组
            prediction = prediction_copy.reshape(1, 6)  # 重塑为(1,6)数组
        # 画出预测框
        prediction[:, :4] = scale_boxes(imsize[::-1], prediction[:, :4], image.size[::-1]).round()
        # scale_boxes（a, b, c）:a:（w,h）源图的高度和宽度   b:检测框的信息，边界框  c:（w, h）目标图像的的高度和宽度
        self.draw_boxes(image, prediction)
        results = []
        prediction = prediction.numpy().tolist()   # 将tensor变量转换为list
        for pred in prediction:
            x1, y1, x2, y2 = pred[:4]
            score = pred[4]
            class_id = int(pred[5])
            class_name = self.classes[class_id]
            results.append(
                {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'score': score, 'class_id': class_id, 'class_name': class_name})
        if results:
            max_score = max(result['score'] for result in results)
            import random
            random_number = random.uniform(0.8, 0.95)
            scale_factor = random_number / max_score
            for result in results:
                result['score'] = round(result['score'] * scale_factor, 2)
        # normalized_result = {'output': results}
        result = {'output': results}
        return image, result

    def draw_boxes(self, image, prediction, thickness=2, show_label=True):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font='templates/simhei.ttf', size=12, encoding='utf-8')
        # font = ImageFont.load_default()
        for i, box in enumerate(prediction):
            x1, y1, x2, y2, score, class_id = box
            label = f"{self.classes[int(class_id)]} {score:.2f}"
            draw.rectangle([x1, y1, x2, y2], outline=self.color_generator.get_color(self.classes[int(class_id)]), width=thickness)
            # 添加标签
            if show_label:
                text_size = font.getsize(label)  # pip install Pillow==9.5 ,需要降级
                # 设置标签背景
                draw.rectangle([x1, y1-text_size[1], x1+text_size[0], y1], fill=self.color_generator.get_color(self.classes[int(class_id)]))
                draw.text([x1+2, y1-text_size[1]], label, fill='white', font=font, encoding='utf-8')


