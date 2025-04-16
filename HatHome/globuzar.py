import pygame as pg
from settings import *
from chest import *
vec = pg.math.Vector2
from math import hypot
from tilemap import collide_hit_rect
from random import *
from tools import *

class Globuzar(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.timer = 0
        self.groups = game.all_sprites, game.globuzars, game.layer_yes
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.bank_image = game.globu_img_bank
        self.image = self.bank_image[0]
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.hit_rect = self.real_rect.copy()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.real_rect.center = self.pos
        self.damage = GLOBUZAR_DAMAGE
        self.life = GLOBU_LIFE
        self.max_life = GLOBU_LIFE
        self.aware = GLOBUZAR_AWARE
        self.wallattack = GLOBUZAR_WALL_ATTACK
        self.bar = Globuzar.Bar(self, self.game)
        self.collideentity = 0
        self.rot = 0

    def footupdate(self):
        self.timer += 1
        if self.timer <=5:
            self.moovestat = 0
        elif self.timer <= 11 :
            self.moovestat = 1
        else:
            self.timer = 0

    def get_dir(self): #equivalent --> get_mouse() de plpayer
        if self.rot <= -135: #left down
            self.image = self.bank_image[12+self.moovestat]
        elif self.rot <= -90: #Down
            self.image = self.bank_image[14+self.moovestat]
        elif self.rot <= -45: #right down
            self.image = self.bank_image[0+self.moovestat]
        elif self.rot <= 0: #Right
            self.image = self.bank_image[2+self.moovestat]
        elif self.rot <= 45: #Top right
            self.image = self.bank_image[4+self.moovestat]
        elif self.rot <= 90:#Top
            self.image = self.bank_image[6+self.moovestat]
        elif self.rot <= 135:#Top left
            self.image = self.bank_image[8+self.moovestat]
        else: #left
            self.image = self.bank_image[10+self.moovestat]

    def update(self):
        self.distancewithplayer = vec(self.game.player.pos - self.pos).length()
        if self.life <= 0:
            for i in range(randint(COINS_DROP_MIN,COINS_DROP_MAX)):
                Coin(self.game, self.pos)
            i = randint(EXPERIENCE_DROP_MIN,EXPERIENCE_DROP_MAX)
            self.game.player.experience += i
            self.game.player.experience_update()
            self.game.player.countmob += 1
            self.kill()
            self.bar.kill()
        else:
            if self.distancewithplayer < self.aware:
                self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))

            else :
                self.rot = (self.game.ship.pos - self.pos).angle_to(vec(1, 0))
            self.footupdate()
            self.get_dir()
            self.real_rect.center = self.pos
            self.acc = vec(GLOBU_SPEED, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.move_collide()

    def move_collide(self):
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.globuzars_with_globuzars()
        self.globuzars_with_player()
        self.hit_rect.centery = self.pos.y
        Tools.collide(self, self.game.collidewithglobuzars, 'y')
        self.hit_rect.centerx = self.pos.x
        Tools.collide(self, self.game.collidewithglobuzars, 'x')
        self.real_rect.center = self.hit_rect.center

    def globuzars_with_globuzars(self):
        for mob in self.game.globuzars:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < 50*PATCHW:
                    self.pos += dist.normalize()*2

    def globuzars_with_player(self):
        dist = self.pos - self.game.player.pos
        if 0 < dist.length() < 50:
            self.game.player.beattack(self)

    class Bar(pg.sprite.Sprite):
        def __init__(self, globuzar, game):
            self.groups = game.all_sprites, game.layer_bar
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.col = (0,0,255)
            self.mob = globuzar
            self.image_bank = self.game.globu_bar
            self.real_rect = self.image_bank[0].get_rect()
            self.rect = self.real_rect
            self.image = pg.Surface((self.image_bank[0].get_width(), self.image_bank[0].get_height()))

        def update(self):
            h = (self.mob.life / self.mob.max_life) * self.image_bank[0].get_width()
            if h<0:
                h = 0
            start = (self.image_bank[0].copy()).subsurface((0,0, h, self.image_bank[0].get_height()))
            self.image.blit(start, (0, 0))
            end = (self.image_bank[1].copy()).subsurface((h, 0, self.image_bank[0].get_width()-h, self.image_bank[0].get_height()))
            self.image.blit(end, (h, 0))
            self.real_rect.x = self.mob.real_rect.x
            self.real_rect.y = self.mob.real_rect.y - 12 * PATCHH
