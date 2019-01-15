__author__ = 'User'

from Graphics.Actor import Actor
from Graphics.Sprite import Sprite
from Addons.Portal import Portal

from Mechanics.CollisionActor import InvisibleWall

# TODO: Make it inherit from subclass Gameplay.Room
class World(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)
        self.sprite = Sprite()
        self.walls = []

        self.sprite.material = self.game.loader.get_image("world").convert()
        self.sprite.material_width = 768
        self.sprite.material_height = 909
        self.sprite.crop = (0, 0, 768, 909)
        self.width = 768
        self.height = 909

        self.sprite.debug = False
        self.sprite.cache_enabled = True

    def update(self):
        Actor.update(self)

    def resize(self, w, h):
        old_w = self.width
        old_h = self.height
        Actor.resize(self, w, h)
        for wall in self.walls:
            wall.resize(wall.width * float(w)/old_w, wall.height * float(h)/old_h)
            wall.set_position(wall.x * w/old_w, wall.y * h / old_h)

    def setup_walls(self, scene):
        wall1 = InvisibleWall(self.game)
        wall1.set_position(65, 92)
        wall1.resize(128, 20)
        self.walls.append(wall1)
        scene.add(wall1)

        wall2 = InvisibleWall(self.game)
        wall2.set_position(32, 112)
        wall2.resize(32, 208)
        self.walls.append(wall2)
        scene.add(wall2)

        self.add_wall(128, 188, 96, 54, scene)
        self.add_wall(289, 92, 95, 54, scene)
        self.add_wall(63, 316, 129, 34, scene)

        portal = Portal(self.game)
        portal.set_position(224, 80)
        portal.resize(33, 14)
        portal.target_x, portal.target_y = 260, 160
        self.walls.append(portal)
        scene.add(portal)

        self.resize(768*3, 909*3)

        portal.target_x, portal.target_y = self.room_coordinates_to_real(portal.target_x, portal.target_y)

    def add_wall(self, x, y, w, h, scene):
        wall = InvisibleWall(self.game)
        wall.set_position(x, y)
        wall.resize(w, h)
        self.walls.append(wall)
        scene.add(wall)

    def room_coordinates_to_real(self, x, y):
        return x * self.width/self.sprite.material_width, y * self.height/self.sprite.material_height
