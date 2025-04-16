import pygame as pg
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2
import random

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, wall):
        self.groups = game.all_sprites, game.walls, game.collidewithplayer, game.collidewithglobuzars
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_bank = game.wall_image_bank
        self.image = self.image_bank[5]
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.pos = vec(x,y)
        self.x = x
        self.y = y
        self.real_rect.x = x * TILESIZE
        self.real_rect.y = y * TILESIZE
        self.hit_rect = self.real_rect
        self.hit_rect.center = self.real_rect.center
        self.life = 5000
        self.max_life = 5000
        self.bar = Wall.Bar(self, game)
        self.collideside = [False, False, False, False] #droite, haut, gauche, bas
        self.game.player.wall_use -= 1

        self.trigger_wall(False)
        self.update()
        self.testcollide()



    def update(self):
        self.real_rect.center = self.pos
        if self.life <= 0:
            self.destruct(True)

    def beattack(self, mob):
        self.life -= mob.wallattack


    def testcollide(self):
        hits1 = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
        hits2 = pg.sprite.spritecollide(self, self.game.playersprite, False, collide_hit_rect)
        hits3 = pg.sprite.spritecollide(self, self.game.globuzars, False, collide_hit_rect)
        hits4 = pg.sprite.spritecollide(self, self.game.ships, False, collide_hit_rect)
        if len(hits1) != 1 or len(hits2) + len(hits3) + len(hits4) != 0:
            self.destruct(False)
        else: #on joue le son de la construction ici car on a la confimartion que le mur peut bien être construit
            for sound in self.game.buildsounds:
                sound.stop()
            self.game.buildsounds[random.randint(0,2)].play() #sélectionne un son au hasard parmis les 3

    def destruct(self, sound):
        self.kill()
        self.bar.kill()
        if self.life/self.max_life == 1:
            self.game.player.wall_use += 1
        for wall in self.game.walls:
            wall.trigger_wall(True)
        if sound:
            self.game.destructsounds[random.randint(0,1)].play()

    def trigger_wall(self, fromotherwall):
        self.collideside = [False, False, False, False]
        for wall in self.game.walls:
            if (self.pos - wall.pos).length() == 50*PATCHW:
                if fromotherwall == False:
                    wall.trigger_wall(True)

                if self.pos[0] - wall.pos[0] == -50*PATCHW:
                    self.collideside[0] = True
                elif self.pos[1] - wall.pos[1] == 50*PATCHH:
                    self.collideside[1] = True
                elif self.pos[0] - wall.pos[0] == 50*PATCHW:
                    self.collideside[2] = True
                elif self.pos[1] - wall.pos[1] == -50*PATCHH:
                    self.collideside[3] = True

        '''
        [droite, haut, gauche, bas]
        '''

        if self.collideside == [True, False, False, False]:
             self.image = pg.transform.flip(self.image_bank[0], True, False).copy()
        #image 5 convient pour si mur detecte en haut
        elif self.collideside == [False, False, True, False]:
            self.image = self.image_bank[0].copy()
        elif self.collideside == [False, False, False, True]:
            self.image = self.image_bank[1].copy()

        elif self.collideside == [True, False, True, False]:
            self.image =self.image_bank[6].copy()
        elif self.collideside == [False, True, False, True]:
            self.image = self.image_bank[1].copy()

        elif self.collideside == [True, True, False, False]:
            self.image = pg.transform.flip(self.image_bank[0], True, False).copy()
        elif self.collideside == [False, True, True, False]:
            self.image = self.image_bank[0].copy()
        elif self.collideside == [False, False, True, True]:
            self.image = pg.transform.flip(self.image_bank[4], True, False).copy()
        elif self.collideside == [True, False, False, True]:
            self.image = self.image_bank[4].copy()

        elif self.collideside == [True, True, True, False]:
            self.image = self.image_bank[6].copy()
        elif self.collideside == [False, True, True, True]:
            self.image = pg.transform.flip(self.image_bank[4], True, False).copy()
        elif self.collideside == [True, False, True, True]:
            self.image = self.image_bank[3].copy()
        elif self.collideside == [True, True, False, True]:
            self.image = self.image_bank[4].copy()

        elif self.collideside == [True, True, True, True]:
            self.image = self.image_bank[3].copy()
        elif self.collideside == [False, False, False, False]:
            self.image = self.image_bank[5].copy()
        elif self.collideside == [False, True, False, False]:
            self.image = self.image_bank[5].copy()

    class Bar(pg.sprite.Sprite):
        def __init__(self, WALL, game):
            self.groups = game.all_sprites, game.layer_bar
            pg.sprite.Sprite.__init__(self, self.groups)
            self.wall = WALL
            self.game = game
            self.col = (0,0,255)
            self.image_bank = self.game.wall_bar
            self.width = self.image_bank[0].get_width()
            self.real_rect = self.image_bank[0].get_rect()
            self.rect = self.real_rect
            self.image = pg.Surface((self.image_bank[0].get_width(), self.image_bank[0].get_height()))

        def update(self):
            h = (self.wall.life / self.wall.max_life) * self.image_bank[0].get_width()
            if h<0:
                h = 0
            start = (self.image_bank[0].copy()).subsurface((0,0, h, self.image_bank[0].get_height()))
            self.image.blit(start, (0, 0))
            end = (self.image_bank[1].copy()).subsurface((h, 0, self.image_bank[0].get_width()-h, self.image_bank[0].get_height()))
            self.image.blit(end, (h, 0))
            self.real_rect.x = self.wall.real_rect.x + 25-13 * PATCHW
            self.real_rect.y = self.wall.real_rect.y + 35 * PATCHH
