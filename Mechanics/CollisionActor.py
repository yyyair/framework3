__author__ = 'User'

from Graphics.Actor import Actor
from Utility.DataTypes import Property
from Mechanics.Collision import CollisionBody, CollisionBox
from Graphics.Sprite import Sprite


class CollisionActor(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)
        self.collision_body = CollisionBody()
        self.collision_body.parent = self
        self.name = "collision_actor"

        if Property.COLLISION not in self.properties:
            self.properties.append(Property.COLLISION)

    def on_collision(self, obj):
        pass

    def on_collision_end(self, obj):
        pass

    def move_position(self, dx, dy):
        # Currently prevents player from walking into walls
        collision = self.collision_body.parent.parent
        if collision is None:
            Actor.move_position(self, dx, dy)
        else:
            if dx != 0:
                Actor.move_position(self, dx, 0)
                collisions = collision.find_collisions_by_component(self, lambda c: c.has_property(Property.COLLISION_WALL), 1)
                if len(collisions) > 0:
                    Actor.move_position(self, -dx, 0)
            if dy != 0:
                Actor.move_position(self, 0, dy)
                collisions = collision.find_collisions_by_component(self, lambda c: c.has_property(Property.COLLISION_WALL), 1)
                if len(collisions) > 0:
                    Actor.move_position(self, 0, -dy)

    def resize(self, w, h):
        Actor.resize(self, w, h)
        if self.collision_body is not None:
            if isinstance(self.collision_body, CollisionBox):
                self.collision_body.resize(w, h)


class Wall(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.height = 64
        self.width = 128
        self.add_property(Property.COLLISION_WALL)

        box = CollisionBox(0, 0, self.width, self.height)
        box.parent = self
        self.collision_body = box


        # Setup sprite
        sprite = Sprite()
        sprite.material = self.game.loader.get_image("wall")
        sprite.height = self.height
        sprite.width = self.width

        sprite.material_height = 48
        sprite.material_width = 48
        sprite.crop = (0,0,48,48)
        self.sprite = sprite

class InvisibleWall(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "invis_wall"
        self.height = 64
        self.width = 64
        self.add_property(Property.COLLISION_WALL)

        box = CollisionBox(0, 0, self.width, self.height)
        box.parent = self
        self.collision_body = box

    def draw(self):
        pass