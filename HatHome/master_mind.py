import pygame as pg
from settings import *
from random import *
from inventory import *
from globuzar import *

class Master_Mind():
    def __init__(self, game):
        self.game = game
        WC = game.map.width/2
        WR = game.map.width
        HC = game.map.height/2
        HD = game.map.height
        self.waveacupdate = WAVEACUPDATE
        self.west = (0, HC)
        self.nordwest = (0, 0)
        self.nord = (WC, 0)
        self.nordest = (WR, 0)
        self.est = (WR, HC)
        self.sudest = (WR, HD)
        self.sud = (WC, HD)
        self.sudwest = (0, HD)

        self.time = 0
        self.waves = []
        self.warning = False
        self.game.wavelaunch_stat = False
        self.warning_time_stat = False
        self.warning_timer = 10

        self.sonar = Sonar(self.game)
        self.new()

    def new(self):
        data = [Group(0, 4, self.west, 0), #Time since wave start, Number of mob, Spawnpoint, Type of mob
                ]
        Waves(self.game, data, self.waves)

        """
        Group(3, 3, self.nordwest, 0),
        Group(6, 3, self.nord, 0),
        Group(9, 3, self.nordest, 0),
        Group(12, 3, self.est, 0),
        Group(15, 3, self.sudest, 0),
        Group(18, 3, self.sud, 0),
        Group(21, 3, self.sudwest, 0)
        """

        data = [Group(0, 4, self.west, 0),
                Group(3, 3, self.nordwest, 0),
                Group(6, 3, self.nord, 0),
                Group(9, 3, self.nordest, 0),
                Group(12, 3, self.est, 0),
                Group(15, 3, self.sudest, 0),
                Group(18, 3, self.sud, 0),
                Group(21, 3, self.sudwest, 0)]
        Waves(self.game, data, self.waves)

    def update(self):
        self.time += self.game.dt
        self.time_image = Tools.number_translate(int(self.time), self.game.numbersx2)

        if self.waveacupdate+1 != len(self.game.master_mind.waves) and \
        self.game.wavelaunch_stat and self.waves[self.waveacupdate].totalofmob <= self.game.player.countmob:
            self.waveacupdate +=1

        if self.game.wavelaunch_stat and not self.waves[self.waveacupdate].launch:
            self.warning_time_stat = True
            self.warning = True

        if self.warning_time_stat:
            self.warning_timer -= self.game.dt
        else:
            self.warning_timer = 10

        if self.warning_timer <= 0:
            self.warning_timer = 10
            self.warning_time_stat = False
            self.warning = False
            self.time = 0
            self.game.player.countmob = 0
            self.waves[self.waveacupdate].launch = True

        if self.waves[self.waveacupdate].launch:
            self.waves[self.waveacupdate].update()



        if self.warning:
            self.warn_number = Tools.number_translate((int(self.warning_timer+1)), self.game.numbersx4)
            self.warn_message = Tools.letter_translate(("warning wave incoming in :"), self.game.lettersx4)

    def draw(self):
        self.game.window.blit(self.time_image, (CLOCK_X, CLOCK_Y))
        self.sonar.draw()
        if self.warning:
            self.game.window.blit(self.warn_message, (30, 50))
            self.game.window.blit(self.warn_number, (30+self.warn_message.get_width(), 50))
class Waves():
    def __init__(self, game, data, waves):
        self.game = game
        self.waves = waves
        waves.append(self)
        self.num = self.waves.index(self)
        self.launch = False
        self.groups = data
        self.totalofmob = 0

        for group in self.groups:
            self.totalofmob += group.mob

    def update(self):
        self.time = self.game.master_mind.time
        for group in self.groups:
            if group.launch:
                if group.start <= self.time:
                    for i in range(0, group.mob):
                        Globuzar(self.game, group.posx, group.posy)
                    group.launch = False
        if self.totalofmob <= self.game.player.countmob:
            self.launch = False

class Group():
    def __init__(self, start, mob, pos, type):
        self.start = start
        self.mob = mob
        self.posx = pos[0]
        self.posy = pos[1]
        self.launch = True
        self.type = type

class Sonar(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.collidewithplayer, game.collidewithglobuzars, game.sonars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.sonar_image_bank
        self.image = self.image_bank[0]
        self.rect = self.image.get_rect()
        self.real_rect = self.image.get_rect()
        self.hit_rect = self.real_rect
        self.real_rect.x = SONAR_X
        self.real_rect.y = SONAR_Y
        self.pos = vec(SONAR_X, SONAR_Y)
        self.real_rect.center = self.pos
        self.drawsonartext = False
        self.sonartext = Tools.letter_translate("press e to launch a new wave", self.game.lettersx2)


    def update(self):
        if (self.pos - self.game.player.pos).length() < 300:
            self.drawsonartext = True
            if self.game.player.keys[pg.K_e]:
                self.game.wavelaunch_stat = True
        else:
            self.game.wavelaunch_stat = False
            self.drawsonartext = False

    def draw(self):
        self.image = self.image_bank[0]
        if self.drawsonartext and not self.game.master_mind.warning and not self.game.master_mind.waves[self.game.master_mind.waveacupdate].launch:
            self.game.window.blit(self.sonartext, (SONARTEXT_X, SONARTEXT_Y))
        if self.game.master_mind.waves[self.game.master_mind.waveacupdate].launch or self.game.master_mind.warning:
            self.image = self.image_bank[1]

    def beattack(self, mob):
        pass
