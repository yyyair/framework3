__author__ = 'User'

from Graphics.Scene import SceneComponent, Scene

class Actor(SceneComponent):
    def __init__(self, game):
        SceneComponent.__init__(self, game)
        self.name = "base_actor"
        self.sprite = None
        self.height = 32
        self.width = 32
        self.absolute = False

        self.debug = False

        # Scaling when resizing
        self.scale_width = True
        self.scale_height = True

    def draw(self):
        #self.log("%s being drawn!" % self.name)
        if self.sprite is None:
            return
        surface = self.sprite.get_surface(dt=self.game.clock.get_time())
        camera = self.game.get_scene().camera
        if self.absolute or camera is None:
            self.game.screen.blit(surface, (self.x, self.y))
        else:
            self.game.screen.blit(surface, (self.x-camera.x, self.y-camera.y))

    def resize(self, w, h):
        self.width = w
        self.height = h
        if self.sprite is not None:
            self.sprite.width = w
            self.sprite.height = h

    def scale(self, xratio, yratio):
        new_width = self.width if not self.scale_width else self.width * xratio
        new_height = self.height if not self.scale_height else self.height * yratio
        self.resize(new_width, new_height)
