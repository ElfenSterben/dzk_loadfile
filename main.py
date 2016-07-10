# coding:utf-8

from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.director import director
from pyglet.window.key import symbol_string
from src.ball import Ball
from src.paddle import Paddle
from src.tools import collised
from src.level import Level
from src.hud import HUD
from cocos.scenes import SplitColsTransition
import editor


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
            self.remove(b)
        # 再初始化新的砖块
        self.level.reset()
        for b in self.level.blocks:
            self.add(b)

    def game_over(self):
        self.hud.death += 1
        scene = Scene(GameOver(self.hud))
        director.replace(scene)

    def update_hud(self):
        self.hud.update()

    def update_blocks(self):
        for b in self.level.blocks:
            if collised(b, self.ball.sprite):
                self.ball.hit()
                self.level.blocks.remove(b)
                self.remove(b)
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
                self.ball.speedx -= 0.1
            elif self.paddle.move_right:
                self.ball.speedx += 0.1
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
                scene = Scene(GuoCangDongHua(self.hud))
            else:
                scene = Scene(GameComplite(self.hud))
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
        label = Label('恭喜通关', font_size=42)
        label.position = (180, 300)
        label2 = Label('第' + str(levels) + '关  ' + '金币: ' + str(gold) + '  死亡次数: ' + str(death))
        label2.position = (230, 150)
        label3 = Label('按任意键从新开始')
        label3.position = (240, 120)
        self.add(label)
        self.add(label2)
        self.add(label3)

    def on_key_press(self, key, mi):
        scene = Scene(Start())
        director.replace(scene)


class GameOver(Layer):
    is_event_handler = True

    def __init__(self, hud):
        super(GameOver, self).__init__()
        self.hud = hud
        levels =self.hud.levels
        gold = self.hud.gold
        death = self.hud.death
        label = Label('游戏结束', font_size=42)
        label.position = (180, 300)
        label2 = Label('第' + str(levels) + '关  ' + '金币: ' + str(gold) + '  死亡次数: ' + str(death))
        label2.position = (230, 150)
        label3 = Label('按R键从第一关重新开始，按C键继续本关')
        label3.position = (180, 120)
        self.add(label)
        self.add(label2)
        self.add(label3)

    def on_key_press(self, key, mi):
        k = symbol_string(key)
        if (k == 'R') or (k == 'C'):
            if k == 'R':
                scene = Scene(GameLayer())
            elif k == 'C':
                print(1)
                scene = Scene(GameLayer(self.hud))
            director.replace(scene)


class GuoCangDongHua(Layer):
    is_event_handler = True

    def __init__(self, hud):
        super(GuoCangDongHua, self).__init__()
        self.hud = hud
        levels = self.hud.levels
        gold = self.hud.gold
        death = self.hud.death
        label = Label('第' + str(levels) + '关', font_size=42)
        label2 = Label('金币: ' + str(gold) + '  死亡次数: ' + str(death))
        label3 = Label('按任意键继续')
        label.position = (230, 300)
        label2.position = (230, 150)
        label3.position = (240, 100)
        self.add(label)
        self.add(label2)
        self.add(label3)

    def on_key_press(self, key, mi):
        scene = Scene(GameLayer(self.hud))
        director.replace(SplitColsTransition(scene))


class Start(Layer):
    '''开始界面'''
    is_event_handler = True

    def __init__(self):
        super(Start, self).__init__()
        label = Label('打砖块', font_size=42)
        label2 = Label('按下S开始,按下E键编辑关卡')
        label.position = (230, 300)
        label2.position = (240, 150)
        self.count = 0
        self.add(label)
        self.add(label2)
        self.schedule(self.update)

    def on_key_press(self, key, mi):
        k = symbol_string(key)
        print(k)
        if k == 'S':
            scenes = Scene(GuoCangDongHua(HUD()))
            director.replace(SplitColsTransition(scenes))
        elif k == 'E':
            scenes = Scene(editor.Editor())
            director.replace(SplitColsTransition(scenes))

    def update(self, dt):
        self.count += 1
        if self.count == 50:
            self.count = 0
            self.get_children()[1].visible = not self.get_children()[1].visible


if __name__ == '__main__':
    director.init()
    director.run(Scene(Start()))
