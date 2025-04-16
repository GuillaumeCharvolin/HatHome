import pygame as pg
from settings import *
from chest import *
vec = pg.math.Vector2
from math import hypot
from tilemap import collide_hit_rect
import random
from math import *
from gun import *
from inventory import *
from wall import *
from globuzar import *
from tools import *

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.playersprite, game.layer_yes
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.gun = Gun(self.game, gold45)
        self.selectgun = 'gold45'
        self.inventory = Inventory(game, self)

        self.bank_image = game.player_image_bank
        self.bank_image_construct = game.player_image_construct_bank
        self.bank_image_coin = game.player_image_coin_bank
        self.image = game.player_image_bank[0]
        self.real_rect = self.image.get_rect()
        self.rect = self.real_rect
        self.hit_rect = self.real_rect
        self.hit_rect.center = self.real_rect.center
        self.vel = vec(0, 0)
        self.pos = vec(PLAYER_X, PLAYER_Y)

        self.moovestat = 0
        self.timer = 0
        self.max_life = PLAYER_LIFE_STAT
        self.life = PLAYER_LIFE_STAT
        self.max_stamina = PLAYER_STAMINA_STAT
        self.stamina = PLAYER_STAMINA_STAT
        self.experience = 0
        self.experience_max = 10
        self.gemstone = 0
        self.wall_use = WALL_START
        self.coins = COINS_START
        self.cd = 0
        self.invincibility = False
        self.cdtp = 0
        self.countmob = 0
        self.use = False

        #VARIABLE POUR LE BUILD
        self.constructmode = False
        self.unbuildable = pg.Surface((50*PATCHW,50*PATCHH), pg.SRCALPHA)
        self.unbuildable.fill((255,0,0,127))
        self.buildable = pg.Surface((50*PATCHW,50*PATCHH), pg.SRCALPHA)
        self.buildable.fill((0,255,0,127))
        self.wallattack = 0

        self.isbuilding = False
        self.buildingtimer = 0
        self.isdestructing = False
        self.destructtimer = 0
        self.nowall = True

        self.detection = []

    def get_keys(self):
        self.vel = vec(0, 0)
        self.keys = self.game.keys
        self.mousepress = self.game.mousepress
        self.translator = vec(self.game.camera.camera.x, self.game.camera.camera.y) # map --> screen
        self.mousepossc = self.game.mousepos - self.translator
        if self.cd > 0:
            self.cd -= 1
        if self.keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if self.keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if self.keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if self.keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.keys[pg.K_e]:
            self.use = True
        else:
            self.use = False
        if self.keys[pg.K_LSHIFT] and (self.vel.y != 0 or self.vel.x != 0):
            if self.stamina > 0:
                self.vel.x = self.vel.x * PLAYER_STAMINA_EFFECT
                self.vel.y = self.vel.y * PLAYER_STAMINA_EFFECT
                self.stamina -= PLAYER_STAMINA_REDUCE
                self.timer += 1

        elif self.stamina < self.max_stamina:
            self.stamina += PLAYER_STAMINA_REGEN
        if self.stamina < 0:
            self.stamina = 0
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina

        if self.keys[pg.K_c]:
            self.gun.kill()
            self.selectgun = None
            if self.constructmode:
                self.constructmode = False
            self.constructmode = True

        #[Cheat]
        if self.keys[pg.K_1]:
            for mob in self.game.globuzars:
                mob.life -= 100000
        if self.keys[pg.K_2] and self.cdtp > 20:
            self.pos = self.mousepossc
            self.cdtp = 0
        if self.keys[pg.K_3]:
            Globuzar(self.game, self.mousepossc.x, self.mousepossc.y)


        if self.keys[pg.K_f]:
            self.bank_image = self.game.player_image_bank
            if self.constructmode == True:
                self.gun = Gun(self.game, wavax)
                self.gun.move()
                self.selectgun = 'wavax'
                self.cd = CD_SELECT_GUN
                self.constructmode = False
            if self.selectgun == 'gold45' and self.cd == 0 :
                self.gun.kill()
                self.gun = Gun(self.game, wavax)
                self.gun.move()
                self.selectgun = 'wavax'
                self.cd = CD_SELECT_GUN
            elif self.selectgun == 'wavax' and self.cd == 0:
                self.gun.kill()
                self.gun = Gun(self.game, aspirator)
                self.gun.move()
                self.selectgun = 'aspirator'
                self.cd = CD_SELECT_GUN
            elif self.selectgun == 'aspirator' and self.cd == 0:
                self.gun.kill()
                self.gun = Gun(self.game, gold45)
                self.gun.move()
                self.selectgun = 'gold45'
                self.cd = CD_SELECT_GUN

        if self.constructmode:
            self.drawable_wall()
            self.bank_image = self.bank_image_construct
            if self.mousepress[0]:
                if (self.mousepossc-self.pos).length() < CONSTRUCT_DISTANCE and self.wall_use > 0:
                    if not self.isbuilding:
                        self.constructbar = self.ConstructBar(self.game, True)
                        self.isbuilding = True
                        #jouer le son de la construiction
                    else:
                        if self.buildingtimer == 0:
                            self.game.constructsound.play()
                        self.buildingtimer += 1
                    if self.buildingtimer == 50:
                        self.construct_wall()
                        self.destructbar()

            elif self.mousepress[2]:
                self.translator = vec(self.game.camera.camera.x, self.game.camera.camera.y) # map --> screen
                self.mousepossc = self.game.mousepos - self.translator # map --> mouse
                if 50 < (self.mousepossc-self.pos).length() < 200:
                    self.nowall = True
                    for i in self.game.walls:
                        if i.rect.collidepoint(self.game.mousepos[0], self.game.mousepos[1]): #en gros si un mur touche la souris
                            if not self.isdestructing:
                                self.wall = i
                                self.constructbar = self.ConstructBar(self.game, False)
                                self.isdestructing = True
                            else:
                                if self.wall == i: #premet de détruire le timer si on change de mur
                                    if self.destructtimer == 0:
                                        self.game.unconstructsound.play()
                                    self.destructtimer += 1
                                else:
                                    self.destructbar()
                            if self.destructtimer == 30:
                                i.destruct(True)
                                self.destructbar()
                            self.nowall = False
                    if self.nowall:
                        self.destructbar() #si aucun mur touche on détruit

            if not (self.mousepress[0] or self.mousepress[2]) and (self.isbuilding or self.isdestructing) : #a ne pas inclure en temps que elif de la boucle d'avant
                self.destructbar()
        if self.gun.d["is"] == 'aspirator' and not self.constructmode:
            self.bank_image = self.bank_image_coin

        if self.vel.x != 0 or self.vel.y != 0:
            self.footupdate()
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def drawable_wall(self):
        self.wallcoord = self.game.mousepos
        if 50 < (self.mousepossc - self.pos).length() < 200:
            for i in self.game.walls:
                if (i.pos - self.mousepossc).length() <= 75:
                    if i.pos[0]-25 > self.mousepossc[0]:
                        self.wallcoord[0] = i.pos[0]-50*PATCHW + self.translator[0]
                    elif i.pos[0]+25 < self.mousepossc[0]:
                        self.wallcoord[0] = i.pos[0]+50*PATCHW + self.translator[0]
                    else:
                        self.wallcoord[0] = i.pos[0]+ self.translator[0]

                    if i.pos[1]-25 > self.mousepossc[1]:
                        self.wallcoord[1] = i.pos[1]-50*PATCHH + self.translator[1]
                    elif i.pos[1]+25 < self.mousepossc[1]:
                        self.wallcoord[1] = i.pos[1]+50*PATCHH + self.translator[1]
                    else:
                        self.wallcoord[1] = i.pos[1] + self.translator[1]

            if self.collidecheck():
                self.game.window.blit(self.buildable , (self.wallcoord[0]-25*PATCHW, self.wallcoord[1]-25*PATCHH))    #-25 car un mur fait 50x50 + il faudra prendre en compt qu'il faut partir du centres
            else:
                self.game.window.blit(self.unbuildable , (self.game.mousepos[0]-25*PATCHW, self.game.mousepos[1]-25*PATCHH))
                if not self.isdestructing:
                    self.destructbar() #évite de continuer de charger la barre du construct quand on ne construit pas vraiment
        else:
            self.game.window.blit(self.unbuildable , (self.game.mousepos[0]-25*PATCHW, self.game.mousepos[1]-25*PATCHH))
            if not self.isdestructing:
                self.destructbar()

    def collidecheck(self):
        hits = 0
        for i in self.game.ships:
            hits += i.rect.collidepoint(self.wallcoord[0]-25*PATCHW, self.wallcoord[1]-25*PATCHH)
        for i in self.game.walls:
            hits += i.rect.collidepoint(self.wallcoord[0]-25*PATCHW, self.wallcoord[1]-25*PATCHH)
        for i in self.game.playersprite:
            hits += i.rect.collidepoint(self.wallcoord[0]-25*PATCHW, self.wallcoord[1]-25*PATCHH)
        for i in self.game.globuzars:
            hits += i.rect.collidepoint(self.wallcoord[0]-25*PATCHW, self.wallcoord[1]-25*PATCHH)
        if hits  != 0:
            return(False)
        else:
            return(True)

    def construct_wall(self):
        Wall(self.game, self.wallcoord[0] - self.translator[0] , self.wallcoord[1] - self.translator[1], 7)

    def destructbar(self):
        self.game.unconstructsound.stop()
        self.game.constructsound.stop()
        self.buildingtimer = 0
        self.destructtimer = 0
        self.isbuilding = False
        self.isdestructing = False
        if hasattr(self, 'constructbar'): #fonction de python qui permet de savoir si l'objet a cet attribut
            self.constructbar.kill()

    def get_mouse(self):
        x = self.game.mousepos[0]
        y = self.game.mousepos[1]

        if y >= self.game.height/2: #BOTTOM
            if x >= self.game.width/2: #RIGHT BOTTOM
                if  DIAGONAL * x < y : #BOTTOM TRIANGLE
                    self.image = self.bank_image[0+self.moovestat]
                    self.gun.triangle = 7
                else:
                    self.image = self.bank_image[2+self.moovestat]
                    self.gun.triangle = 8
            else: #LEFT BOTTOM
                if DIAGONAL * (-x) + self.game.height < y : #TOP TRIANGLE
                    self.image = self.bank_image[14+self.moovestat]
                    self.gun.triangle = 6
                else:
                    self.image = self.bank_image[12+self.moovestat]
                    self.gun.triangle = 5
        else: #TOP
            if x <= self.game.width/2: #LEFT TOP
                if DIAGONAL * x < y : #BOTTOM TRIANGLE
                    self.image = self.bank_image[10+self.moovestat]
                    self.gun.triangle = 4
                else:
                    self.image = self.bank_image[8+self.moovestat]
                    self.gun.triangle = 3
            else: #RIGHT TOP
                if DIAGONAL * (-x) + self.game.height < y : #TOP TRIANGLE
                    self.image = self.bank_image[4+self.moovestat]
                    self.gun.triangle = 1
                else:
                    self.image = self.bank_image[6+self.moovestat]
                    self.gun.triangle = 2
        if self.invincibility:
            self.image = pg.Surface((self.rect.width, self.rect.height))
            self.image.set_alpha(0)


    def footupdate(self):
        self.timer += 1

        if self.timer <= 25: #obligé de passer par une inégalité et non une égalité car on ne peut prédire a quel valeur exact du timer ce dernier fera changer de pied (a cause du sprint qui empeche de predir si la timer passera exactement sur une valeur)
            if self.moovestat == 1:
                self.stepsound()
                self.moovestat = 0
        elif self.timer <= 50:
            if self.moovestat == 0:
                self.stepsound()
                self.moovestat = 1
        else:
            self.timer = 0

    def stepsound(self):
        for sound in self.game.walksounds:
            sound.stop()
        self.game.walksounds[randint(0,6)].play()


    def update(self):
        Player.countime += 1
        self.cdtp += 1
        #MOUVEMENT
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centery = self.pos.y
        Tools.collide(self, self.game.collidewithplayer, 'y')
        self.hit_rect.centerx = self.pos.x
        Tools.collide(self, self.game.collidewithplayer, 'x')
        self.real_rect.center = self.hit_rect.center
        self.experience_update()
        #Direction
        self.get_mouse()
        #Inventory
        self.inventory.update()

        if Player.countime < INVINCIBILITY_TIME and Player.countime%10 < 5:
            self.invincibility = True
        else:
            self.invincibility = False

    def experience_update(self):
        if self.experience > self.experience_max:
            self.experience = 0
            self.gemstone += 1
            self.experience_max *= 1.1

    def draw_hud(self, x, x_max, f_bank, r_bank, posx, posy):
        h = (x / x_max) * f_bank.get_width()
        if h<0:
            h = 0
        start = (f_bank.copy()).subsurface((0,0, h, f_bank.get_height()))
        self.game.window.blit(start, (posx, posy))
        end = (r_bank.copy()).subsurface((h,0, f_bank.get_width()-h, f_bank.get_height()))
        self.game.window.blit(end, (h+posx, posy))



    countime = INVINCIBILITY_TIME+1
    def beattack(self, mob):
        if Player.countime > INVINCIBILITY_TIME:
            self.life -= mob.damage
            Player.countime = 0

            for sound in self.game.damagesounds:
                sound.stop()
            self.game.damagesounds[randint(0,2)].play()


    class ConstructBar(pg.sprite.Sprite):
        def __init__(self, game, construct):
            self.groups = game.all_sprites, game.layer_bar
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            self.col = (135, 130, 130)
            self.construct = construct
            if self.construct:
                self.image_bank = self.game.wall_bar
            else:
                self.image_bank = self.game.wall_bar
            self.width = self.image_bank[0].get_width()
            self.real_rect = self.image_bank[0].get_rect()
            self.rect = self.real_rect
            self.image = pg.Surface((self.image_bank[0].get_width(), self.image_bank[0].get_height()))


        def update(self):
            if self.construct:
                h = (self.game.player.buildingtimer / 50) * self.image_bank[0].get_width()
            else:
                h = (self.game.player.destructtimer / 30) * self.image_bank[0].get_width()

            start = (self.image_bank[0].copy()).subsurface((0,0, h, self.image_bank[0].get_height()))
            self.image.blit(start, (0, 0))
            end = (self.image_bank[1].copy()).subsurface((h, 0, self.image_bank[0].get_width()-h, self.image_bank[0].get_height()))
            self.image.blit(end, (h, 0))
            self.real_rect.x = self.game.player.wallcoord[0] - self.game.player.translator[0] + 25-13 * PATCHW
            self.real_rect.y = self.game.player.wallcoord[1] - self.game.player.translator[1] + 35 * PATCHH
