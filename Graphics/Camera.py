__author__ = 'User'


class Camera:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.zoom = 1
        self.angle = 0

        self.locked = False
        self.following = None

    def set_position(self, x, y):
        self.x = x
        self.y = y