__author__ = 'User'
from Core.Component import ComponentManager
import pygame
from Utility.Geometry import Rectangle, Point
from Graphics.Utility import rectangle_surface
from Utility.DataTypes import Property

class CollisionBody:
    def __init__(self):
        self.parent = None
        self.mass = 0
        self.solid = True

    def collides(self, body):
        return False

    def draw_surface(self):
        pass

    def center_of_mass(self):
        return Point(0,0)

    def resize(self, *args):
        pass


class CollisionBox(Rectangle, CollisionBody):
    def __init__(self, x,y,w,h):
        Rectangle.__init__(self,x,y,w,h)
        CollisionBody.__init__(self)

        self.debug_surface = rectangle_surface(self.width, self.height, color=(255,255,255,128))

    def center_of_mass(self):
        return Point(self.x+self.width/2, self.y+self.height/2)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def resize(self, w, h):
        self.height = h
        self.width = w
        if self.parent is None:
            self.debug_surface = rectangle_surface(self.width, self.height, color=(255,255,255,128))
        elif  self.parent.has_property(Property.COLLISION_WALL):
            self.debug_surface = rectangle_surface(self.width, self.height, color=(0,255,0,128))
        else:
            self.debug_surface = rectangle_surface(self.width, self.height, color=(255,255,255,128))


    def collides(self, body):
        # Box-Box collision
        if isinstance(body, CollisionBox):
            # Update relative locations
            real_body_x = body.x
            real_body_y = body.y
            if body.parent is not None:
                body.x += body.parent.x
                body.y += body.parent.y

            real_self_x = self.x
            real_self_y = self.y
            if self.parent is not None:
                self.x += self.parent.x
                self.y += self.parent.y
            # Check for collision
            for v in self.get_vertices():
                if v in body:
                    self.x, self.y = real_self_x, real_self_y
                    body.x, body.y = real_body_x, real_body_y
                    return True
            for v in body.get_vertices():
                if v in self:
                    self.x, self.y = real_self_x, real_self_y
                    body.x, body.y = real_body_x, real_body_y
                    return True
            self.x, self.y = real_self_x, real_self_y
            body.x, body.y = real_body_x, real_body_y
        return False


class CollisionManager(ComponentManager):
    def __init__(self, game):
        ComponentManager.__init__(self, game)
        self.name = "collision_manager"
        # Components that can go through others
        self.ghosts = []
        # Draw all collision bodies for debug
        self.debug_draw = True

        self.debug = False

        # Save a cache of collisions to detect changes
        self.collisions = []


    def update(self):
        # Check collisions


        collisions = []

        # Ignore walls since they are handled on movement
        candidates = [c for c in self.components if not c.has_property(Property.COLLISION_WALL)]
        c_num = len(candidates)
        for i in range(c_num):
            for j in range(i+1, c_num):

                # If something collision related doesn't work, this might cause it
                if candidates[i].has_property(Property.COLLISION_WALL) and candidates[j].has_property(Property.COLLISION_WALL):
                    continue

                c_1 = candidates[i].collision_body
                c_2 = candidates[j].collision_body
                if c_1 is None or c_2 is None:
                    self.log("wow")
                elif c_1.collides(c_2):
                    self.log("(%s, %s) collision" % (c_1.parent.name, c_2.parent.name))
                    collisions.append((candidates[i], candidates[j]))

        for collision in collisions:
            c1, c2 = collision[0], collision[1]
            if c1 is None or c2 is None or c1.name == "dead" or c2.name == "dead":
                self.log("bad")
                continue
            c1.on_collision(c2)
            c2.on_collision(c1)

        for collision in [c for c in self.collisions if c not in collisions]:
            c1, c2 = collision[0], collision[1]
            if c1 is None or c2 is None or c1.name == "dead" or c2.name == "dead":
                self.log("bad")
                continue
            c1.on_collision_end(c2)
            c2.on_collision_end(c1)

        self.collisions = [(c[0], c[1]) for c in collisions if c[0].name != "dead" and c[1].name != "dead"]

    # Returns all
    def find_collisions_by_component(self, body, filter=None, max_amount=float("inf")):
        collisions = []
        candidates = self.components if filter is None else [c for c in self.components if filter(c)]
        c_1 = body.collision_body


        for c in candidates:
            c_2 = c.collision_body
            if c_1 is not None and c_2 is not None and c != body:
                if c_1.collides(c_2):
                    collisions.append((c_1, c_2))
                    if len(collisions) >= max_amount:
                        return collisions

        return collisions

    def draw(self):
        if not self.debug_draw:
            return
        for c in self.components:
            collision_body = c.collision_body
            if collision_body is None:
                pass
            elif isinstance(collision_body, CollisionBox):
                camera = self.game.get_scene().camera
                if camera is not None:
                    x = collision_body.parent.x + collision_body.x - camera.x
                    y = collision_body.parent.y + collision_body.y - camera.y
                    self.game.screen.blit(collision_body.debug_surface, (x, y))