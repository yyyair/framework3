__author__ = 'User'

from Graphics.Scene import SceneComponent

class Camera(SceneComponent):
    def __init__(self, game):
        SceneComponent.__init__(self, game)
        self.zoom = 1
        self.angle = 0