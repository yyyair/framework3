__author__ = 'User'

from Graphics.Scene import SceneComponent

class Actor(SceneComponent):
    def __init__(self, game):
        SceneComponent.__init__(self, game)
        self.name = "base_actor"
        self.sprite = None
        self.height = 32
        self.width = 32

        self.debug = False

    def draw(self):
        #self.log("%s being drawn!" % self.name)
        if self.sprite is None:
            return
        surface = self.sprite.get_surface(dt=self.game.clock.get_time())
        self.game.screen.blit(surface, (self.x, self.y))
