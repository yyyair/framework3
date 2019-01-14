__author__ = 'User'

from Mechanics.CollisionActor import CollisionActor
from Mechanics.Collision import CollisionBox
from Graphics.Sprite import default_animated_sprite
class Player(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "player"

        # Collision
        self.collision_body = CollisionBox(0,0,self.width, self.height)
        self.collision_body.parent = self

        self.speed = 0.1

        self.bind_movement_keys()

        self.sprite = default_animated_sprite()
        self.sprite.material = self.game.loader.get_image("default")

    def bind_movement_keys(self):
        amount = self.speed
        events = self.game.events
        move_mode = self.move_velocity
        events.listen("key_down_w", lambda e: move_mode(0, -amount), self)
        events.listen("key_up_w", lambda e: move_mode(0, amount), self)

        events.listen("key_down_s", lambda e: move_mode(0, amount), self)
        events.listen("key_up_s", lambda e: move_mode(0, -amount), self)

        events.listen("key_down_d", lambda e: move_mode(amount, 0), self)
        events.listen("key_up_d", lambda e: move_mode(-amount, 0), self)

        events.listen("key_down_a", lambda e: move_mode(-amount, 0), self)
        events.listen("key_up_a", lambda e: move_mode(amount, 0), self)