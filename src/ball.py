#coding:utf-8
from cocos.sprite import Sprite


class Ball(object):
    def __init__(self, imagepath):
        super(Ball, self).__init__()
        # 创建元素
        self.sprite = Sprite(imagepath)
        # 设置初始点
        self.reset_position = (0, 0)
        self.sprite.position = self.reset_position
        # 设置速度
        self.speedx = 5
        self.speedy = 5
        # 设置状态
        self.alive = True
        self.fired = False

    def reset(self):
        self.alive = True
        self.fired = False
        self.speedx = 5
        self.speedy = 5
        self.sprite.position = self.reset_position

    def fire(self):
        self.fired = True

    def hit(self):
        self.speedy = -self.speedy

    def dead(self):
        return not self.alive

    def update(self):
        if not self.fired:
            return
        x, y = self.sprite.position
        s = self.sprite
        if self.fired:
            if x < (0 + s.width / 2) or x > (640 - s.width / 2):
                self.speedx = -self.speedx
            if y > (480 - s.height / 2):
                self.speedy = -self.speedy
            x += self.speedx
            y += self.speedy
            self.sprite.position = (x, y)
            if y < 0:
                self.alive = False

