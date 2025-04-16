import pygame as pg
import sys
from os import path
from settings import *
from tilemap import *
from player import *
from ship import *
from ground import *
from globuzar import *
from wall import *
from constructor import *
from math import *
from master_mind import *
from dealer import *
from tools import *
from save import *


class Game:
    def __init__(self):
        self.volume = VOLUME
        self.volumesounds = VOLUMESOUNDS
        self.volumemusic = VOLUMEMUSIC
        pg.mixer.pre_init(44100, -16, 2, 2048)  #fix bugd sound
        pg.init()
        pg.key.set_repeat(50, 100)
        self.width = WIDTH
        self.height = HEIGHT
        self.window = pg.display.set_mode((self.width, self.height), pg.FULLSCREEN)
        self.screen = self.window
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.playing = 'Menu'
        self.create_group()
        self.constructor = Constructor(self)
        self.menu = self.Menu(self)
        self.options = self.Options(self)
        self.floor = Floor(len(self.map.data[0]),len(self.map.data), self)
        self.invocate()
        self.camera = Camera(self.map.width, self.map.height, self)
        self.minimap = Minimap(MWIDTH, MHEIGHT, self)
        self.master_mind = Master_Mind(self)
        self.save = Save_game(self)
        self.run()

    def create_group(self):
        self.all_sprites = pg.sprite.Group()
        self.collidewithplayer = pg.sprite.Group()
        self.collidewithglobuzars = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grounds = pg.sprite.Group()
        self.globuzars = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        self.playersprite = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bulletssharp = pg.sprite.Group()
        self.ships = pg.sprite.Group()
        self.drawable = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.inventory = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.dealers = pg.sprite.Group()
        self.floor_group = pg.sprite.Group()
        self.sonars = pg.sprite.Group()
        self.layer_yes = pg.sprite.LayeredUpdates()
        self.layer_bar = pg.sprite.LayeredUpdates()


    def invocate(self):
        self.player = Player(self)
        self.ship = Ship(self)
        self.dealer = Dealer(self)
        self.hurtica = Hurtica(self)

    def run(self):
        while True:
            if self.playing == 'Quit':
                self.save.save_content()
                pg.quit()
                sys.exit()
            while self.playing == 'Menu':
                self.events()
                self.menu.update()
            while self.playing == 'Options':
                self.events()
                self.options.update()

            while self.playing == 'Game':
                self.dt = self.clock.tick(FPS) / 1000
                if int(self.dt) > 0.9:
                    self.dt = 0
                self.events()
                self.update()
                self.draw()

    def events(self):
        self.keys = pg.key.get_pressed()
        self.mousepos = vec(pg.mouse.get_pos())
        self.mousepress = pg.mouse.get_pressed()
        self.mouse = pg.Rect((int(self.mousepos[0]), int(self.mousepos[1]), 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if self.keys[pg.K_ESCAPE]:
                self.playing = 'Menu'

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        self.master_mind.update()

    def draw(self):
        self.window.fill(BGCOLOR)
        for sprite in self.all_sprites:
            sprite.rect = self.camera.apply(sprite)
        self.floor_group.draw(self.window)
        self.ships.draw(self.window)
        self.sonars.draw(self.window)
        self.walls.draw(self.window)
        self.layer()
        self.layer_yes.draw(self.window)
        self.layer_bar.draw(self.window)
        self.master_mind.draw()
        self.draw_hud_main()
        pg.display.flip()

    def layer(self):
        self.list = []
        for i in self.layer_yes:
            self.list.append(i)
        self.list.sort(key=lambda item: item.rect.centery)
        for item in self.list:
            self.layer_yes.change_layer(item, self.list.index(item))
            try:
                item.bar.change_layer(item, self.list.index(item))
            except:
                pass

    def draw_hud_main(self):
        self.player.draw_hud(self.player.life, self.player.max_life, self.hud_bar[0], self.hud_bar[1], LIFE_X, LIFE_Y)
        self.player.draw_hud(self.player.stamina, self.player.max_stamina, self.hud_bar[2], self.hud_bar[3], STAMINA_X, STAMINA_Y)
        self.player.draw_hud(self.player.experience, self.player.experience_max, self.hud_bar[4], self.hud_bar[5], EXPERIENCE_X, EXPERIENCE_Y)
        self.minimap.draw_minimap()
        if self.player.constructmode:
            self.player.drawable_wall()
        self.player.inventory.draw_inventory()

    def set_volume(self):
        pg.mixer.music.set_volume(1 * self.volume /100 * self.volumemusic /100)
        for sound in self.buildsounds:
            sound.set_volume(0.6 * self.volume /100 * self.volumesounds / 100)
        for sound in self.destructsounds:
            sound.set_volume(0.6 * self.volume /100 * self.volumesounds / 100)
        for sound in self.damagesounds:
            sound.set_volume(0.6 * self.volume /100 * self.volumesounds / 100)
        for sound in self.walksounds:
            sound.set_volume(0.2 * self.volume /100 * self.volumesounds / 100)
        self.constructsound.set_volume(0.6 * self.volume /100 * self.volumesounds / 100)
        self.unconstructsound.set_volume(0.6 * self.volume /100 * self.volumesounds / 100)
        self.buysound.set_volume(0.6 * self.volume /100 * self.volumesounds / 100)

    def set_resolution(self):
        #ETEINDS ET RALUME LE JEU AVEC BONNE RESOLUTION
        pass

    def save(self):
        pass

    class Menu:
        def __init__(self, game):
            self.game = game
            pg.mixer.pre_init(44100, -16, 2, 2048)  #bug soundp
            pg.init()
            self.window = pg.display.set_mode((self.game.width, self.game.height), pg.FULLSCREEN)

            true = Tools.letter_translate("play", self.game.lettersx4)
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.button_play = Button(self.game, false, true, (XPLAY, YPLAY))
            self.button_play_stat = False

            true = Tools.letter_translate("options", self.game.lettersx4)
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.button_option = Button(self.game, false, true, (XOPTION, YOPTION))
            self.button_option_stat = False


            true = Tools.letter_translate("sauvegarder", self.game.lettersx4)
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.button_sauvegarder = Button(self.game, false, true, (XSAUVEGARDE, YSAUVEGARDE))
            self.button_sauvegarder_stat = False

            self.button_quit = Button(game, self.game.button_quit_image_bank[0], self.game.button_quit_image_bank[1],
             (XQUIT, YQUIT))
            self.button_quit_stat = False

        def update(self):
            self.window.fill(BLACK)
            self.button_play_stat = self.button_play.action()
            self.button_option_stat = self.button_option.action()
            self.button_quit_stat = self.button_quit.action()
            self.button_savegarder_stat = self.button_sauvegarder.action()

            if self.button_play_stat:
                self.game.playing = 'Game'
            elif self.button_option_stat:
                self.game.playing = 'Options'
                self.game.options.volumegenerallocal = self.game.volume
                self.game.options.volumesoundslocal = self.game.volumesounds
                self.game.options.volumemusiclocal = self.game.volumemusic
                self.game.options.chiffregeneralvolume = Tools.number_translate(self.game.options.volumegenerallocal, self.game.numbersx4)
                self.game.options.chiffresoundsvolume = Tools.number_translate(self.game.options.volumesoundslocal, self.game.numbersx4)
                self.game.options.chiffremusicvolume = Tools.number_translate(self.game.options.volumemusiclocal, self.game.numbersx4)
            elif self.button_quit_stat:
                self.game.playing = 'Quit'
            elif self.button_sauvegarder_stat:
                self.game.save()


            pg.display.flip()

    class Options:
        def __init__(self, game):
            self.game = game

            self.volumegenerallocal = self.game.volume
            self.volumesoundslocal = self.game.volumesounds
            self.volumemusiclocal = self.game.volumemusic
            self.localheight = self.game.height
            self.localwidth = self.game.width

            self.window = pg.display.set_mode((self.game.width, self.game.height), pg.FULLSCREEN)
            pg.init()
            pg.mixer.pre_init(44100, -16, 2, 2048)

            true = Tools.letter_translate("back", self.game.lettersx3)
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.button_back = Button(self.game, false, true, (XBACK, YBACK))
            self.button_back_stat = False

            true = Tools.letter_translate("confirm", self.game.lettersx3)
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.button_valider = Button(self.game, false, true, (XCONFIRM, YCONFIRM))
            self.button_valider_stat = False
            #VOLUME GENERAL
            self.lettregeneralvolume = Tools.letter_translate("general volume", self.game.lettersx4)
            self.chiffregeneralvolume = Tools.number_translate(self.volumegenerallocal, self.game.numbersx4)

            true = Tools.letter_translate("+", self.game.lettersx4) #mettre un plus
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.plus_generalvolume = Button(self.game, false, true, (XPVOLUME, YPVOLUME))
            self.plus_generalvolume_stat = False

            true = Tools.letter_translate("- ", self.game.lettersx4) #mettre un moins
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.moins_generalvolume = Button(self.game, false, true, (XMVOLUME, YMVOLUME))
            self.moins_generalvolume_stat = False
            #VOLUME SONS
            self.lettresoundsvolume = Tools.letter_translate("sounds volume", self.game.lettersx4)
            self.chiffresoundsvolume = Tools.number_translate(self.volumesoundslocal, self.game.numbersx4)

            true = Tools.letter_translate("+", self.game.lettersx4) #mettre un plus
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.plus_soundsvolume = Button(self.game, false, true, (XPSOUNDSVOLUME, YPSOUNDSVOLUME))
            self.plus_soundsvolume_stat = False

            true = Tools.letter_translate("-", self.game.lettersx4) #mettre un moins
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.moins_soundsvolume = Button(self.game, false, true, (XMSOUNDSVOLUME, YMSOUNDSVOLUME))
            self.moins_soundsvolume_stat = False

            #VOLUME musique
            self.lettremusicvolume = Tools.letter_translate("music volume", self.game.lettersx4)
            self.chiffremusicvolume = Tools.number_translate(self.volumemusiclocal, self.game.numbersx4)

            true = Tools.letter_translate("+", self.game.lettersx4) #mettre un plus
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.plus_musicvolume = Button(self.game, false, true, (XPMUSICVOLUME, YPMUSICVOLUME))
            self.plus_musicvolume_stat = False

            true = Tools.letter_translate("-", self.game.lettersx4) #mettre un moins
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.moins_musicvolume = Button(self.game, false, true, (XMMUSICVOLUME, YMMUSICVOLUME))
            self.moins_musicvolume_stat = False

            true = Tools.number_translate(int(str(self.localwidth) + str(self.localheight)) , self.game.numbersx4) #a modifier (le manip avec les int et str permet de les mettres a coter)
            false = true.copy()
            true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
            false.fill(GREY,special_flags=pg.BLEND_MULT)
            self.button_resolution = Button(self.game, false, true, (XRESOLUTION, YRESOLUTION))
            self.button_resolution_stat = False

        def update(self):
            self.window.fill(BLACK)
            self.button_back_stat = self.button_back.action()
            self.button_valider_stat = self.button_valider.action()

            self.button_plus_generalvolume_stat = self.plus_generalvolume.action()
            self.button_moins_generalvolume_stat = self.moins_generalvolume.action()

            self.button_plus_soundsvolume_stat = self.plus_soundsvolume.action()
            self.button_moins_soundsvolume_stat = self.moins_soundsvolume.action()

            self.button_plus_musicvolume_stat = self.plus_musicvolume.action()
            self.button_moins_musicvolume_stat = self.moins_musicvolume.action()

            self.button_resolution_stat = self.button_resolution.action()

            #image non interactives
            self.game.window.blit(self.chiffregeneralvolume, (int(XVOLUME), int(YVOLUME)))
            self.game.window.blit(self.lettregeneralvolume, (int(XTVOLUME), int(YTVOLUME)))

            self.game.window.blit(self.chiffresoundsvolume, (int(XSOUNDSVOLUME), int(YSOUNDSVOLUME)))
            self.game.window.blit(self.lettresoundsvolume, (int(XTSOUNDSVOLUME), int(YTSOUNDSVOLUME)))

            self.game.window.blit(self.chiffremusicvolume, (int(XMUSICVOLUME), int(YMUSICVOLUME)))
            self.game.window.blit(self.lettremusicvolume, (int(XTMUSICVOLUME), int(YTMUSICVOLUME)))

            if self.button_back_stat:
                self.game.playing = 'Menu'

            elif self.button_valider_stat:
                self.game.volume = self.volumegenerallocal
                self.game.volumesounds = self.volumesoundslocal
                self.game.volumemusic = self.volumemusiclocal
                self.game.set_volume()
                #ICI ON CHANGE LA RESOLUTION
                if self.localwidth != self.game.width:
                    self.game.width = self.localwidth
                    self.game.height = self.localheight
                    self.game.set_resolution()

            elif self.button_plus_generalvolume_stat:
                if self.volumegenerallocal != 100:
                    self.volumegenerallocal +=1
                    self.chiffregeneralvolume = Tools.number_translate(self.volumegenerallocal, self.game.numbersx4)

            elif self.button_moins_generalvolume_stat:
                if self.volumegenerallocal != 0:
                    self.volumegenerallocal -=1
                    self.chiffregeneralvolume = Tools.number_translate(self.volumegenerallocal, self.game.numbersx4)

            elif self.button_plus_soundsvolume_stat:
                if self.volumesoundslocal != 100:
                    self.volumesoundslocal +=1
                    self.chiffresoundsvolume = Tools.number_translate(self.volumesoundslocal, self.game.numbersx4)

            elif self.button_moins_soundsvolume_stat:
                if self.volumesoundslocal != 0:
                    self.volumesoundslocal -=1
                    self.chiffresoundsvolume = Tools.number_translate(self.volumesoundslocal, self.game.numbersx4)

            elif self.button_plus_musicvolume_stat:
                if self.volumemusiclocal != 100:
                    self.volumemusiclocal +=1
                    self.chiffremusicvolume = Tools.number_translate(self.volumemusiclocal, self.game.numbersx4)

            elif self.button_moins_musicvolume_stat:
                if self.volumemusiclocal != 0:
                    self.volumemusiclocal -=1
                    self.chiffremusicvolume = Tools.number_translate(self.volumemusiclocal, self.game.numbersx4)

            elif self.button_resolution_stat:
                done = False
                for i, res in enumerate(RESOLUTION):
                    if res[0] == self.localwidth and not(done):
                        self.localwidth = RESOLUTION[i-1][0]
                        self.localheight = RESOLUTION[i-1][1]
                        done = True

                        true = Tools.number_translate(int(str(self.localwidth) + str(self.localheight)) , self.game.numbersx4) #a modifier (le manip avec les int et str permet de les mettres a coter)
                        false = true.copy()
                        true.fill(LIGHTGREY,special_flags=pg.BLEND_MULT)
                        false.fill(GREY,special_flags=pg.BLEND_MULT)
                        self.button_resolution = Button(self.game, false, true, (XRESOLUTION, YRESOLUTION))
                        self.button_resolution_stat = False

            pg.display.flip()

g = Game()
