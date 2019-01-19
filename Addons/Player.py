__author__ = 'User'

from Mechanics.CollisionActor import CollisionActor
from Mechanics.Collision import CollisionBox
from Graphics.Sprite import default_animated_sprite, default_walking_animation
from Graphics.Utility import rectangle_surface

from Utility.DataTypes import Direction, Property

class Player(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "player"
        self.add_property(Property.HAS_INVENTORY)
        self.add_property(Property.CAN_INTERACT)
        self.debug = True
        self.log(self.properties)
        # Movement
        self.speed = 0.1
        self.sprinting_speed = 3
        self.walking_speed = 0.1
        self.move_mode = self.move_velocity

        # Sprite
        self.sprite = default_walking_animation()
        self.sprite.material = self.game.loader.get_image("player")
        self.resize(64, 64)

        # Collision
        self.collision_body = CollisionBox(8,16,self.width-16, self.height-16)
        self.collision_body.parent = self


        self.bind_movement_keys()

        self.interact = None


    def bind_movement_keys(self):
        events = self.game.events
        events.listen("key_down_w", lambda e: self.start_move_up(), self)
        events.listen("key_up_w", lambda e: self.stop_move_up(), self)

        events.listen("key_down_s", lambda e: self.start_move_down(), self)
        events.listen("key_up_s", lambda e: self.stop_move_down(), self)

        events.listen("key_down_d", lambda e: self.start_move_right(), self)
        events.listen("key_up_d", lambda e: self.stop_move_right(), self)

        events.listen("key_down_a", lambda e: self.start_move_left(), self)
        events.listen("key_up_a", lambda e: self.stop_move_left(), self)

        events.listen("key_down_space", lambda e: self.start_sprint(), self)
        events.listen("key_up_space", lambda e: self.stop_sprint(), self)

        events.listen("key_up_e", lambda e: print(self.interact) if self.interact is None else self.interact.interact(self))

    def start_move_up(self):
        print("Asdfa")
        self.move_mode(0, -self.speed)
        self.sprite.set_frame("up_1")
        self.sprite.frame_order = ["up_1", "up_2"]
        self.sprite.autoplay = True

    def start_move_down(self):
        self.move_mode(0, self.speed)
        self.sprite.set_frame("down_1")
        self.sprite.frame_order = ["down_1", "down_2"]
        self.sprite.autoplay = True

    def start_move_right(self):
        self.move_mode(self.speed, 0)
        self.sprite.set_frame("right_1")
        self.sprite.frame_order = ["right_1", "right_2"]
        self.sprite.autoplay = True

    def start_move_left(self):
        self.move_mode(-self.speed, 0)
        self.sprite.set_frame("left_1")
        self.sprite.frame_order = ["left_1", "left_2"]
        self.sprite.autoplay = True

    def stop_move_up(self):
        self.move_mode(0, -self.v_y)
        self.sprite.autoplay = not "up_1" in self.sprite.frame_order
        self.find_current_direction(Direction.UP)

    def stop_move_down(self):
        self.move_mode(0, -self.v_y)
        self.sprite.autoplay = not "down_1" in self.sprite.frame_order
        self.find_current_direction(Direction.DOWN)

    def stop_move_right(self):
        self.move_mode(-self.v_x, 0)
        self.sprite.autoplay = not "right_1" in self.sprite.frame_order
        self.find_current_direction(Direction.RIGHT)

    def stop_move_left(self):
        self.move_mode(-self.v_x, 0)
        self.sprite.autoplay = not "left_1" in self.sprite.frame_order
        self.find_current_direction(Direction.LEFT)

    def start_sprint(self):
        self.sprint = True
        self.v_x *= self.sprinting_speed
        self.v_y *= self.sprinting_speed
        self.speed *= self.sprinting_speed
        self.sprite.speed = 2

    def stop_sprint(self):
        self.sprint = False
        self.v_x /= self.sprinting_speed
        self.v_y /= self.sprinting_speed
        self.speed /= self.sprinting_speed
        self.sprite.speed = 1

    def find_current_direction(self, to_ignore):
        keyboard = self.game.keyboard
        if "w" in keyboard.pressed and to_ignore != Direction.UP:
            self.sprite.frame_order = ["up_1", "up_2"]
            self.sprite.autoplay = True
        elif "s" in keyboard.pressed and to_ignore != Direction.DOWN:
            self.sprite.frame_order = ["down_1", "down_2"]
            self.sprite.autoplay = True
        elif "a" in keyboard.pressed and to_ignore != Direction.LEFT:
            self.sprite.frame_order = ["left_1", "left_2"]
            self.sprite.autoplay = True
        elif "d" in keyboard.pressed and to_ignore != Direction.RIGHT:
            self.sprite.frame_order = ["right_1", "right_2"]
            self.sprite.autoplay = True

    def get_inventory_surface(self):
        wrapper = rectangle_surface(512, 64, color=(171, 176, 186), border_width=2)
        item_container = [rectangle_surface(48, 48, color=(121, 125, 132), border_width=1) for i in range(9)]
        for i in range(9):
            wrapper.blit(item_container[i], (8*(i+1) + i * 48, wrapper.get_height()/2 - item_container[i].get_height()/2))
        return wrapper

    def draw(self):
        CollisionActor.draw(self)

        # Draw inventory
        inventory = self.get_inventory_surface()
        self.game.screen.blit(inventory, (self.game.screen.get_width()/2-inventory.get_width()/2,self.game.screen.get_height()-inventory.get_height()-8))

    def update(self):
        CollisionActor.update(self)