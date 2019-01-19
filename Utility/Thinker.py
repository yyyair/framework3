__author__ = 'User'

from Core.Component import GameComponent

'''
Component to be used in order to add in runtime methods to be run every tick
'''

class Thinker(GameComponent):
    def __init__(self, game, method):
        GameComponent.__init__(self, game)
        self.name = "thinker"
        self.method = method

    def think(self):
        self.method()

    def update(self):
        if not self.dead:
            self.think()

# Thinks every few milliseconds
class IntervalThinker(Thinker):
    def __init__(self, game, method):
        Thinker.__init__(self, game, method)
        self.name = "interval_thinker"

        self.interval_length = 1
        self.time_since_last = 0

    def think(self, dt=0):
        self.time_since_last += dt
        if self.time_since_last > self.interval_length:
            self.time_since_last = 0
            Thinker.think(self)

    def update(self):
        if not self.dead:
            self.think(dt=self.game.clock.get_time())
