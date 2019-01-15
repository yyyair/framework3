__author__ = 'User'

'''
Components are in-game objects.
Name should be a unique, lower case string with _ as word delimiters
'''
class Component:
    def __init__(self):
        # The parent component
        self.parent = None

        # Name of component, should be unique
        self.name = "base_component"

        # Priority is used to prioritize component computation
        self.priority = 0

        # Used to prevent logging
        self.debug = True

        # Probably bad programming habit
        self.properties = []

        self.dead = False

    # Called every game tick
    def update(self):
        pass

    # Called every game tick after update
    def draw(self):
        pass

    # Called once before the frist game tick
    def load(self):
        pass

    # Called once upon creation
    def init(self):
        pass

    # Removes the component from game
    def kill(self):
        self.dead = True
        if isinstance(self.parent, ComponentManager):
            self.parent.remove(self.name)
        self.name = "dead"
        self.parent = None

    def log(self, *msg, ignore_debug=False):
        if ignore_debug or self.debug:
            print(("%s: " % self.name) + " ".join([str(s) for s in msg]))

    def has_property(self, prop):
        return prop in self.properties

    def add_property(self, prop):
        if prop not in self.properties:
            self.properties.append(prop)

'''
Game components are components that can access the game object and interact with other game objects.
'''
class GameComponent(Component):
    def __init__(self, game):
        Component.__init__(self)
        self.parent = game
        self.game = game

'''
Handles a collection of components.
'''
class ComponentManager(GameComponent):
    def __init__(self, game):
        GameComponent.__init__(self, game)
        self.components = []
        self.components_names = []
        self.ignore_priority = False

    def add(self, c):
        # Prevent duplicate names
        i=1
        base_name = c.name
        while c.name in self.components_names:
            c.name = base_name + str(i)
            i += 1
        self.log("Renamed %s to %s" % (base_name, base_name+str(i)))

        # Add the component
        self.log("Adding %s" % c.name)
        self.components_names.append(c.name)
        c.parent = self
        if self.ignore_priority:
            self.components.append(c)
            return True

        # Make sure we keep them sorted by priority
        for i in range(len(self.components)):
            if self.components[i].priority <= c.priority:
                self.components.insert(i, c)
                break

        # If its empty just insert
        if len(self.components) == 0:
            self.components.append(c)

        return True

    # Removes a component by name
    def remove(self, c_name):
        to_remove = []
        # Find all relevant components
        for c in self.components:
            if c.name == c_name:
                to_remove.append(c)

        # Remove them
        for c in to_remove:
            self.components.remove(c)
        self.components_names.remove(c_name)

    # Removes a component by pointer
    def remove_absolute(self, c):
        self.remove(c.name)

    def get_component(self, name):
        if name not in self.components_names:
            return None
        for c in self.components:
            if c.name == name:
                return c

    def update(self):
        for c in self.components:
            if not c.dead:
                c.update()

    def draw(self):
        for c in self.components:
            #self.log("Drawing %s" % c.name)
            if not c.dead:
                c.draw()