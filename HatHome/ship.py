import pygame as pg
from settings import *
vec = pg.math.Vector2
from math import *

class Ship(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.ships, game.collidewithplayer, game.collidewithglobuzars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.ship_image_bank
        self.buttonwave_bank = game.ship_image_buttonwave_bank
        self.image = self.image_bank[0].copy()
        self.rect = self.image.get_rect()
        self.real_rect = self.image.get_rect()
        self.hit_rect = self.real_rect
        self.real_rect.x = SHIP_X
        self.real_rect.y = SHIP_Y
        self.max_life = SHIP_MAX_LIFE
        self.life = SHIP_LIFE
        self.pos = vec(SHIP_X, SHIP_Y)
        self.real_rect.center = self.pos
    '''
    def detect(self):
        if (self.pos - self.game.player.pos).length() < 100:
            self.detectstat = True
            self.moovestat += 4
        else:
            self.detectstat = False
    '''
    def update(self):
        #self.detect()
        h = (self.life / self.max_life) * self.image_bank[1].get_height()
        if h<=0:
            h=0
        self.image = self.image_bank[0].copy()
        empty = (self.image_bank[1].copy()).subsurface((0,0, self.image_bank[1].get_width(), self.image_bank[1].get_height()-h))
        self.image.blit(empty, (0, 0))

    def beattack(self, mob):
        self.life -= mob.wallattack
