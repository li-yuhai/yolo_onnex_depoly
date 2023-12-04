

from datetime import datetime

def generate_unique_id():
    current_time = datetime.now()
    unique_id = current_time.strftime("%Y%m%d%H%M%S%f")[:-3]
    return unique_id

# 生成唯一ID
# unique_id = generate_unique_id()


# map颜色映射关系表
import random
class RandomColorGenerator:
    def __init__(self):
        self.category_color_map = {}

    def generate_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def get_color(self, category):
        if category not in self.category_color_map:
            # 如果类别没有颜色映射，则生成一个随机颜色
            random_color = self.generate_random_color()
            self.category_color_map[category] = random_color

        return self.category_color_map[category]

# # 创建颜色生成器对象
# color_generator = RandomColorGenerator()
#
# # 示例：获取类别对应的随机颜色
# cat_color = color_generator.get_color("cat")
# dog_color = color_generator.get_color("dog")
# bird_color = color_generator.get_color("bird")
#
# print(f"Cat color: {cat_color}")
# print(f"Dog color: {dog_color}")
# print(f"Bird color: {bird_color}")


