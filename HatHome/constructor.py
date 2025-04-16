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
from gun import *

class Constructor:

    def __init__(self, game):
        self.game = game
        self.load_data()

    def load_data(self):

        #folder
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "Image")
        self.gold45_folder = path.join(self.img_folder, "Gold45")
        self.wavax_folder = path.join(self.img_folder, "Wavax")
        self.aspirator_folder = path.join(self.img_folder, "Aspirator")
        self.sound_folder = path.join(self.game_folder, "Sound")
        self.fire_sound_folder = path.join(self.sound_folder, 'FireSound')
        self.ship_folder = path.join(self.img_folder, 'Ship')
        self.menu_folder = path.join(self.img_folder, "Menu")
        self.text_folder = path.join(self.img_folder, "Text")
        #map music
        self.game.map = Map(path.join(self.game_folder, MAP))
        self.game.map_image = self.charge(self.img_folder + MAP_IMAGE)
        #self.game.music = pg.mixer.music.load(self.sound_folder + MUSIC)
        pg.mixer.music.set_volume(1 * self.game.volume /100)

        self.game.buildsounds = []
        self.game.buildsounds.append(pg.mixer.Sound(self.sound_folder + BUILD_SOUND1))
        self.game.buildsounds.append(pg.mixer.Sound(self.sound_folder + BUILD_SOUND2))
        self.game.buildsounds.append(pg.mixer.Sound(self.sound_folder + BUILD_SOUND3))

        self.game.destructsounds = []
        self.game.destructsounds.append(pg.mixer.Sound(self.sound_folder + DESTRUCT_SOUND1))
        self.game.destructsounds.append(pg.mixer.Sound(self.sound_folder + DESTRUCT_SOUND2))

        self.game.damagesounds = []
        self.game.damagesounds.append(pg.mixer.Sound(self.sound_folder + DAMAGE_SOUND1))
        self.game.damagesounds.append(pg.mixer.Sound(self.sound_folder + DAMAGE_SOUND2))
        self.game.damagesounds.append(pg.mixer.Sound(self.sound_folder + DAMAGE_SOUND3))

        self.game.walksounds = []
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK1))
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK2))
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK3))
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK4))
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK5))
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK6))
        self.game.walksounds.append(pg.mixer.Sound(self.sound_folder + WALK7))

        self.game.constructsound = pg.mixer.Sound(self.sound_folder + CONSTRUCT_SOUND)
        self.game.unconstructsound = pg.mixer.Sound(self.sound_folder + UNCONSTRUCT_SOUND)
        self.game.buysound = pg.mixer.Sound(self.sound_folder + BUY_SOUND)

        self.game.set_volume()

        #player
        self.game.player_image_bank = self.separate(pg.image.load(self.img_folder + PLAYER_BANK_IMG).convert_alpha(), 78)
        self.game.player_image_construct_bank = self.separate(pg.image.load(self.img_folder + PLAYER_CONSTRUCT_BANK_IMG).convert_alpha(), 78)
        self.game.player_image_coin_bank = self.separate(pg.image.load(self.img_folder + PLAYER_COIN_BANK_IMG).convert_alpha(), 78)
        self.game.player_image_coin_empty_bank = self.separate(pg.image.load(self.img_folder + PLAYER_COIN_EMPTY_BANK_IMG).convert_alpha(), 78)
        self.game.hud_bar = []
        self.game.hud_bar = self.separate(pg.image.load(self.img_folder + HUD_BAR_IMG).convert_alpha(), 260)


        #wall
        self.game.wall_image_bank = self.separate(pg.image.load(self.img_folder + WALL_IMG).convert_alpha(), 50)
        self.game.wall_inventory_image = self.separate(pg.image.load(self.img_folder + WALL_INV_IMG).convert_alpha(), 16, 2)
        self.game.ground_image_bank = self.separate(pg.image.load(self.img_folder + GROUND_IMG).convert_alpha(), 50)
        self.game.wall_bar = []
        self.game.wall_bar.append(self.charge(self.img_folder + WALL_LIFE_IMAGE))
        self.game.wall_bar.append(self.charge(self.img_folder + WALL_LIFE_IMAGE_EMPTY))
        #vegetation
        self.game.vegetation_image_bank = self.separate(pg.image.load(self.img_folder + VEGETATION_IMG).convert_alpha(), 20)
        #glo4u
        self.game.globu_img_bank = self.separate(pg.image.load(self.img_folder + GLOBU_IMG).convert_alpha(), 55)
        self.game.globu_bar = []
        self.game.globu_bar.append(self.charge(self.img_folder + GLOBU_LIFE_IMAGE))
        self.game.globu_bar.append(self.charge(self.img_folder + GLOBU_LIFE_IMAGE_EMPTY))
        #dealer
        self.game.dealer_img_bank = self.separate(pg.image.load(self.img_folder + DEALER_IMG).convert_alpha(), 47)
        self.game.hurtica_img_bank = self.separate(pg.image.load(self.img_folder + HURTICA_IMG).convert_alpha(), 153)
        #chest
        self.game.chest_image_bank = self.separate(pg.image.load(self.img_folder + CHEST_IMAGE).convert_alpha(), 51)
        #Gold45
        g = self.separate(pg.image.load(self.gold45_folder + GOLD45_IMAGE).convert_alpha(), 49)
        self.game.gold45_image_bank = list()
        for i in g:
            self.game.gold45_image_bank.append(i)
            self.game.gold45_image_bank.append(pg.transform.flip(i, False, True))
        self.game.gold45_image_bank.append(self.charge(self.gold45_folder + GOLD45_BULLET_IMAGE).convert_alpha())
        gold45['bank_image'] = self.game.gold45_image_bank
        #Wavax
        w = self.separate(pg.image.load(self.wavax_folder + WAVAX_IMAGE).convert_alpha(), 49)
        self.game.wavax_image_bank = list()
        for i in w:
            self.game.wavax_image_bank.append(i)
            self.game.wavax_image_bank.append(pg.transform.flip(i, False, True))
        self.game.wavax_image_bank.append(self.charge(self.wavax_folder + WAVAX_BULLET_IMAGE).convert_alpha())
        wavax['bank_image'] = self.game.wavax_image_bank
        #Apirator
        a = self.separate(pg.image.load(self.aspirator_folder + ASPIRATOR_IMAGE).convert_alpha(), 78)
        self.game.aspirator_image_bank = list()
        for i in a:
            self.game.aspirator_image_bank.append(i)
            self.game.aspirator_image_bank.append(pg.transform.flip(i, False, True))
        self.game.aspirator_image_bank.append(self.charge(self.aspirator_folder + ASPIRATOR_IMAGE_BACK))
        aspirator['bank_image'] = self.game.aspirator_image_bank
        #ship
        self.game.ship_image_bank = []
        self.game.ship_image_bank.append(self.charge(self.ship_folder + SHIP_IMAGE).convert_alpha())
        self.game.ship_image_bank.append(self.charge(self.ship_folder + SHIP_IMAGE_EMPTY).convert_alpha())
        self.game.ship_image_buttonwave_bank = self.separate(pg.image.load(self.ship_folder + SHIP_IMAGE_BUTTON_WAVE).convert_alpha(),9)
        #sonar
        self.game.sonar_image_bank = self.separate(pg.image.load(self.img_folder + SONAR_IMAGE).convert_alpha(),165)

        #menu
        self.game.button_quit_image_bank = self.separate(pg.image.load(self.menu_folder + IMG_QUIT).convert_alpha(),9, 4)
        self.game.button_play_image_bank = self.separate(pg.image.load(self.menu_folder + IMG_PLAY).convert_alpha(),21, 4)
        #inventory
        self.game.inventory_image_bank = self.separate(pg.image.load(self.img_folder + IMG_INVENTORY).convert_alpha(), 451, 1)
        self.game.numbers = self.separate(pg.image.load(self.text_folder + NUMBERS_IMAGE).convert_alpha(),6, 1)
        self.game.numbersx2 = self.separate(pg.image.load(self.text_folder + NUMBERS_IMAGE).convert_alpha(),6, 2)
        self.game.numbersx3 = self.separate(pg.image.load(self.text_folder + NUMBERS_IMAGE).convert_alpha(),6, 3)
        self.game.numbersx4 = self.separate(pg.image.load(self.text_folder + NUMBERS_IMAGE).convert_alpha(),6, 4)
        self.game.letters = self.separate(pg.image.load(self.text_folder + LETTERS_IMAGE).convert_alpha(),6, 1)
        self.game.lettersx2 = self.separate(pg.image.load(self.text_folder + LETTERS_IMAGE).convert_alpha(),6, 2)
        self.game.lettersx3 = self.separate(pg.image.load(self.text_folder + LETTERS_IMAGE).convert_alpha(),6, 3)
        self.game.lettersx4 = self.separate(pg.image.load(self.text_folder + LETTERS_IMAGE).convert_alpha(),6, 4)
        self.game.teleporthat = self.charge(self.img_folder + TELEPORTHAT_IMAGE).convert_alpha()
        self.game.buttonprimary = self.separate(pg.image.load(self.text_folder + BUTTON_PRIMARY_IMAGE).convert_alpha(),56)
        self.game.buttonsecondary = self.separate(pg.image.load(self.text_folder + BUTTON_SECONDARY_IMAGE).convert_alpha(),36)
        self.game.buttonhat = self.separate(pg.image.load(self.text_folder + BUTTON_HAT_IMAGE).convert_alpha(),31)
        #Coin
        self.game.gemstone_image_bank = self.separate(pg.image.load(self.img_folder + GEMSTONE_IMAGE).convert_alpha(),16, 2)
        self.game.coins_image_bank = self.separate(pg.image.load(self.img_folder + COINS_IMAGE).convert_alpha(),13, 1)
        self.game.coins_image_bankx2 = self.separate(pg.image.load(self.img_folder + COINS_IMAGE).convert_alpha(),13, 2)


    def separate(self, img, w1, mult=1):
        w2 = img.get_width()
        h2 = img.get_height()
        timer = int(w2/w1)
        img_list = []
        img_list_return = []
        for i in range(timer):
            img_list.append(img.subsurface(i*w1, 0, w1, h2))
            img_list[i] = pg.transform.scale(img_list[i], (int(mult*w1), int(mult*h2)))
            wc = int(img_list[i].get_width() * PATCHW)
            hc = int(img_list[i].get_height() * PATCHH)
            img_list_return.append(pg.transform.scale(img_list[i], (wc, hc)))
        return img_list_return

    def wall_construct(self, img, mult=1):
        img_list = []
        for i in img[:3]: #3 * 4 = 12
            img_list.append(i)
            img_list.append(pg.transform.rotate(i, 270))
            img_list.append(pg.transform.rotate(i, 90))
            img_list.append(pg.transform.rotate(i, 180))
        img_list.append(img[3]) # +1
        return img_list

    def charge(self, image_path, mult=1):
        img = pg.image.load(image_path).convert_alpha()
        width = img.get_width()
        height = img.get_height()
        pg.transform.scale(img, (int(mult*width), int(mult*height)))
        wc = int(width * PATCHW)
        hc = int(height * PATCHH)
        return pg.transform.scale(img, (wc, hc))
