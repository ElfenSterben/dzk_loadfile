# coding:utf-8
from cocos.menu import *
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.director import director
from pyglet.window.key import symbol_string
from cocos.sprite import Sprite
from src.ball import Ball
from src.paddle import Paddle
from src.tools import collised
from src.level import Level
from src.hud import HUD
from cocos.scenes import SplitColsTransition
import editor


def create_scene(layer):
    return Scene(Background(), layer)

def font_set(size, color=(255, 255, 255, 150)):
     font_setting = {
        'font_size': size,
        'color': color,
        'font_name': 'Ubuntu Mono',
        'anchor_x': 'center',
        'anchor_y': 'center',
    }
     return font_setting


class GameLayer(Layer):
    is_event_handler = True

    def __init__(self, hud):
        super(GameLayer, self).__init__()
        # 添加板子和球
        self.paddle = Paddle('images/paddle.png')
        self.add(self.paddle.sprite)
        self.ball = Ball('images/ball.png')
        self.ball.reset_position = (320, self.paddle.sprite.height + self.ball.sprite.height / 2)
        self.add(self.ball.sprite)
        # hud 用于记录，更新关卡，死亡，金币数据
        self.hud = hud
        # 生成关卡
        self.level = Level()
        self.level.levels = self.hud.levels

        self.add(self.hud.gold_hud)
        self.add(self.hud.level_hud)
        self.add(self.hud.death_hud)

        # 添加按键状态
        self.key_pressed_left = False
        self.key_pressed_right = False
        self.key_pressed_up = False
        self.key_pressed_down = False

        self.reset()

        # 定期调用 self.update 函数
        # FPS frame per second 每秒帧数
        self.schedule(self.update)

    def reset(self):
        self.paddle.reset()
        self.ball.reset()
        # 清空界面上的block
        for b in self.level.blocks:
            self.remove(b.sprite)
        # 再初始化新的砖块
        self.level.reset()
        for b in self.level.blocks:
            self.add(b.sprite)

    def game_over(self):
        self.hud.death += 1
        scene = create_scene(GameOver(self.hud))
        director.replace(scene)

    def update_hud(self):
        self.hud.update()

    def update_blocks(self):
        for b in self.level.blocks:
            if collised(b.sprite, self.ball.sprite):
                self.ball.hit()
                b.live -= 1
                if b.live < 0:
                    self.level.blocks.remove(b)
                    self.remove(b.sprite)
                else:
                    b.reset()
                self.hud.gold += 1
                self.update_hud()
                print('金币:', self.hud.gold)
                break

    def update_ball(self):
        if self.ball.fired:
            self.ball.update()
        else:
            bx, by = self.ball.sprite.position
            px, py = self.paddle.sprite.position
            self.ball.sprite.position = (px, by)
        collide = collised(self.ball.sprite, self.paddle.sprite)
        if collide:
            if self.paddle.move_left:
                self.ball.speedx -= 0.5
            elif self.paddle.move_right:
                self.ball.speedx += 0.5
            self.ball.hit()
        if self.ball.dead():
            self.game_over()

    def update_paddle(self):
        self.paddle.update()

    def update_input(self):
        self.paddle.move_right = self.key_pressed_right
        self.paddle.move_left = self.key_pressed_left
        if self.key_pressed_up:
            self.ball.fire()

    def update_newlevel(self):
        if len(self.level.blocks) == 0:
            if self.level.next():
                print(self.level.levels)
                self.hud.levels += 1
                scene = create_scene(GuoCangDongHua(self.hud))
            else:
                scene = create_scene(GameComplite(self.hud))
            director.replace(scene)

    def update(self, dt):
        self.update_newlevel()
        self.update_ball()
        self.update_paddle()
        self.update_input()
        self.update_blocks()
        self.update_hud()

    def on_key_press(self, key, modifiers):
        k = symbol_string(key)
        status = True
        if k == 'LEFT':
            self.key_pressed_left = status
        elif k == 'RIGHT':
            self.key_pressed_right = status
        elif k == 'UP':
            self.key_pressed_up = status

    def on_key_release(self, key, modifiers):
        k = symbol_string(key)

        status = False
        if k == 'LEFT':
            self.key_pressed_left = status
        elif k == 'RIGHT':
            self.key_pressed_right = status
        elif k == 'UP':
            self.key_pressed_up = status


class GameComplite(Layer):
    is_event_handler = True

    def __init__(self, hud):
        super(GameComplite, self).__init__()
        self.hud = hud
        levels = self.hud.levels
        gold = self.hud.gold
        death = self.hud.death
        label = Label('Game Complete', **font_set(42))
        centerx = director.get_window_size()[0] / 2
        label.position = (centerx, 300)
        info = 'Level: ' + str(levels) + 'Gold: ' + str(gold) + '  Death: ' + str(death)
        label2 = Label(info, **font_set(22))
        label2.position = (centerx, 150)
        label3 = Label('press any key to continue', **font_set(18))
        label3.position = (centerx, 120)
        self.add(label)
        self.add(label2)
        self.add(label3)

    def on_key_press(self, key, mi):
        scene = create_scene(Start())
        director.replace(scene)


class GameOver(Layer):
    is_event_handler = True

    def __init__(self, hud):
        super(GameOver, self).__init__()
        self.hud = hud
        levels =self.hud.levels
        gold = self.hud.gold
        death = self.hud.death
        label = Label('Game Over', **font_set(42))
        centerx = director.get_window_size()[0] / 2
        label.position = (centerx, 300)
        info = 'Level: ' + str(levels) + '  Gold: ' + str(gold) + '  Death: ' + str(death)
        label2 = Label(info, **font_set(22))
        label2.position = (centerx, 150)
        label3 = Label('press R to restart, press C to continue', **font_set(18))
        label3.position = (centerx, 120)
        self.add(label)
        self.add(label2)
        self.add(label3)

    def on_key_press(self, key, mi):
        k = symbol_string(key)
        if (k == 'R') or (k == 'C'):
            if k == 'R':
                scene = create_scene(Start())
            elif k == 'C':
                scene = create_scene(GameLayer(self.hud))
            director.replace(scene)


class GuoCangDongHua(Layer):
    is_event_handler = True

    def __init__(self, hud):
        super(GuoCangDongHua, self).__init__()
        self.hud = hud
        levels = self.hud.levels
        gold = self.hud.gold
        death = self.hud.death
        ll = 'Level ' + str(levels)
        gdl = 'Gold: ' + str(gold) + ' Death: ' + str(death)
        color = (164, 164, 164, 200)
        label = Label(ll, **font_set(42, color))
        label2 = Label(gdl, **font_set(22, color))
        label3 = Label('press any key to continue', **font_set(18, color))

        centerx = director.get_window_size()[0]/2
        label.position = (centerx, 300)
        label2.position = (centerx, 200)
        label3.position = (centerx, 150)
        self.add(label)
        self.add(label2)
        self.add(label3)

    def on_key_press(self, key, mi):
        self.stop()
        scene = create_scene(GameLayer(self.hud))
        director.replace(SplitColsTransition(scene))

class Background(Layer):
    def __init__(self):
        super(Background, self).__init__()
        image = Sprite('images/back.jpg', anchor=(0, 0))
        window_size = director.get_window_size()
        width, height = window_size
        wscale = width / image.width
        hscale = height / image.height
        image.scale = max(wscale, hscale)
        self.add(image)


class Start(Menu):
    '''开始界面'''
    is_event_handler = True
    def __init__(self):
        super(Start, self).__init__()
        font_item = {'font_name': 'Ubuntu Mono', 'font_size': 42, 'color': (220,87, 18, 180)}
        font_item_selected = {'font_name': 'Ubuntu Mono', 'font_size': 60, 'color': (244, 208, 0, 180)}
        font_title ={
            'font_name': 'Arial',
            'font_size': 56,
            'color': (229, 131, 8, 200),
            'bold': True,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'dpi': 96,
            'x': 0, 'y': 0,
        }
        play = MenuItem('Play', self.on_play)
        editor = MenuItem('Edit Levels', self.on_editor)
        quit = MenuItem('Quit', self.on_quit)
        items = []
        items.append(play)
        items.append(editor)
        items.append(quit)
        self.title = 'Arkanoid'
        self.font_title = font_title
        self.font_item = font_item
        self.font_item_selected = font_item_selected
        self.create_menu(items, shake(), shake_back())

    def on_test(self):
        pass

    def on_quit(self):
        quit()

    def on_play(self):
        self.stop()
        scenes = create_scene(GuoCangDongHua(HUD()))
        director.replace(SplitColsTransition(scenes))

    def on_editor(self):
        self.stop()
        scenes = create_scene(editor.Editor())
        director.replace(SplitColsTransition(scenes))


if __name__ == '__main__':
    director.init()
    director.run(create_scene(Start()))
