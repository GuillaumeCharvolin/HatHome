import pygame as pg
from settings import *
vec = pg.math.Vector2


class Dealer(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.all_sprites, game.dealers, game.layer_yes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.bank_image = game.dealer_img_bank
        self.image = self.bank_image[0]
        self.pos = vec(DEALER_X, DEALER_Y)
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.hit_rect = self.real_rect.copy()
        self.real_rect.center = self.pos
        self.right = True
        self.moovestat = 0
        self.timer = 0
        self.count_walk = 0
        self.detectstat = False

        #shop
        #self.sellingitemprimary = ['Wavax', 'Gold45' ]


    def update(self):
        self.footupdate()
        self.detect()
        if self.count_walk == 25:
            self.count_walk = 0
            if self.right:
                self.right = False
            else:
                self.right = True

        if self.right:
            self.image = self.bank_image[2+self.moovestat]
            self.pos.x +=1
            self.count_walk +=1
        else:
            self.image = self.bank_image[0+self.moovestat]
            self.pos.x -=1
            self.count_walk +=1
        self.real_rect.center = self.pos

    def detect(self):
        if (self.pos - self.game.player.pos).length() < 200*PATCHW:
            self.game.player.detection.append(self)
            self.moovestat += 4
            self.detectstat = True
        else:
            self.detectstat = False

    def footupdate(self):
        self.timer += 1
        if self.timer <=15:
            self.moovestat = 0

        elif self.timer <= 31:
            self.moovestat = 1
        else:
            self.timer = 0
            self.moovestat = 0


    def selling(self, item, type):

        done = False
        if type == "primary":
            if self.game.player.inventory.priceitemprimary[item] <= self.game.player.coins:
                for index, slot in enumerate(self.game.player.inventory.priminvslots):
                    if slot == None and not(done):
                        self.game.player.inventory.priminvslots[index] = self.game.player.inventory.sellingitemprimary[item]
                        self.game.player.coins -= self.game.player.inventory.priceitemprimary[item]
                        self.game.player.inventory.sellingitemprimary.pop(item)
                        self.game.player.inventory.priceitemprimary.pop(item)
                        self.buysound()
                        done = True
        elif type == "secondary":
            if self.game.player.inventory.priceitemsecondary[item] <= self.game.player.coins:
                for index, slot in enumerate(self.game.player.inventory.secondinvslots):
                    if slot == None and not(done):
                        self.game.player.inventory.secondinvslots[index] = self.game.player.inventory.sellingitemsecondary[item]
                        self.game.player.coins -= self.game.player.inventory.priceitemsecondary[item]
                        self.game.player.inventory.sellingitemsecondary.pop(item)
                        self.game.player.inventory.priceitemsecondary.pop(item)
                        self.buysound()
                        done = True
        elif self.game.player.inventory.priceitemhat[item] <= self.game.player.coins:
            for index, slot in enumerate(self.game.player.inventory.hatinvslots):
                if slot == None and not(done):
                    self.game.player.inventory.hatinvslots[index] = self.game.player.inventory.sellingitemhat[item]
                    self.game.player.coins -= self.game.player.inventory.priceitemhat[item]
                    self.game.player.inventory.sellingitemhat.pop(item)
                    self.game.player.inventory.priceitemhat.pop(item)
                    self.buysound()
                    done = True

    def buysound(self):
        self.game.buysound.stop()
        self.game.buysound.play()


class Hurtica(pg.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.all_sprites, game.dealers, game.layer_yes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.bank_image = game.hurtica_img_bank
        self.image = self.bank_image[0]
        self.pos = vec(HURTICA_X, HURTICA_Y)
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.hit_rect = self.real_rect.copy()
        self.real_rect.center = self.pos
        self.right = True
        self.moovestat = 0
        self.timer = 0
        self.count_walk = 0

    def update(self):
        self.footupdate()
        if self.game.dealer.detectstat:
            self.moovestat +=4
        if self.count_walk == 25:
            self.count_walk = 0
            if self.right:
                self.right = False
            else:
                self.right = True

        if self.right:
            self.image = self.bank_image[2+self.moovestat]
            self.pos.x +=1
            self.count_walk +=1
        else:
            self.image = self.bank_image[0+self.moovestat]
            self.pos.x -=1
            self.count_walk +=1
        self.real_rect.center = self.pos

    def footupdate(self):
        self.timer += 1
        if self.timer <=24:
            self.moovestat = 0
        elif self.timer <= 35:
            self.moovestat = 1
        else:
            self.timer = 0
            self.moovestat = 0
