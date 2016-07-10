from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.director import director
from cocos.sprite import Sprite
from pyglet.window.key import symbol_string
from cocos.scenes import SplitColsTransition
from cocos.rect import Rect
from src.level import Level
import glob
# import main
import os


class Editor(Layer):
    is_event_handler = True

    def __init__(self):
        super(Editor, self).__init__()
        label = Label('关卡编辑器', position=(0, 0))
        label2 = Label('按S键保存', position=(200, 0))
        self.new_level_label = Label('新建关卡', position=(20, 50))
        self.delete_level_label = Label('删除当前关卡', position=(100, 50))
        self.saveflag = Label('未保存', position=(300, 0))
        self.edit_level = Label('当前编辑关卡: ', position=(400, 0))
        self.yes_label = Label('是', position=(280, 50))
        self.no_label = Label('否', position=(320, 50))
        self.yes_label.visible = False
        self.no_label.visible = False
        self.block_image_path = 'images/smallblock.png'
        # 编辑区属性
        self.editor_bottom = 250
        self.editor_top = 450
        self.editor_left = 0
        self.editor_right = 640

        # 以下两个标签用于提示用户编辑窗的位置
        buttom = self.editor_bottom - 1
        top = self.editor_top + 1
        line1 = Sprite('images/line.png', position=(0, buttom), anchor=(0, 0))
        line2 = Sprite('images/line.png', position=(0, top), anchor=(0, 0))

        self.add(label)
        self.add(label2)
        self.add(self.saveflag)
        self.add(line1)
        self.add(line2)
        self.add(self.edit_level)
        self.add(self.new_level_label)
        self.add(self.delete_level_label)
        self.add(self.yes_label)
        self.add(self.no_label)

        # 鼠标按下标志和坐标
        self.mouse_press_left = False
        self.mouse_press_right = False
        self.mouse_x = 0
        self.mouse_y = 0

        # 生成砖块可以添加的位置
        self.recttmp = []
        self.create_grid()
        # 存储坐标
        self.pos = []
        # 存储bloks
        self.blocks = []

        # 存储关卡选择
        self.save_as = 1
        self.page = 1
        self.page_count = 1
        self.page_is_pressing = False
        self.delete_is_press = False
        self.level_select = []
        self.level_select_position = []
        self.page_select = []

        self.create_level_select()
        self.create_page_select()

        self.reset_blocks()

        self.schedule(self.update)

    def create_grid(self):
        b = Sprite(self.block_image_path)
        ewidth = self.editor_right - self.editor_left
        left = int(self.editor_left + ewidth % b.width / 2)
        right = self.editor_right
        top = self.editor_top
        bottom = self.editor_bottom
        for x in range(left, right, b.width):
            for y in range(bottom, top, b.height):
                self.recttmp.append(Rect(x, y, b.width, b.height))

    def get_all_level(self):
        '''获取已存在的关卡'''
        files = glob.glob('levelfile/*.txt')
        levels = []
        for f in files:
            level = f.split('level')[-1].split('.')[0]
            if level.isdigit():
                levels.append(int(level))
        levels.sort()
        return levels

    def create_level_select(self):
        '''创建关卡选择器'''
        levels = self.get_all_level()
        count_pre_pages = 10
        for i in range(0, len(levels)):
            page = i // count_pre_pages
            if i % 10 < 5:
                offect_y = 200
            else:
                offect_y = 150
            # 每一排5个选择 所以用 数量 i 除以 5 取余
            offect_x = 640 * page + 40 + (i % 5) * 120
            label = Label('第' + str(i + 1) + '关', position=(offect_x, offect_y))
            self.add(label)
            # 40,20 宽度和高度是试验出来的
            r = Rect(label.x, label.y, 40, 20)
            self.level_select.append([r, label])
            self.level_select_position.append((label.x, label.y))

    def create_page_select(self):
        '''创建关卡选择的页面选择器'''
        levels = self.get_all_level()
        count_pre_pages = 10
        pages = len(levels) // count_pre_pages + 1
        self.page_count = pages
        last_page = Label('上一页')
        next_page = Label('下一页')
        y = 100
        lx = 320 - 54
        nx = 320 + 10
        for i in range(pages):
            # 从中间开始放页码
            if i < pages / 2:
                x = 320 - (pages / 2 - i) * 20
                lx = 320 - pages / 2 * 20 - 64
            else:
                x = 320 + (i - pages / 2) * 20
                nx = 320 + pages / 2 * 20 + 10
            label = Label(str(i + 1), position=(x, y))
            last_page.position = (lx, y)
            next_page.position = (nx, y)
            r = Rect(label.x, label.y, 10, 16)
            self.page_select.append([r, label])
            self.add(label)

        lr = Rect(last_page.x, last_page.y, 50, 20)
        nr = Rect(next_page.x, next_page.y, 50, 20)
        self.page_select.append([lr, last_page])
        self.page_select.append([nr, next_page])
        self.add(last_page)
        self.add(next_page)

    def reset_level_select(self):
        for r, l in self.level_select:
            self.remove(l)
        for r, l in self.page_select:
            self.remove(l)
        self.level_select.clear()
        self.page_select.clear()
        self.level_select_position.clear()
        self.create_level_select()
        self.create_page_select()

    def update_page(self):
        for i in range(len(self.level_select)):
            r, l = self.level_select[i]
            sx, sy = self.level_select_position[i]
            x = sx - (self.page - 1) * 640
            r.position = (x, sy)
            l.position = (x, sy)

    def select_page(self, x, y):
        if not self.page_is_pressing:
            self.page_is_pressing = True
            for r, l in self.page_select:
                if r.contains(x, y):
                    text = l.element.text
                    if text == '下一页':
                        self.page += 1
                    elif text == '上一页':
                        self.page -= 1
                    else:
                        page = int(text)
                        self.page = page
                    if self.page < 1:
                        self.page = 1
                    elif self.page > self.page_count:
                        self.page = self.page_count

    def create_new_level(self):
        levels = self.get_all_level()
        if len(levels) == max(levels):
            self.save_as = max(levels) + 1
        else:
            for l in range(1, len(levels) + 1):
                if l not in levels:
                    self.save_as = l
        self.reset_blocks()

    def new_level(self, x, y):
        r = Rect(self.new_level_label.x, self.new_level_label.y, 70, 20)
        if r.contains(x, y):
            self.create_new_level()

    def delete_level(self, x, y):
        r = Rect(self.delete_level_label.x, self.delete_level_label.y, 130, 20)
        if r.contains(x, y):
            status = True
            self.yes_label.visible = status
            self.no_label.visible = status
            self.delete_is_press = status
        if self.delete_is_press:
            yes = Rect(self.yes_label.x, self.yes_label.y, 15, 20)
            no = Rect(self.no_label.x, self.no_label.y, 15, 20)
            status = False
            if yes.contains(x, y):
                path = 'levelfile/level'+str(self.save_as)+'.txt'
                if os.path.exists(path):
                    os.remove(path)
                self.save_as = self.get_all_level()[-1]
                self.yes_label.visible = status
                self.no_label.visible = status
                self.delete_is_press = status
                self.reset_blocks()
                self.reset_level_select()
            elif no.contains(x, y):
                self.delete_is_press = status
                self.yes_label.visible = status
                self.no_label.visible = status

    def reset_blocks(self):
        level = Level()
        level.levels = self.save_as

        # 通过文件生成块
        level.reset()
        # 删除已存在的块
        for b in self.blocks:
            self.remove(b)

        # 清空存储的块和坐标
        self.blocks.clear()
        self.pos.clear()

        # 添加新的块
        for b in level.blocks:
            self.add(b)
            self.blocks.append(b)
        # 添加新的坐标
        for pos in level.blocks_pos:
            self.pos.append(pos)

    def select_level(self, x, y):
        for r, l in self.level_select:
            if r.contains(x, y):
                level = int(l.element.text[1:][:-1])
                self.save_as = level
                self.reset_blocks()

    def add_block(self, x, y):
        b = Sprite(self.block_image_path, anchor=(0, 0))
        for r in self.recttmp:
            if r.contains(x, y) and (r.position not in self.pos):
                b.position = r.position
                self.add(b)
                self.blocks.append(b)
                self.pos.append(r.position)
                break

    def delete_block(self, x, y):
        for b in self.blocks:
            r = b.get_rect()
            if r.contains(x, y) and (r.position in self.pos):
                self.blocks.remove(b)
                self.remove(b)
                self.pos.remove(r.position)
                break

    def update_input(self):
        x = self.mouse_x
        y = self.mouse_y
        if self.mouse_press_left:
            self.add_block(x, y)
            self.select_level(x, y)
            self.select_page(x, y)
            self.new_level(x, y)
            self.delete_level(x, y)
        elif self.mouse_press_right:
            self.delete_block(x, y)

    def update(self, dt):
        self.update_input()
        self.update_page()
        self.edit_level.element.text = '当前编辑关卡: ' + str(self.save_as)

    def save_file(self, path, content):
        with open(path, 'w') as f:
            for x, y in content:
                f.write(str(int(x))+', '+str(int(y))+'\n')
        self.reset_level_select()

    def on_key_press(self, key, m):
        k = symbol_string(key)
        if k == 'S':        # 按S键保存
            self.save_file('levelfile/level'+str(self.save_as)+'.txt', self.pos)
            self.reset_level_select()
            self.saveflag.element.text = '已保存'
        elif k == 'P':      # 按P键开始游戏
            scenes = Scene(main.Start())
            director.replace(SplitColsTransition(scenes))

    def on_mouse_press(self, x, y, key, m):
        '''1是左键，4是右键，2是中键'''
        k = symbol_string(key)
        status = True
        if k == '1':
            self.mouse_press_left = status
        elif k == '4':
            self.mouse_press_right = status
        self.saveflag.element.text = '未保存'
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_release(self, x, y, key, m):
        k = symbol_string(key)
        status = False
        if k == '1':

            self.page_is_pressing = status
            self.mouse_press_left = status
        elif k == '4':
            self.mouse_press_right = status


# class MYTest(Layer):
#     def __init__(self):
#         super(MYTest, self).__init__()
#         label = Label('test', position=(300, 200))
#         self.add(label)
#         b = Sprite('images/block.png', anchor=(0, 0))
#         b.position = (448, 390)
#         self.add(b)
#         self.schedule(self.update)
#     def update(self, st):
#         pass

if __name__ == '__main__':
    director.init()
    director.run(Scene(Editor()))

