from cocos.text import Label

class HUD(object):
    def __init__(self):
        super(HUD, self).__init__()
        self.levels = 1
        self.gold = 0
        self.death = 0
        self.gold_hud = Label('Gold: ' + str(self.gold), position=(0, 460))
        self.level_hud = Label('Level: ' + str(self.levels), position=(80, 460))
        self.death_hud = Label('Death: ' + str(self.death), position=(160, 460))

    def update(self):
        self.gold_hud.element.text = 'Gold: ' + str(self.gold)
        self.level_hud.element.text = 'Level: ' + str(self.levels)
        self.death_hud.element.text = 'Death: ' + str(self.death)

