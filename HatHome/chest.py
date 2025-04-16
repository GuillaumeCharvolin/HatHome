import pygame as pg
from settings import *
from random import *
from math import *

class Chest(pg.sprite.Sprite):
    def __init__(self, game, mobpos):
        self.groups = game.all_sprites, game.chests, game.collidewithplayer, game.collidewithmobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.chest_image_bank
        self.image = self.image_bank[0]
        self.image_old = self.image
        self.pos = mobpos
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.real_rect.center = self.pos

    def update(self):
        self.real_rect.center = self.pos

class Coin(pg.sprite.Sprite):

    def __init__(self, game, mobpos):
        self.groups = game.all_sprites, game.coins, game.layer_yes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.coins_image_bank #image
        self.image = self.image_bank[0]
        self.image_old = self.image
        self.pos = mobpos
        self.pos.x -= 20*PATCHW
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.real_rect.center = self.pos
        self.old_real_rect = self.real_rect.copy()
        self.x = 0
        self.x2 = 0
        self.beingapsiratored = False
        self.oldy2 = self.real_rect.centery

        self.done = False

        self.side = randrange(-1, 2, 2)
        if self.side == 1:
            self.rect.centerx += 55     #si la pièce part a droite, alors on la fait partir de la droite du mob (comme ca meme distance parcouru a droite et a gauche)

        self.g = 10
        self.speed = 43 + randint(-3 ,3)
        self.angle =  (75 + randint(-5, 5)) * 3.14 / 180


        #self.old_real_rect.centery -= ((self.x-55)**2 * 0.04)
        self.oldy = self.real_rect.centery
    def collide_player(self):
        if (self.pos - self.game.player.pos).length() < 100*PATCHW:
            self.game.player.coins += 1
            self.kill()

    def update(self):
        if self.real_rect.centery <= self.oldy and not self.done and not self.beingapsiratored:
            self.real_rect.centerx += 3 * self.side
            self.real_rect.centery = -(-(self.g/(2*self.speed**2*cos(self.angle)**2)) * self.x ** 2 + tan(self.angle) * self.x) + self.oldy
            self.image = pg.transform.rotate(self.image_old, self.x*int(randrange(20, 40, 1)))
            self.x += 3
            self.oldy2 = self.real_rect.centery


        elif self.real_rect.centery <= self.oldy2 and not(self.beingapsiratored):
            self.done = True
            self.real_rect.centerx += 2 * self.side
            self.real_rect.centery = -(-(self.g/(2*(self.speed/2)**2*cos(self.angle)**2)) * self.x2 ** 2 + tan(self.angle) * self.x2) + self.oldy2
            self.x2 += 2
        self.pos = self.real_rect.center
        self.collide_player()
