import pygame as pg
from settings import *
from tools import *

class Inventory(pg.sprite.Sprite):
    def __init__(self, game, player):
        self.groups =  game.inventory
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image_bank = self.game.inventory_image_bank
        self.image = self.image_bank[0].copy()
        self.image_dealer = self.image_bank[1].copy()
        self.image.set_alpha(200)
        self.display = False
        self.toggletimer = 0

        self.priminvslots = PRIMINVSLOTS
        self.secondinvslots = SECONDINVSLOTS
        self.hatinvslots = HATINVSLOTS
        self.clicked = False

        self.sellingitemprimary = SELLINGITEMPRIMARY
        self.priceitemprimary = PRICEITEMPRIMARY
        self.sellingitemsecondary = SELLINGITEMSECONDARY
        self.priceitemsecondary = PRICEITEMSECONDARY
        self.sellingitemhat = SELLINGITEMHAT
        self.priceitemhat = PRICEITEMHAT

        #button



        self.invprimarybutton = []
        self.invsecondarybutton = []
        self.invhatbutton = []
        self.invprimarydealerbutton = []
        self.invsecondarydealerbutton = []
        self.invhatdealerbutton = []

        true = self.game.buttonprimary[0]
        false = self.game.buttonprimary[1]
        self.invprimarybutton.append(Button(self.game, false, true, (XSLOT1_BUTTON, YSLOT1_BUTTON)))
        self.invprimarybutton.append(Button(self.game, false, true, (XSLOT2_BUTTON, YSLOT2_BUTTON)))

        for i in range(15):
            #true et false sont deja bien set (juste avant)
            self.invprimarydealerbutton.append(Button(self.game, false, true, (886*PATCHW  + INVENTORYX + (i%5) * ECART_PX , 67 * PATCHH + INVENTORYY  + (i// 5) * ECART_PY)))

        for i in range(3):
            #true et false sont deja bien set (juste avant)
            self.invprimarybutton.append(Button(self.game, false, true, (INVENTORY_PLAYER_PRIMARY_X  + INVENTORYX - 4 * PATCHW + i * ECART_PX , INVENTORY_PLAYER_PRIMARY_Y + INVENTORYY -3 * PATCHH)))

        true = self.game.buttonsecondary[0]
        false = self.game.buttonsecondary[1]
        self.invsecondarybutton.append(Button(self.game, false, true, (XSLOT3_BUTTON, YSLOT3_BUTTON)))

        for i in range(2):
            self.invsecondarybutton.append(Button(self.game, false, true, (INVENTORY_PLAYER_SECONDARY_X + INVENTORYX - 4 * PATCHW + i * ECART_SX, INVENTORY_PLAYER_SECONDARY_Y + INVENTORYY - 3 * PATCHH )))

        for i in range(6):
            self.invsecondarydealerbutton.append(Button(self.game, false, true, (885 * PATCHW  + INVENTORYX  + i * (ECART_SX+5) , 255 * PATCHH + INVENTORYY )))


        true = self.game.buttonhat[0]
        false = self.game.buttonhat[1]
        self.invhatbutton.append(Button(self.game, false, true, (XSLOT4_BUTTON, YSLOT4_BUTTON)))
        for i in range(3):
            self.invhatbutton.append(Button(self.game, false, true, (INVENTORY_PLAYER_HAT_X + INVENTORYX - 2 * PATCHW + i * ECART_HX, INVENTORY_PLAYER_HAT_Y + INVENTORYY - 6 * PATCHH)))

        for i in range(8):
            self.invhatdealerbutton.append(Button(self.game, false, true, (885 *PATCHW + INVENTORYX + i * ECART_HX , INVENTORYY + 325 *  PATCHH)))


    def number_translate(game, number, bank):
        number_str = str(number)
        image = pg.Surface((len(number_str)*bank[0].get_width(),bank[0].get_height()), pg.SRCALPHA)
        image.set_alpha(0)
        for i in enumerate(number_str):
            image.blit(bank[int(i[1])],(i[0]*bank[0].get_width(), 0))
        return image

    def update(self):
        self.toggletimer += 1
        if self.player.keys[pg.K_TAB] and self.toggletimer > MAXIMUM_TIME_TOGGLETIMER:
            if self.display:
                self.display = False
                self.game.wavelaunch_stat = False
            else:
                self.display = True
            self.toggletimer = 0

    def draw_inventory(self):
        self.invprimarybutton_stat = []
        self.invsecondarybutton_stat = []
        self.invhatbutton_stat = []
        if self.display:
            for i in self.invprimarybutton:
                self.invprimarybutton_stat.append(i.action())
            for i in self.invsecondarybutton:
                self.invsecondarybutton_stat.append(i.action())
            for i in self.invhatbutton:
                self.invhatbutton_stat.append(i.action())
            self.image_new = self.image.copy()
            self.draw_stats()
            self.draw_item()
            self.draw_stockinventory()
            self.game.window.blit(self.image_new, (INVENTORYX,INVENTORYY))

            if self.game.dealer.detectstat:
                self.draw_inventory_dealer()

            for index, i in enumerate(self.invprimarybutton_stat):
                if i:
                    self.clickeded(self.priminvslots[index], index, "primary")
                    self.invprimarybutton_stat[index] = False

            for index, i in enumerate(self.invsecondarybutton_stat):
                if i:
                    self.clickeded(self.secondinvslots[index], index, "secondary")
                    self.invsecondarybutton_stat[index] = False

            for index, i in enumerate(self.invhatbutton_stat):
                if i:
                    self.clickeded(self.hatinvslots[index], index, "hat")
                    self.invhatbutton_stat[index] = False


    def clickeded(self, item, slot, type):
        if not self.clicked:
            self.item_drag = item
            self.origin = slot
            self.origintype = type
            self.clicked = True
        else:
            if self.origintype == type: #Pour vérifier qu'on peut bien intervertire les items
                if self.origintype == "primary":
                    self.priminvslots[self.origin] = item
                    self.priminvslots[slot] = self.item_drag
                    self.clicked = False

                if self.origintype == "secondary":
                    self.secondinvslots[self.origin] = item
                    self.secondinvslots[slot] = self.item_drag
                    self.clicked = False

                if self.origintype == "hat":
                    self.hatinvslots[self.origin] = item
                    self.hatinvslots[slot] = self.item_drag
                    self.clicked = False

    def draw_stockinventory(self):
        for i in range(3):
            if self.priminvslots[i+2] != None:
                self.image_new.blit((self.test(self.priminvslots, i+2)), (INVENTORY_PLAYER_PRIMARY_X + ECART_PX * i, INVENTORY_PLAYER_PRIMARY_Y))
        for i in range(2):
            if self.secondinvslots[i+1] != None:
                self.image_new.blit((self.test(self.secondinvslots, i+1)), (INVENTORY_PLAYER_SECONDARY_X + ECART_SX * i, INVENTORY_PLAYER_SECONDARY_Y))
        for i in range(3):
            if self.hatinvslots[i+1] != None:
                self.image_new.blit((self.test(self.hatinvslots, i+1)), (INVENTORY_PLAYER_HAT_X + ECART_HX * i, INVENTORY_PLAYER_HAT_Y ))

    def draw_inventory_dealer(self):
        self.invprimarydealerbutton_stat = []
        self.invsecondarydealerbutton_stat = []
        self.invhatdealerbutton_stat = []

        for i in self.invprimarydealerbutton:
            self.invprimarydealerbutton_stat.append(i.action())
        for i in self.invsecondarydealerbutton:
            self.invsecondarydealerbutton_stat.append(i.action())
        for i in self.invhatdealerbutton:
            self.invhatdealerbutton_stat.append(i.action())

        for index, i in enumerate(self.invprimarydealerbutton_stat):
            if i and self.sellingitemprimary[index] != None:
                self.game.dealer.selling(index, 'primary')
        for index, i in enumerate(self.invsecondarydealerbutton_stat):
            if i and self.sellingitemsecondary[index] != None:
                self.game.dealer.selling(index, 'secondary')
        for index, i in enumerate(self.invhatdealerbutton_stat):
            if i and self.sellingitemhat[index] != None:
                self.game.dealer.selling(index, 'hat')


        self.image_new_dealer = self.image_dealer.copy()

        for i in range(len(self.sellingitemprimary)):
            if self.sellingitemprimary[i] != None:
                self.image_new_dealer.blit((self.test(self.sellingitemprimary, i)), (INVENTORY_DEALER_PRIMARY_X + ECART_PX * (i%5), INVENTORY_DEALER_PRIMARY_Y + ECART_PY * ((i) // 5)))
                self.image_new_dealer.blit(Inventory.number_translate(self.game, self.priceitemprimary[i], self.game.numbersx2), (INVENTORY_DEALER_PRIMARY_X + ECART_PX * (i%5), INVENTORY_DEALER_PRIMARY_Y + 50 * PATCHH + ECART_PY * ((i) // 5)))
        for i in range(len(self.sellingitemsecondary)):
            if self.sellingitemsecondary[i] != None:
                self.image_new_dealer.blit((self.test(self.sellingitemsecondary, i)), (INVENTORY_DEALER_PRIMARY_X + (ECART_SX+5) * (i%5), 258 * PATCHH))
                self.image_new_dealer.blit(Inventory.number_translate(self.game, self.priceitemsecondary[i], self.game.numbersx2), (INVENTORY_DEALER_PRIMARY_X + (ECART_SX+5) * (i%5), 304 * PATCHH ))
        for i in range(len(self.sellingitemhat)):
            if self.sellingitemhat[i] != None:
                self.image_new_dealer.blit((self.test(self.sellingitemhat, i)), (INVENTORY_DEALER_PRIMARY_X + ECART_HX * (i%5), 328 * PATCHH))
                self.image_new_dealer.blit(Inventory.number_translate(self.game, self.priceitemhat[i], self.game.numbersx2), (INVENTORY_DEALER_PRIMARY_X + ECART_HX * (i%5), 365 * PATCHH ))
        self.game.window.blit(self.image_new_dealer, (INVENTORY_DEALER_X,INVENTORY_DEALER_Y))

    def draw_item(self):
        if self.priminvslots[0] != None:
            self.image_slot1 = self.test(self.priminvslots, 0)
            self.image_slot1 = pg.transform.flip(self.image_slot1, True, False)
            self.image_new.blit(self.image_slot1, (IS_IMAGE_SLOT1_X, IS_IMAGE_SLOT1_Y))
        #2
        if self.priminvslots[1] != None:
            self.image_slot2 = self.test(self.priminvslots, 1)
            self.image_new.blit(self.image_slot2, (IS_IMAGE_SLOT2_X, IS_IMAGE_SLOT2_Y))
        #3
        if self.secondinvslots[0] != None:
            self.image_slot3 = self.test(self.secondinvslots, 0)
            self.image_new.blit(self.image_slot3, (IS_IMAGE_SLOT3_X, IS_IMAGE_SLOT3_Y))
        #4
        if self.hatinvslots[0] != None:
            self.image_slot4 = self.test(self.hatinvslots, 0)
            self.image_new.blit(self.image_slot4, (IS_IMAGE_SLOT4_X, IS_IMAGE_SLOT4_Y))

    def test(self, inventory, slot):
        if inventory[slot] == "Gold45":
            return self.game.gold45_image_bank[0]
        elif inventory[slot] == "Wavax":
            return self.game.wavax_image_bank[0]
        elif inventory[slot] == "Aspirator":
            return self.game.aspirator_image_bank[4]
        elif inventory[slot] == "Teleport_Hat":
            return self.game.teleporthat

    def draw_stats(self):
        d = DISTANCE_NUMBER
        self.coins_image_number = Inventory.number_translate(self.game, self.game.player.coins, self.game.numbersx2)
        self.gemstone_image_number = Inventory.number_translate(self.game, self.game.player.gemstone, self.game.numbersx2)
        self.wall_use_image_number = Inventory.number_translate(self.game, self.game.player.wall_use, self.game.numbersx2)
        height = IS_STATS + self.game.coins_image_bankx2[0].get_height() - self.coins_image_number.get_height() - 5*PATCHW
        self.image_new.blit(self.game.coins_image_bankx2[0], (IS_COINS, IS_STATS))
        self.image_new.blit(self.coins_image_number, (IS_COINS+d+self.game.coins_image_bankx2[0].get_width(), height))
        self.image_new.blit(self.game.gemstone_image_bank[0], (IS_LVL, IS_STATS))
        self.image_new.blit(self.gemstone_image_number, (IS_LVL+d+self.game.gemstone_image_bank[0].get_width(), height))
        self.image_new.blit(self.game.wall_inventory_image[0], (IS_WALL, IS_STATS))
        self.image_new.blit(self.wall_use_image_number, (IS_WALL+d+self.game.wall_inventory_image[0].get_width(), height))
