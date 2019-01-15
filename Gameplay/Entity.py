__author__ = 'User'


from Mechanics.CollisionActor import CollisionActor
from Mechanics.Collision import CollisionBox
from Utility.DataTypes import Property

'''
Any general game object. Can be projectiles, playersm, items.
'''

class Entity(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "entity"
        self.height = 64
        self.width = 64

        # Collision
        box = CollisionBox(0, 0, self.width, self.height)
        box.parent = self
        self.collision_body = box


    def on_collision(self, obj):
        self.log("Collided with %s" % obj.name)
