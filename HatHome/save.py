import json
import os

class Save_game:
    def __init__(self, game):
        self.game = game

    def save_content(self):
        data_json = {}
        data_json['volumes'] = {
        "general": self.game.volume,
        "music": self.game.volumemusic,
        "sound": self.game.volumesounds,
        }
        data_json['settings'] = {
        "resolution": (self.game.width, self.game.height)
        }
        data_json['ship'] = {
        "life" : self.game.ship.life,
        "max_life" : self.game.ship.max_life
        }
        data_json['wave'] = {
        "selectwave" : self.game.master_mind.waveacupdate
        }
        data_json['player'] = {
        "life" : self.game.player.life,
        "selectgun" : self.game.player.selectgun,
        "experience_max": self.game.player.experience_max,
        "experience": self.game.player.experience
        }
        data_json['inventory'] = {
        "coins": self.game.player.coins,
        "gemstone": self.game.player.gemstone,
        "walls": self.game.player.wall_use,

        "priminvslots": self.game.player.inventory.priminvslots,
        "secondinvslots": self.game.player.inventory.secondinvslots,
        "hatinvslots": self.game.player.inventory.hatinvslots,

        "sellingitemprimary": self.game.player.inventory.sellingitemprimary,
        "priceitemprimary": self.game.player.inventory.priceitemprimary,
        "sellingitemsecondary": self.game.player.inventory.sellingitemsecondary,
        "priceitemsecondary": self.game.player.inventory.priceitemsecondary,
        "sellingitemhat": self.game.player.inventory.sellingitemhat,
        "priceitemhat": self.game.player.inventory.priceitemhat
        }

        data = json.dumps(data_json, indent=2)

        with open("HatHome song\\save_file.txt", "w") as file:
            file.write(data)
