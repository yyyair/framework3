__author__ = 'User'

from Gameplay.Entity import Entity
from Graphics.Sprite import default_sprite
from Utility.DataTypes import Property
from Mechanics.CollisionActor import InvisibleWall

class PushableEntity(Entity):
    def __init__(self, game):
        Entity.__init__(self, game)
        self.properties.append(Property.CAN_PUSH)
        self.sprite = default_sprite()
        self.pusher = None
        self.debug = True

        self.border = InvisibleWall(self.game)
        self.border.resize(56, 56)
        self.border.set_position(2, 2)
        self.border.name = self.name + "_fake_wall"
        self.border.ignore.append(self)

        self.game.get_scene().add(self.border)
        self.border.scale(0.5, 0.5)
        self.scale(0.5, 0.5)

        self.allow_pull = False

    def on_collision(self, obj):
        #self.log(obj)
        if obj.has_property(Property.CAN_PUSH):
            test_x = lambda o: o.collision_body.center_of_mass().x + o.x
            test_y = lambda o: o.collision_body.center_of_mass().y + o.y
            sgn = lambda x: 1 if x > 0 else -1 if x < 0 else 0
            #print("%s == %s = %s", (sgn(self.v_y), sgn(test_y(self) - test_y(obj)), (sgn(self.v_y) == sgn(test_y(self) - test_y(obj)))))
            if (sgn(obj.v_x) == sgn(test_x(self) - test_x(obj))) or self.allow_pull:
                self.pusher = obj
                self.v_x = self.pusher.v_x
            if (sgn(obj.v_y) == sgn(test_y(self) - test_y(obj))) or self.allow_pull:
                self.pusher = obj
                self.v_y = self.pusher.v_y
    def set_position(self, x, y):
        dx, dy = x - self.x, y - self.y
        self.log("Moving %s, %s" % (x,y))
        Entity.set_position(self, x, y)
        self.border.set_position(self.border.x + dx, self.border.y + dy)

    def on_collision_end(self, obj):
        if obj == self.pusher:
            self.pusher = None
            self.v_x = 0
            self.v_y = 0

    def on_created(self):
        self.parent.add(self.border)


