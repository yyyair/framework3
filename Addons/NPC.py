__author__ = 'User'

from Gameplay.Entity import InteractionEntity
from Graphics.Sprite import Sprite
from Mechanics.CollisionActor import InvisibleWall

class NPC(InteractionEntity):
    def __init__(self, game):
        InteractionEntity.__init__(self , game)
        self.name = "npc_entity"
        self.debug = True

        self.sprite = Sprite()
        self.sprite.material = game.loader.get_image("pikachu")
        self.sprite.crop = (32, 96, 32, 32)
        self.resize(64, 64)

        self.collision_body.set_position(0, 8)

        self.border = InvisibleWall(self.game)
        self.border.resize(32, 32)
        self.border.set_position(16, 24)
        self.border.name = self.name + "_fake_wall"

        self.game.get_scene().add(self.border)

    def set_position(self, x, y):
        dx, dy = x - self.x, y - self.y
        InteractionEntity.set_position(self, x, y)
        self.border.set_position(self.border.x + dx, self.border.y + dy)
    def interact(self, obj):
        self.log("Interacted with ", obj.name)

        # Dialog testing tmp


    def update(self):
        pass
        #self.log(self.border.x, self.border.y)

    def on_created(self):
        self.parent.add(self.border)
