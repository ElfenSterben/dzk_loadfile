#coding:utf-8
from cocos.sprite import Sprite


class Paddle(object):
    def __init__(self, imagepath):
        super(Paddle, self).__init__()
        # 创建元素
        self.sprite = Sprite(imagepath)
        # 设置默认位置
        self.sprite.position = (320, self.sprite.height/2)
        # 设置移动状态
        self.move_right = False
        self.move_left = False
        # 设置板子默认移动速度
        self.speed = 10

    def reset(self):
        self.move_right = False
        self.move_left = False
        self.sprite.position = (320, self.sprite.height / 2)
        self.speed = 10

    def update(self):
        x, y = self.sprite.position
        if self.move_right:
            x += self.speed
        if self.move_left:
            x -= self.speed
        if x < (0 + self.sprite.width / 2):
            x = 0 + self.sprite.width / 2
        if x > (640 - self.sprite.width / 2):
            x = 640 - self.sprite.width / 2
        self.sprite.position = (x, y)
