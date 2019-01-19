__author__ = 'User'

from Graphics.Sprite import Sprite
from Graphics.Scene import SceneComponent
from Mechanics.CollisionActor import InvisibleWall

'''
Implements a game "room".
Each scene contains rooms. Entities can move from room to room.
Every room has walls that cant be moved.
Rooms can be tile based or background-based.
Physics should be consistent from room to room.
'''

class Room(SceneComponent):
    def __init__(self, game):
        SceneComponent.__init__(self, game)
        self.width = 512
        self.height = 512

        self.name = "room"

        self.background = Sprite()
        self.background.material = self.game.loader.get_image("world")
        self.background.material_width, self.background.material_height = 768, 909
        self.background.width, self.background.height = self.width, self.height
        self.background.crop = (0, 0, 768, 909)

        # Cache room background surface for optimization
        self.cache_enabled = True
        self.cache = None

        # List of rectangles
        self.walls = []
        # List of shapes
        self.obstacles = []

        # List of InvisibleWall objects
        self.compiled_walls = []
        # List of collision bodies
        self.compiled_obstacles = []

    # Initialize room stuff
    def setup_room(self, scene, width, height):
        self.log("Setting up")
        self.setup_walls(scene)
        self.resize(width, height)

    # Add wall collision to scene
    def setup_walls(self, scene):
        self.log("Adding walls", self.walls)
        for wall in self.walls:
            self.add_wall(wall.x, wall.y, wall.width, wall.height, scene)

    # Adds obstacle collision to scene
    def setup_obstacles(self, scene):
        pass

    # Resize room
    def resize(self, w, h):
        self.log(self.width, self.height)
        old_w, old_h = self.width,  self.height
        self.width, self.height = w, h
        ratio_w, ratio_h = self.width/old_w, self.height/old_h
        # Update existing walls
        for wall in self.compiled_walls:
            wall.scale(ratio_w, ratio_h)
            wall.set_position(wall.x * ratio_w, wall.y * ratio_h)
        self.background.width, self.background.height = self.width, self.height
        self.cache = None

    # Converts local room coordinates to global screen coordinates
    def room_axis_to_global(self, x, y):
        return x + self.x, y + self.y

    # Converts global screen coordinates to local room coordinates
    def global_axis_to_room(self, x, y):
        return x - self.x, y - self.y

    def add_wall(self, x, y, w, h, scene):
        wall_x, wall_y = self.room_axis_to_global(x, y)
        wall = InvisibleWall(self.game)
        wall.set_position(wall_x, wall_y)
        wall.resize(w, h)
        self.compiled_walls.append(wall)
        scene.add(wall)
        self.log("Added", wall)

    def draw(self):
        camera = self.game.get_scene().camera
        dx = 0 if camera is None else camera.x
        dy = 0 if camera is None else camera.y
        if self.cache_enabled and self.cache is not None:
            self.game.screen.blit(self.cache, (self.x - dx, self.y - dy))
        else:
            surface = self.background.get_surface(dt=0)
            if self.cache_enabled:
                self.cache = surface
            self.game.screen.blit(self.cache, (self.x - dx, self.y - dy))