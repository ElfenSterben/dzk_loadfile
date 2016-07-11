#coding:utf-8
import random
from cocos.sprite import Sprite
from src.block import Block

class Level(object):
    def __init__(self, path='levelfile'):
        super(Level, self).__init__()
        self.levels = 1
        self.path = path
        self.blocks_props = []
        self.blocks = []

    def load(self):
        '''加载关卡数据'''
        self.blocks_props.clear()
        path = self.path + '\level' + str(self.levels) + '.txt'
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
                for b in lines:
                    prop = b.split(', ')
                    if len(prop) < 3:
                        prop.append('0')
                    x = int(prop[0])
                    y = int(prop[1])
                    live = int(prop[2])
                    self.blocks_props.append((x, y, live))
                return True
        except:
            return False

    def reset(self):
        '''生成blocks'''
        self.load()
        self.blocks = []
        blocks_props = self.blocks_props
        number_of_blocks = len(blocks_props)
        for i in range(number_of_blocks):
            x, y, live = blocks_props[i]
            b = Block()
            bx = int(x)
            by = int(y)
            b.sprite.position = (bx, by)
            b.live = live
            b.reset()
            self.blocks.append(b)

    def next(self):
        '''载入下一关的坐标'''
        self.levels += 1
        return self.load()

