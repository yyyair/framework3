__author__ = 'User'

from Mechanics.CollisionActor import CollisionActor
from Mechanics.Collision import CollisionBox
from Graphics.Sprite import default_animated_sprite, default_walking_animation
from Graphics.Utility import rectangle_surface
from Utility.Geometry import Point

from Utility.DataTypes import Direction, Property
from Addons.Item import ItemEntity
from Gameplay.Projectile import Projectile

class Player(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "player"
        self.add_property(Property.HAS_INVENTORY)
        self.add_property(Property.CAN_INTERACT)
        self.add_property(Property.CAN_PUSH)
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

        self.inventory = []
        self.inventory_size = 9
        self.selected_slot = -1

        self.direction = Point(0,0)


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

        events.listen("key_down_1", lambda e: self.set_slot(0), self)
        events.listen("key_down_2", lambda e: self.set_slot(1), self)
        events.listen("key_down_3", lambda e: self.set_slot(2), self)
        events.listen("key_down_4", lambda e: self.set_slot(3), self)
        events.listen("key_down_5", lambda e: self.set_slot(4), self)
        events.listen("key_down_6", lambda e: self.set_slot(5), self)
        events.listen("key_down_7", lambda e: self.set_slot(6), self)
        events.listen("key_down_8", lambda e: self.set_slot(7), self)
        events.listen("key_down_9", lambda e: self.set_slot(8), self)

        events.listen("key_down_space", lambda e: self.shoot_projectile(), self)
    def set_slot(self, n):
        self.selected_slot = n
    def start_move_up(self):
        self.move_mode(0, -self.speed)
        self.sprite.set_frame("up_1")
        self.sprite.frame_order = ["up_1", "up_2"]
        self.sprite.autoplay = True
        self.direction.x, self.direction.y = 0, -1

    def start_move_down(self):
        self.move_mode(0, self.speed)
        self.sprite.set_frame("down_1")
        self.sprite.frame_order = ["down_1", "down_2"]
        self.sprite.autoplay = True
        self.direction.x, self.direction.y = 0, 1

    def start_move_right(self):
        self.move_mode(self.speed, 0)
        self.sprite.set_frame("right_1")
        self.sprite.frame_order = ["right_1", "right_2"]
        self.sprite.autoplay = True
        self.direction.x, self.direction.y = 1, 0

    def start_move_left(self):
        self.move_mode(-self.speed, 0)
        self.sprite.set_frame("left_1")
        self.sprite.frame_order = ["left_1", "left_2"]
        self.sprite.autoplay = True
        self.direction.x, self.direction.y = -1, 0

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
        item_container = [rectangle_surface(48, 48, color=(121, 125, 132), border_width=3 if i == self.selected_slot else 1) for i in range(9)]
        dummy_item = ItemEntity(self.game)
        dummy_item.set_position(0,0)
        dummy_item.absolute = True
        for item in self.inventory:
            dummy_item.draw_on(item_container[0])

        for i in range(9):
            wrapper.blit(item_container[i], (8*(i+1) + i * 48, wrapper.get_height()/2 - item_container[i].get_height()/2))
        return wrapper

    def shoot_projectile(self):
        projectile = Projectile(self.game)
        projectile.direction.x, projectile.direction.y = self.direction.x, self.direction.y
        projectile.resize(16,16)
        projectile.set_position(self.x + self.width/2, self.y + self.height/2)
        self.game.get_scene().add(projectile)

    def draw_on(self, surface):
        CollisionActor.draw_on(self, surface)

        # Draw inventory
        inventory = self.get_inventory_surface()
        surface.blit(inventory, (self.game.screen.get_width()/2-inventory.get_width()/2,self.game.screen.get_height()-inventory.get_height()-8))

    def update(self):
        CollisionActor.update(self)