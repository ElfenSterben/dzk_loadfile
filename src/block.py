#coding:utf-8
from cocos.sprite import Sprite


class Block(object):
    def __init__(self, imagepath):
        super(Block, self).__init__()
        self.sprite = Sprite(imagepath)
        