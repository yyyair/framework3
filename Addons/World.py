__author__ = 'User'

from Graphics.Actor import Actor
from Graphics.Sprite import Sprite
from Addons.Portal import Portal
from Gameplay.Room import Room
from Utility.Geometry import Rectangle

from Mechanics.CollisionActor import InvisibleWall

# TODO: Make it inherit from subclass Gameplay.Room
class World(Room):
    def __init__(self, game):
        Room.__init__(self, game)
        self.background.material = self.game.loader.get_image("world").convert()
        self.background.material_width = 768
        self.background.material_height = 909
        self.background.crop = (0, 0, 768, 909)
        self.width = 768
        self.height = 909

        self.background.debug = False
        self.background.cache_enabled = True

        self.walls = [Rectangle(65, 92, 128, 20), Rectangle(32, 112, 32, 208), Rectangle(128, 188, 96, 54), Rectangle(289, 92, 95, 54), Rectangle(63, 316, 129, 34)]

    def _setup_walls(self, scene):
        # TODO: Add walls in initalization to room, then listen for an entered_scene event to actually create walls
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

        #portal.target_x, portal.target_y = self.room_coordinates_to_real(portal.target_x, portal.target_y)


