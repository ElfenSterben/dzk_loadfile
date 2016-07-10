from cocos.text import Label

class HUD(object):
    def __init__(self):
        super(HUD, self).__init__()
        self.levels = 1
        self.gold = 0
        self.death = 0
        self.gold_hud = Label('金币: ' + str(self.gold), position=(0, 460))
        self.level_hud = Label('关卡: ' + str(self.levels), position=(80, 460))
        self.death_hud = Label('死亡: ' + str(self.death), position=(160, 460))

    def update(self):
        self.gold_hud.element.text = '金币: ' + str(self.gold)
        self.level_hud.element.text = '关卡: ' + str(self.levels)
        self.death_hud.element.text = '死亡: ' + str(self.death)

