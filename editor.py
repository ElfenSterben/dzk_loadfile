from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.director import director
from cocos.sprite import Sprite
from pyglet.window.key import symbol_string
from cocos.scenes import SplitColsTransition
import main

class Editor(Layer):
    is_event_handler = True

    def __init__(self):
        super(Editor, self).__init__()
        label = Label('关卡编辑器')
        label2 = Label('按S键保存')
        # 以下两个标签用于提示用户编辑窗的位置
        buttom = 299
        top = 451
        line1 = Sprite('images/line.png', position=(0, buttom), anchor=(0, 0))
        line2 = Sprite('images/line.png', position=(0, top), anchor=(0, 0))
        self.saveflag = Label('未保存', position=(300, 0))
        label.position = (0, 0)
        label2.position = (200, 0)

        self.add(label)
        self.add(label2)
        self.add(self.saveflag)
        self.add(line1)
        self.add(line2)

        # 鼠标按下标志和坐标
        self.mouse_press_left = False
        self.mouse_press_right = False
        self.mouse_x = 0
        self.mouse_y = 0

        # 编辑区属性
        self.editor_bottom = 300
        self.editor_top = 450
        self.editor_left = 0
        self.editor_right = 640

        # 预定坐标
        self.postmp = []
        self.create_grid()
        # 存储坐标
        self.pos = []
        # 存储bloks
        self.blocks = []
        self.schedule(self.update)

    def create_grid(self):
        b = Sprite('images/block.png')
        for x in range(0, self.editor_right, b.width):
            for y in range(self.editor_bottom, self.editor_top, b.height):
                self.postmp.append((x, y))

    def press_left(self, x, y, b):
        if self.mouse_press_left:
            b.position = (x, y)
            self.add(b)
            self.blocks.append(b)
            self.pos.append((x, y))

    def press_right(self, x, y, b):
        if self.mouse_press_right:
            for b in self.blocks:
                print(b.position)
                if b.position == (x, y):
                    self.blocks.remove(b)
                    self.remove(b)
                    self.pos.remove((x, y))
                    break

    def update_blocks(self):
        '''更新砖块'''
        b = Sprite('images/block.png', anchor=(0, 0))
        b.position = (self.mouse_x, self.mouse_y)
        r = b.get_rect()
        for x, y in self.postmp:
            bx = x + b.width
            by = y + b.height
            if r.contains(bx, by):
                if (x, y) not in self.pos:
                    self.press_left(x, y, b)
                else:
                    self.press_right(x, y, b)
                break

    def update(self, dt):
        self.update_blocks()

    def save_file(self, path, content):
        with open(path, 'w') as f:
            for x, y in content:
                f.write(str(x)+', '+str(y)+'\n')

    def on_key_press(self, key, m):
        k = symbol_string(key)
        print(k)
        if k == 'S':
            self.save_file('levelfile/level1.txt', self.pos)
            self.saveflag.element.text = '已保存'
        elif k == 'P':
            scenes = Scene(main.Start())
            director.replace(SplitColsTransition(scenes))

    def on_mouse_press(self, x, y, key, m):
        '''1是左键，4是右键，2是中键'''
        k = symbol_string(key)
        status = True
        if k == '1':
            self.mouse_press_left = status
        elif k == '4':
            print(2)
            self.mouse_press_right = status
        self.saveflag.element.text = '未保存'
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_release(self, x, y, key, m):
        k = symbol_string(key)
        status = False
        if k == '1':
            self.mouse_press_left = status
        elif k == '4':
            self.mouse_press_right = status
        self.mouse_x = 0
        self.mouse_y = 0


if __name__ == '__main__':
    director.init()
    director.run(Scene(Editor()))
