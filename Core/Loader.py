__author__ = 'User'

import pygame
import json
from Utility.PointerDicts import get_class
from Graphics.Scene import Scene
from Graphics.GUI import GUIManager
from Mechanics.Collision import CollisionManager

class Loader:
    def __init__(self, game):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.game = game
        self.debug = True

    def load_image(self, name, path):
        img = pygame.image.load(path)
        self.images[name] = img

    def load_sound(self, name):
        pass

    def load_font(self, name):
        pass

    def get_image(self, name):
        if name not in self.images:
            return None
        else:
            return self.images[name]

    '''
    Crates a scene from a JSON file. JSON file must have the following fields:
     - name: Scene name
     - type: ???
     - features: Which features (GUI/Collision) the scene requires.
     - graphics: The graphics engine (rooms/tiles/none) for the scene
     - content: A list of game objects to create when initializing the scene
        - name: Component name
        - type: Component type
        - params: Additional component specific parameters
        - path: For include types only

    '''
    def scene_from_file(self, path):
        with open(path) as fp:
            data = json.load(fp)
        if data is None:
            return
        content = []
        self.log("Loading scene %s" % data["name"])
        for item in data["content"]:
            _class = get_class(item["type"])
            _object = None
            if _class is not None:
                _object = _class(self.game)
            if _object is not None:
                for param in item["params"].keys():
                    setattr(_object, param, item["params"][param])
                # Handle x, y, height, width separately because of collision boxes
                x = item["params"]["x"] if "x" in item["params"] else _object.x
                y = item["params"]["y"] if "y" in item["params"] else _object.y
                width = item["params"]["width"] if "width" in item["params"] else _object.width
                height = item["params"]["height"] if "height" in item["params"] else _object.height
                _object.set_position(x,y)
                _object.resize(width, height)

                # Should handle
                content.append(_object)
                self.log("Loaded component %s" % _object)

        s = Scene(self.game)
        s.name = data["name"]
        cm, gm = CollisionManager(self.game), GUIManager(self.game)
        s.setup_scene(gm, cm)
        for c in content:
            s.add(c)

        return s



    def gui_from_file(self, path):
        pass

    def log(self, *msg, ignore_debug=False):
        if ignore_debug or self.debug:
            print("loader: " + " ".join([str(s) for s in msg]))