__author__ = 'User'

from Gameplay.Entity import Entity
from Utility.DataTypes import Property
from Graphics.Sprite import Sprite

class ItemEntity(Entity):
    def __init__(self, game):
        Entity.__init__(self, game)
        self.name = "item"
        # Item ID
        self.id = -1

        # Setup sprite
        self.sprite = Sprite()
        self.sprite.material = self.game.loader.get_image("items")
        self.sprite.material_width = self.sprite.material_height = 16
        self.sprite.crop = (160,17,16,16)
        self.resize(32, 32)
        self.debug = True
        # Stack count
        self.count = 1

    def on_collision(self, obj):
        self.log(obj.properties, obj.name)
        if obj.has_property(Property.HAS_INVENTORY):
            self.log("sudoku2")
            if not self.dead:

                self.kill()