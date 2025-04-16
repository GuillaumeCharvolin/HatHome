import pygame as pg
from settings import *
vec = pg.math.Vector2

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.ground_image_bank
        self.image = self.image_bank[0]
        self.rect = self.image.get_rect() #
        self.real_rect = self.image.get_rect() #
        self.x = x
        self.y = y
        self.real_rect.x = x * TILESIZE #
        self.real_rect.y = y * TILESIZE #

'''
class Groundmap(pg.sprite.Sprite)
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.grounds
        pg.sprite.Sprite.__init__(self, self.grounds)
        self.game = game
'''

class Vegetation(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.vegetation_image_bank
        self.image = self.image_bank[0]
        self.rect = self.image.get_rect()
        self.real_rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.real_rect.x = x * TILESIZE + random.randint(1,50)
        self.real_rect.y = y * TILESIZE + random.randint(1,50)
