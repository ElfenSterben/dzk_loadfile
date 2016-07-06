#coding:utf-8
import random
from cocos.sprite import Sprite


class Level(object):
    def __init__(self, path='levelfile'):
        super(Level, self).__init__()
        self.levels = 1
        self.path = path
        self.blocks_pos = []
        self.blocks = []

    def start(self):
        self.level_from_file()

    def level_from_file(self):
        self.blocks_pos.clear()
        path = self.path + '\level' + str(self.levels) + '.txt'
        with open(path, 'r') as f:
            lines = f.readlines()
            for b in lines[1:]:
                pos = b.split(', ')
                x = int(pos[0])
                y = int(pos[1])
                self.blocks_pos.append([x, y])

    def reset(self):
        self.start()
        self.blocks = []
        positions = self.blocks_pos
        number_of_blocks = len(positions)
        for i in range(number_of_blocks):
            b = Sprite('images/block.png')
            x, y = positions[i]
            bx = x + b.width / 2
            by = y + b.height / 2
            b.position = (bx, by)
            # self.add(b)
            self.blocks.append(b)

    def next(self):
        self.levels += 1
        self.level_from_file()
        # block_width = 64
        # block_height = 10
        # i = random.randint(10, 150)
        # self.number_of_blocks = i
        # while i > 0:
        #     x = random.randrange(0, self.w, block_width)
        #     y = random.randrange(0, self.h, 10)
        #     bx = self.wstart + x + block_width / 2
        #     by = self.hstart + y + block_height / 2
        #     print(x, y)
        #     if (bx, by) not in self.blocks_pos:
        #         self.blocks_pos.append((bx, by))
        #         i -= 1


