__author__ = 'User'

import math

# An object located in space
class SpaceObject:
    def __init__(self):
        self.x = 0
        self.y = 0

    def __str__(self):
        return "(%s,%s)" % (self.x, self.y)

class Point(SpaceObject):
    def __init__(self, x, y):
        SpaceObject.__init__(self)
        self.x = x
        self.y = y

    def distance(self, point):
        return ((self.x-point.x)**2 + (self.y-point.y)**2)**0.5

    def distance_sq(self, point):
        return (self.x-point.x)**2 + (self.y-point.y)**2

    def norm(self, point):
        return self.x**2 + self.y**2

    def angle(self, reference_point):
        if reference_point.x == self.x:
            return math.pi/2
        else:
            return math.atan((self.y - reference_point.y)/(self.x - reference_point.x))

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

class Rectangle(SpaceObject):
    def __init__(self,x ,y, width, height):
        SpaceObject.__init__(self)

        # Location of the upper-left vertex
        self.x = x
        self.y = y

        self.width = width
        self.height = height

    def get_center(self):
        return Point(self.x + self.width/2, self.y + self.height/2)

    def get_vertices(self):
        return [Point(self.x, self.y),
                Point(self.x + self.width, self.y),
                Point(self.x, self.y + self.height),
                Point(self.x + self.width, self.y + self.height)]

    def move_center(self, dx, dy):
        self.x += dx
        self.y += dy

    def set_center(self, x, y):
        self.x = x - self.width/2
        self.y = y - self.height/2

    def __contains__(self, point):
        return self.x <= point.x <= self.x+self.width and self.y <= point.y <= self.y + self.height

    def __str__(self):
        return "%sx%s at (%s,%s)" % (self.width, self.height, self.x, self.y)

# Rectangle that can rotate
class AngledRectangle(Rectangle):
    def __init__(self, x, y, width, height):
        Rectangle.__init__(self, x, y, width, height)
        self.angle = 0

# Triangle
class Triangle:
    pass

class Circle:
    pass

# A more complex shape, composed from smaller ones
class ShapeBundle:
    pass

class Vector2D:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def set_start(self, point):
        self.start = point

    def set_end(self, point):
        self.end = point

    def angle(self):
        return self.end.angle(self.start)

    def rotate(self, angle):
        pass

    def __add__(self, other):
        return Vector2D(self.start+other.start, self.end+other.end)

    def __sub__(self, other):
        return Vector2D(self.start-other.start, self.end-other.end)

    def __mul__(self, other):
        return Vector2D(other*self.star, other*self.end)
