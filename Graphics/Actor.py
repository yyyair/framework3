__author__ = 'User'

from Graphics.Scene import SceneComponent, Scene
from Utility.DataTypes import PositionType
class Actor(SceneComponent):
    def __init__(self, game):
        SceneComponent.__init__(self, game)
        self.name = "base_actor"
        self.sprite = None
        self.height = 32
        self.width = 32
        self.position_type = PositionType.RELATIVE

        self.debug = False

        # Scaling when resizing
        self.scale_width = True
        self.scale_height = True

        # Cache the actor surface
        self.cache = True
        self.update_cache = True
        self.cache_surface = None

    def draw(self):
        self.draw_on(self.game.screen)

    def draw_on(self, _surface):
        camera = self.game.get_scene().camera
        # Try to get suface from cache or create a new one
        surface = None
        if self.cache and not self.update_cache and self.cache_surface is not None:
            surface = self.cache_surface
        elif self.sprite is not None:
            surface = self.sprite.get_surface(dt=self.game.clock.get_time())

        if surface is None:
            self.log("Can't draw, no surface")
            return

        if self.position_type == PositionType.ABSOLUTE or camera is None:
            _surface.blit(surface, (self.x, self.y))
        else:
            _surface.blit(surface, (self.x-camera.x, self.y-camera.y))

    def get_cache(self):
        return self.cache_surface

    def set_cache(self, surface):
        self.log("Updated cache")
        self.cache_surface = surface
        self.update_cache = False

    def resize(self, w, h):
        self.width = w
        self.height = h
        if self.sprite is not None:
            self.sprite.width = w
            self.sprite.height = h
        self.update_cache = True

    def scale(self, xratio, yratio):
        new_width = self.width if not self.scale_width else self.width * xratio
        new_height = self.height if not self.scale_height else self.height * yratio
        self.resize(new_width, new_height)
