__author__ = 'User'

from Mechanics.CollisionActor import CollisionActor
from Mechanics.Collision import CollisionBox
from Utility.DataTypes import Property

class Portal(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "portal"
        self.height = 64
        self.width = 64

        box = CollisionBox(0, 0, self.width, self.height)
        box.parent = self
        self.collision_body = box

        self.target_x = 223
        self.target_y = 80

    def draw(self):
        pass

    def on_collision(self, obj):
        if not obj.has_property(Property.COLLISION_WALL):
            obj.x = self.target_x
            obj.y = self.target_y

