
from cocos.sprite import Sprite


class Block(object):
    def __init__(self, live=0, anchor=(0, 0)):
        white = (255, 255, 255)
        blue = (0, 0, 255)
        self.colors = [white, blue]
        self.live = live
        self.sprite = Sprite('images/smallblock.png', anchor=anchor)
        self.sprite.color = self.colors[self.live]

    def reset(self):
        self.sprite.color = self.colors[self.live]
