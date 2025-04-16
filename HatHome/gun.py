import pygame as pg
vec = pg.math.Vector2
from settings import *
import random


class Gun(pg.sprite.Sprite):
    def __init__(self, game, d):
        self.groups = game.all_sprites, game.weapons, game.layer_yes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.d = d
        if d['is'] == 'wavax':
            self.energymax = d['energy']
            self.energy = d['energy']
            self.consum = d['energy_consum']
        self.image = d['bank_image'][0]
        self.image_old = self.image
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.real_rect.center = vec(0,0)
        self.pos = self.real_rect.center
        self.last_shot = 0
        self.cd = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.move()
        if not self.game.player.inventory.display:
            self.fire()

    def move(self):
        self.vector_calcul()
        if ((self.rot < -90) or (self.rot > 90)):
            self.image_old = self.d['bank_image'][1].copy()
            if self.d['is'] == 'wavax':
                self.image_old.blit(self.battery(self.d['start'], self.d['end'], self.d['bank_image'][3].copy()), (self.d['start'] , 0))
        else:
            self.image_old = self.d['bank_image'][0].copy()
            if self.d['is'] == 'wavax':
                self.image_old.blit(self.battery(self.d['start'], self.d['end'], self.d['bank_image'][2].copy()), (self.d['start'] , 0))

        if self.d['is'] == 'wavax':
            self.real_rect.center = (self.game.player.real_rect.center ) + self.levecteur + vec(self.width/2, self.height/2) + self.vecvec
        else:
            self.real_rect.center = (self.game.player.real_rect.center ) + self.levecteur + vec(self.width/2, self.height/2) + self.vecvec
        self.image = pg.transform.rotate(self.image_old, self.rot)
        self.pos = self.real_rect.center

    def vector_calcul(self):
        self.gun_vector = self.game.mousepos - vec(self.game.width/2, self.game.height/2)
        if self.gun_vector != vec(0,0):
            self.vecvec = self.gun_vector.normalize()*self.d['distance']
        else:
            self.vecvec = vec(1,0)*self.d['distance']
        self.rot = self.gun_vector.angle_to(vec(1, 0))
        self.levecteur = vec(-(self.image.get_width()/2),-(self.image.get_height()/2))

    def battery(self, start_x, end_x, image_empty):
            length = end_x-start_x
            self.image_child = image_empty.subsurface(start_x, 0, length, self.image_old.get_height())
            self.widthempty = int((self.energy / self.d['energy']) * length)
            self.newwidthempty = length/2 - (self.widthempty - length/2)
            self.image_understand = self.image_child.subsurface(0, 0, self.newwidthempty , self.image_old.get_height())
            return self.image_understand

    def fire(self):
        if self.d['is'] == 'aspirator' and self.game.mousepress[0]:
            self.vrombissement()
            for coin in self.game.coins:
                self.cointoplayer = coin.pos - self.game.player.pos
                self.coinrot = self.cointoplayer.angle_to(vec(1, 0))
                if self.rot < -140:
                    condition = self.coinrot < self.rot + 40 or self.coinrot > self.rot + 320
                elif self.rot > 140:
                    condition = self.coinrot > self.rot - 40 or self.coinrot < self.rot - 320
                else:
                    condition = self.rot - 40 < self.coinrot < self.rot + 40
                if self.cointoplayer.length() < ASPIRATOR_RANGE and condition:
                    if not coin.beingapsiratored:
                        coin.beingapsiratored = True
                        coin.image = pg.transform.rotate(coin.image_old, coin.x*int(random.randrange(20, 40, 1)))
                    self.cointogun = coin.pos - (self.game.player.pos + self.vecvec.normalize() * self.rect.width * PATCHW)
                    self.cointogun.y *= 0.5/PATCHW
                    mult = self.cointogun.length()
                    if mult>50:
                        mult = 50
                    coin.real_rect.center -= self.cointogun.normalize() * (ASPIRATOR_SPEED / mult)

        elif self.d['is'] == 'wavax' and self.game.mousepress[0] and self.energy - self.consum > 0:
            self.energy -= self.consum
            if self.energy - self.consum > 0:
                self.vrombissement()
                now = pg.time.get_ticks()
                if now - self.last_shot > self.d['bullet_fire_cooldown']:
                    self.last_shot = now
                    dir = vec(1, 0).rotate(-self.rot)
                    pos = (self.game.player.pos) + (dir * self.d['fire_distance'])
                    Bullet(self.game, pos, self.d)

        elif self.d['is'] == 'wavax' and self.energy <= self.energymax:
            self.energy += self.consum

        elif self.d['is'] == 'gold45' and self.game.mousepress[0]:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.d['bullet_fire_cooldown']:
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = (self.game.player.pos) + (dir * self.d['fire_distance'])
                Bullet(self.game, pos, self.d)
                self.recul()

    def vrombissement(self):
        self.real_rect.centerx += int(random.randrange(0, 5, 1))
        self.real_rect.centery += int(random.randrange(0, 5, 1))

    def recul(self):
        pass

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, d):
        self.groups = game.all_sprites, game.bullets, game.layer_yes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.d = d
        if self.d['is'] == 'wavax':
            self.image = d['bank_image'][4]
        else:
            self.image = d['bank_image'][4]
        self.image_old = self.image
        self.rect = self.image.get_rect()
        self.real_rect = self.rect
        self.real_rect.center = pos
        self.pos = vec(self.real_rect.center)
        self.vector = self.game.player.gun.gun_vector
        self.rot = self.vector.angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.image_old, self.rot)
        self.vel = self.game.player.gun.vecvec * d['bullet_speed']
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.collide()
        self.pos += self.vel * self.game.dt
        self.real_rect.center = self.pos
        if pg.time.get_ticks() - self.spawn_time > self.d['bullet_life_time']:
            self.kill()

    def collide(self):
        if pg.sprite.spritecollideany(self, self.game.walls) or pg.sprite.spritecollideany(self, self.game.ships):
            self.kill()
        hits = pg.sprite.groupcollide(self.game.globuzars, self.game.bullets, False, True)
        for hit in hits:
            hit.vel -= hit.vel/self.d['bullet_repel']
            hit.life -= self.d['bullet_damage']
            hit.aware = 5000*PATCHW

gold45 = {'distance' : 30*PATCHW,
               'bullet_speed' : 90*PATCHW,
               'bullet_life_time' : 2000,
               'bullet_fire_cooldown' : 500,
               'bullet_damage' : 50,
               'fire_distance' : 75*PATCHW,
               'gold45' : True,
               'recul_distance' : 50,
               'bullet_repel' : 1.5*PATCHW,
               'is' : 'gold45'}

wavax = {'distance' : 30*PATCHW,
               'bullet_speed' : 60*PATCHW,
               'bullet_life_time' : 2000,
               'bullet_fire_cooldown' : 10,
               'bullet_damage' : 10,
               'fire_distance' : 67*PATCHW,
               'bullet_repel' : 1.5,
               'energy' : 100,
               'energy_consum' : 1,
               'start' : 3*PATCHW,
               'end' : 40*PATCHW,
               'is' : 'wavax'}

aspirator = {'distance' : 45*PATCHW,
               'start' : 8*PATCHW,
               'end' : 131*PATCHW,
               'is' : 'aspirator',
               'mult' : 1}
