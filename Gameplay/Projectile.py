__author__ = 'User'

'''
Implements an Entity that moves on its own according to a pre-determined path.
'''

from Gameplay.Entity import Entity
from Utility.Geometry import Point

class Projectile(Entity):
    def __init__(self, game):
        Entity.__init__(self, game)
        self.name = "projectile"

        # How much time the projectile has until it is removed from the game
        self.ttl = 2500
        # How far can the projectile go
        self.max_distance = 1000

        self.time_lived = 0
        self.distance_traveled = 0

        # Direction and speed of projectile
        self.direction = Point(0,1)
        self.speed = 5

        # Can the projectile hit multiple people?
        self.multiple = False

        # Can the projectile hit the same entity twice?
        self.repeat = False
        self.history = []

        # Which types should the projectile hit? Should be properties.
        self.targets = []


    def update(self):
        # Check if should kill projectile
        if self.time_lived > self.ttl or self.max_distance < self.distance_traveled:
            self.log("I should die")
            self.kill()
            pass

        self.time_lived += self.game.clock.get_time()

        current_location = Point(self.x,self.y)
        next_location = current_location + self.direction * self.speed
        self.distance_traveled += current_location.distance(next_location)
        self.set_position(next_location.x, next_location.y)

        Entity.update(self)




