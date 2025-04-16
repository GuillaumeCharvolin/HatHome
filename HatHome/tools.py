import pygame as pg
from settings import *
from tilemap import collide_hit_rect

class Tools:
    def collide(sprite, group, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            for hit in hits:
                if sprite.hit_rect.centerx < hit.real_rect.centerx:
                    sprite.pos.x = hit.real_rect.left - sprite.hit_rect.width / 2
                if sprite.hit_rect.centerx > hit.real_rect.centerx:
                    sprite.pos.x = hit.real_rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
                hit.beattack(sprite)

        if dir == 'y':
            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
            for hit in hits:
                if sprite.hit_rect.centery < hit.real_rect.centery:
                    sprite.pos.y = hit.real_rect.top - sprite.hit_rect.height / 2
                if sprite.hit_rect.centery > hit.real_rect.centery:
                    sprite.pos.y = hit.real_rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                hit.beattack(sprite)

    def number_translate(number, bank):
        if number < 0:
            return bank[0]
        else:
            number_str = str(number)
            image = pg.Surface((len(number_str)*bank[0].get_width(),bank[0].get_height()), pg.SRCALPHA)
            image.set_alpha(0)
            for i in enumerate(number_str):
                image.blit(bank[int(i[1])],(i[0]*bank[0].get_width(), 0))
            return image

    def letter_translate(str, bank):
        alph = "abcdefghijklmnopqrstuvwxyz :+-"
        number = []
        for letter in str:
            for let in alph:
                if letter == let:
                    number.append(alph.index(let))
        image = pg.Surface((len(str)*bank[0].get_width(),bank[0].get_height()), pg.SRCALPHA)
        image.set_alpha(0)
        for i in enumerate(number):
            image.blit(bank[int(i[1])],(i[0]*bank[0].get_width(), 0))
        return image

class Button():
    def __init__(self, game, img_false, img_true, coord):
        self.game = game
        self.image = img_false
        self.rect = self.image.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]
        self.image_true = img_true   #white image
        self.image_false = img_false  #grey
        self.time = 0

    def action(self):
        self.game.window.blit(self.image, (self.rect.x, self.rect.y))
        if self.time < BUTTON_SPACE_CLICK:
            self.time +=1
        if self.rect.colliderect(self.game.mouse):
            self.image = self.image_true.copy()
            if self.game.mousepress[0] and self.time >= BUTTON_SPACE_CLICK:
                self.time = 0
                return True

        else:
            self.image = self.image_false.copy()
