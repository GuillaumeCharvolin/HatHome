import pygame as pg
from settings import *
import random
import math

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.real_rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
            self.tilewidth = len(self.data[0])
            self.tileheight= len(self.data)
            self.width = self.tilewidth * TILESIZE
            self.height = self.tileheight * TILESIZE

class Floor(pg.sprite.Sprite):
    def __init__(self, width, height, game):
        self.groups = game.all_sprites, game.floor_group
        self.game = game
        self.wind = STATUSWIND
        self.images = []
        if self.wind:
            for veget in self.game.vegetation_image_bank:
                self.images.append(pg.Surface((width*50, height*50)))
        else:
            self.images.append(pg.Surface((width*50, height*50)))
        self.real_rect = self.images[0].get_rect()
        self.rect = self.real_rect

        pg.sprite.Sprite.__init__(self, self.groups)
        self.windc = 0
        self.fct = 0
        self.autresens = False
        self.avancement = random.uniform(0,0.2)
        self.compteur = 0
        self.x = 0.5
        self.fct = math.sin(self.x)


        for image in self.images:
            for col, tiles in enumerate(self.game.map.data):
                for row, tile in enumerate(tiles):
                    if tile == '.' or tile == 'G' or tile == 'P' or tile == 'S' or tile == 'D':#Ground
                        image.blit(self.game.ground_image_bank[0],(row *TILESIZE, col*TILESIZE))
                        #Ground(self, col, row)
            for col, tiles in enumerate(self.game.map.data):
                for row, tile in enumerate(tiles):
                    if tile == '.' or tile == 'G' or tile == 'P' or tile == 'S' or tile == 'D':#Vegetation
                        if random.randint(1,1) == 1:
                            for i in range(2):
                                x = row*TILESIZE + random.randint(1,int(50*PATCHW))
                                y = col*TILESIZE + random.randint(1,int(50*PATCHW))
                                for z, image in enumerate(self.images):
                                    image.blit(self.game.vegetation_image_bank[z],(x, y)) #REMPLACER 0 PAR I

        #self.image = self.images[0]
        self.image = self.game.map_image

    '''
    def update(self):
        if self.compteur >= 1000 and self.windc <= 0.5:
            self.winc = 0.5
            self.autresens = False
            self.intensity = random.uniform(0,0.2)
            self.compteur = 0

        if not self.autresens:
            self.windc += self.intensity
            if int(self.windc) >= len(self.images) - 0.5:
                self.winc = len(self.images) - 0.5
                self.windc -= self.intensity
                self.autresens = True
        else:
            self.windc-= self.intensity
            print(self.windc)
            if self.windc <= 0.5:
                self.winc = 0.5
                self.autresens = False
        self.compteur +=1
        self.image = self.images[int(self.windc)]

        1)générer coef d'avancement aleatoire
        2)partir de 0 pour l'intensité du vent
        3)generer un coef d'avancement entre 0 et 0.2 quand le compteur arrive au max
        4)calculer l'intensité du vent en fonction de la fonction sin (sur 0;pi)

        '''

    def update(self):
        if self.wind:
            if self.compteur >= 1000 :
                self.windc = 0.5
                self.autresens = False
                self.avancement = random.uniform(0,0.2)
                self.x += self.avancement
                if self.x > 3.14:
                    self.x = 0
                    self.fct = math.sin(self.x)
                    self.compteur = 0

            if not self.autresens:
                self.windc += self.fct/15
                if int(self.windc) >= len(self.images) - 0.5:
                    self.windc = len(self.images) - 0.5
                    self.autresens = True
            else:
                self.windc -= self.fct/15
                if self.windc <= 0.5:
                    self.windc += 0.5
                    self.autresens = False


            if self.windc > len(self.images):
                self.windc = self.windc - len(self.images)

            self.compteur +=1
            self.image = self.images[int(self.windc)]

class Minimap(pg.sprite.Sprite):
    def __init__(self, width, height, game):

        self.game = game
        self.width = width*PATCHW
        self.height = height*PATCHH
        self.mapwidth = len(self.game.map.data[0]) * 50
        self.mapheight = len(self.game.map.data) * 50
        self.image = pg.Surface((self.width,self.height) ,pg.SRCALPHA) #pg.SRCALPHA permet la transparance
        self.image.fill((0,0,0,125))

        self.reddot = pg.Surface((4,4), pg.SRCALPHA)
        self.reddot.fill((255,0,0,200))

        self.greendot = pg.Surface((4,4), pg.SRCALPHA)
        self.greendot.fill((0,255,0,200))

        self.yellowdot = pg.Surface((8,8), pg.SRCALPHA)
        self.yellowdot.fill((255,255,0,200))

        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect


    def draw_minimap(self):

        self.mapimage = self.game.window.blit(self.image, (self.game.width-self.width, 0))

        for sprite in self.game.globuzars:
            coords = sprite.pos
            xonmap = round(coords[0] / self.mapwidth * self.width)
            yonmap = round(coords[1] / self.mapheight * self.height)

            self.game.window.blit(self.reddot, (self.mapimage[0]+xonmap,self.mapimage[1]+yonmap))

        for sprite in self.game.playersprite:
            coords = sprite.pos
            xonmap = round(coords[0] / self.mapwidth * self.width)
            yonmap = round(coords[1] / self.mapheight * self.height)

            self.game.window.blit(self.greendot, (self.mapimage[0]+xonmap,self.mapimage[1]+yonmap))

        for sprite in self.game.ships:
            coords = sprite.pos
            xonmap = round(coords[0] / self.mapwidth * self.width)
            yonmap = round(coords[1] / self.mapheight * self.height)

            self.game.window.blit(self.yellowdot, (self.mapimage[0]+xonmap,self.mapimage[1]+yonmap))


         #j'ai essayé de blit sur self.mapimage mais c'est un rect donc j'ajoute les coords



class Camera(pg.sprite.Sprite):
    def __init__(self, width, height, game):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.game = game


    def apply(self,entity):
        return entity.real_rect.move(self.camera.topleft)

    def update(self, target):
        newx = int(self.game.width/2) - target.real_rect.center[0]
        newy = int(self.game.height/2) - target.real_rect.center[1]
        self.camera.x = newx
        self.camera.y = newy
