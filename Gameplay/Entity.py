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

# Allows an Entity to interact in another by standing in its hitbox.
class InteractionEntity(Entity):
    def __init__(self, game):
        Entity.__init__(self , game)
        self.name = "interaction_entity"
        self.add_property(Property.HAS_INTERACTION)

    # Update the current interaction of the collided player.
    def on_collision(self, obj):
        if obj.has_property(Property.CAN_INTERACT):
            obj.interact = self

    def on_collision_end(self, obj):
        self.log("Collision ended with", obj.name)
        if obj.has_property(Property.CAN_INTERACT) and obj.interact == self:
            obj.interact = None

    def interact(self, obj):
        pass

# An entity that can in theory be controlled and moved
class UnitEntity(Entity):
    pass

# A unit entity that can be interacted, should be used for NPC
class InteractionUnitEntity(UnitEntity, InteractionEntity):
    pass