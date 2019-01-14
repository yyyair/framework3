__author__ = 'User'
from Core.Component import ComponentManager
import pygame
from Utility.Geometry import Rectangle, Point
class CollisionBody:
    def __init__(self):
        self.parent = None
        self.mass = 0

    def collides(self, body):
        return False

    def draw_surface(self):
        pass

    def center_of_mass(self):
        return Point(0,0)


class CollisionBox(Rectangle, CollisionBody):
    def __init__(self, x,y,w,h):
        Rectangle.__init__(self,x,y,w,h)
        CollisionBody.__init__(self)

    def center_of_mass(self):
        return Point(self.x+self.width/2, self.y+self.height/2)


    def collides(self, body):
        # Box-Box collision
        if isinstance(body, CollisionBox):
            # Update relative locations
            if body.parent is not None:
                body.x = body.parent.x
                body.y = body.parent.y
            if self.parent is not None:
                self.x = self.parent.x
                self.y = self.parent.y
            # Check for collision
            for v in self.get_vertices():
                if v in body:
                    return True
            for v in body.get_vertices():
                if v in self:
                    return True

        return False

class CollisionManager(ComponentManager):
    def __init__(self, game):
        ComponentManager.__init__(self, game)
        self.name = "collision_manager"
        # Components that can go through others
        self.ghosts = []
        # Draw all collision bodies for debug
        self.debug_draw = True


    def update(self):
        # Check collisions

        c_num = len(self.components)
        for i in range(c_num):
            for j in range(i+1, c_num):

                c_1 = self.components[i].collision_body
                c_2 = self.components[j].collision_body
                if c_1 is None or c_2 is None:
                    self.log("wow")
                elif c_1.collides(c_2):
                    self.log("(%s, %s) collision" % (c_1.parent.name, c_2.parent.name))

    # Returns all
    def find_collisions_by_component(self, body, filter=None):
        collisions = []
        candidates = self.components if filter is None else [c for c in self.components if filter(c)]
        c_1 = body.collision_body

        for c in candidates:
            c_2 = c.collision_body
            if c_1 is not None and c_2 is not None and c != body:
                if c_1.collides(c_2):
                    collisions.append((c_1, c_2))

        return collisions

    def draw(self):
        if not self.debug_draw:
            return
        for c in self.components:
            collision_body = c.collision_body
            if collision_body is None:
                pass
            '''
            elif collision_body.debug_draw is not None:
                x = c.x
                y = c.y
                #self.game.blit(collision_body.debug_draw, (x,y))
            '''