__author__ = 'User'

from Core.Component import GameComponent, ComponentManager
from Mechanics.Collision import CollisionManager, CollisionBody
from Utility.DataTypes import Property
from Graphics.Camera import Camera
'''
Component that can appear in a scene
'''
class SceneComponent(GameComponent):
    def __init__(self, game):
        GameComponent.__init__(self, game)
        self.name = "base_scene_component"

        # Position
        self.x = 0
        self.y = 0

        # Velocity
        self.v_x = 0
        self.v_y = 0

        # Acceleration
        self.a_x = 0
        self.a_y = 0

        # Axis lock
        self.lock_x = False
        self.lock_y = False

        # The room of the component. None = global
        self.room = None

    # Sets the position of the component.
    # Also triggers component_moved event.
    # Use for discrete motion
    def set_position(self, x, y):
        #self.log("Moving %s from %s, %s  to %s, %s" % (self.name, self.x, self.y, x, y))

        if not self.lock_x:
            self.x = x
        if not self.lock_y:
            self.y = y


    def move_position(self, dx, dy):
        self.set_position(self.x + dx, self.y + dy)

    # Use for linear motion
    # Change velocity
    def set_velocity(self, x, y):
        self.v_x = x
        self.v_y = y

    def move_velocity(self, dx, dy):
        self.set_velocity(self.v_x + dx, self.v_y + dy)

    # Parabolic motion

    def set_acceleration(self, x, y):
        self.a_x = x
        self.a_y = y

    # Change acceleration
    def move_acceleration(self, dx, dy):
        self.set_acceleration(self.a_x + dx, self.a_y + dy)

    def update(self):
        # Measure time since last update
        dt = self.game.clock.get_time()

        # Calculate change in x axis
        self.v_x += self.a_x * dt
        dx = self.v_x * dt

        # Calculate change in y axis
        self.v_y += self.a_y * dt
        dy = self.v_y * dt

        if dx != 0 or dy != 0:
            self.move_position(dx, dy)

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def on_created(self):
        pass

    def on_died(self):
        pass

    def kill(self):
        self.game.get_scene().remove(self.name)
        GameComponent.kill(self)

class SceneCollisionComponent(SceneComponent):
    def __init__(self, game):
        SceneComponent.__init__(self, game)
        self.collision_body = None

    def on_collision(self, body):
        self.log("I collided!")



class Scene(ComponentManager):
    def __init__(self, game):
        ComponentManager.__init__(self, game)
        self.name = "scene"

        self.gui = None
        self.collision = None
        self.camera = Camera(game)

    # Doesn't actually check that it's a GUIManager object
    def setup_gui(self, gui_manager):
        self.gui = gui_manager
        self.gui.parent = self

    def setup_collision(self, collision_manager):
        self.collision = collision_manager
        collision_manager.parent = self

    def setup_scene(self, gui, collision):
        self.setup_gui(gui)
        self.setup_collision(collision)

    def add(self, c):
        if ComponentManager.add(self, c):
            # Check if added component has the Collision property
            ''' Old check
            if "collision_box" in c.__dict__ is not None and isinstance(c.collision_body, CollisionBody):
                self.collision.add(c.collision_body)
            '''
            if Property.COLLISION in c.properties and self.collision is not None:
                self.collision.add(c)
            if Property.GUI in c.properties and self.gui is not None:
                self.gui.add(c)
            c.on_created()


    def draw(self):
        for c in self.components:
            c.draw()

        # Draw GUI last so its on top of anything else
        if self.gui is not None:
            self.gui.draw()

        # Draw collision objects
        if self.collision is not None:
            self.collision.draw()

    def update(self):
        for c in self.components:
            c.update()

        # Update GUI currently doesn't do anything
        if self.gui is not None:
            self.gui.update()

        # Update collision, tests for collisions
        if self.collision:
            self.collision.update()

        if self.camera.following is not None:
            following = self.camera.following
            x = following.x - self.game.screen.get_width()/2 + following.width/2
            y = following.y - self.game.screen.get_height()/2 + following.height/2
            self.camera.set_position(x, y)

