__author__ = 'User'

from Core.Game import Game
from Graphics.Scene import Scene
from Graphics.Actor import Actor
from Graphics.Sprite import default_animated_sprite
from Graphics.GUI import *

from Addons.Player import Player
from Mechanics.CollisionActor import Wall
class MyGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.default_height *= 2
        self.default_width *= 2


    def load(self):
        self.loader.load_image("default", "Images/default.png")
        self.loader.load_image("wall", "Images/wall.png")

    def init(self):
        Game.init(self)

        # Create test scene
        s = Scene(game)
        s.name = "main_scene"
        # Setup GUI
        gui = GUIManager(game)
        s.setup_gui(gui)

        test_gui = RichTextbox(game)
        gui.add(test_gui)

        test_button = Button(game)
        test_button.set_position(0, 512)
        test_button.resize(96, 32)
        test_button.func = self.start_game
        gui.add(test_button)


        # Player object
        player = Actor(game)
        player.x, player.y = 256, 256
        player.sprite = default_animated_sprite()
        player.sprite.material = self.loader.get_image("default")
        s.add(player)

        # Player movement
        player.debug = False
        amount = 0.0005
        self.events.listen("key_down_w", lambda e: player.move_acceleration(0, -amount), player)
        self.events.listen("key_up_w", lambda e: player.move_acceleration(0, amount), player)

        self.events.listen("key_down_s", lambda e: player.move_acceleration(0, amount), player)
        self.events.listen("key_up_s", lambda e: player.move_acceleration(0, -amount), player)

        self.events.listen("key_down_d", lambda e: player.move_acceleration(amount, 0), player)
        self.events.listen("key_up_d", lambda e: player.move_acceleration(-amount, 0), player)

        self.events.listen("key_down_a", lambda e: player.move_acceleration(-amount, 0), player)
        self.events.listen("key_up_a", lambda e: player.move_acceleration(amount, 0), player)

        self.events.listen("mouse_click_1", lambda e: self.log("Clicked %s" % e))

        # Add scene to game
        self.add_scene(s)
        self.set_scene("main_scene")

    def start_game(self):

        # Create game scene
        world = Scene(game)
        world.name = "world"
        self.add_scene(world)

        # Create player
        player = Player(self)
        player.x, player.y = 256, 256
        world.add(player)

        # Add temporary wall
        wall = Wall(self)
        world.add(wall)

        self.set_scene("world")



    def update(self):
        Game.update(self)

    def draw(self):
        Game.draw(self)

    # Returns true if a component can listen to an event. Used to lock components when they are inactive.
    # TODO: Rework events so there are per-scene events and global events.
    def can_listen(self, component, event_name="any"):
        if component is not None:
            scene = self.get_scene()
            gui = scene.gui
            col = scene.collision

            # Check if component is not in scene
            if component.parent not in [scene, gui, col]:
                return False

            # Check if locked on UI element
            elif Property.GUI not in component.properties and gui.active_component is not None:
                return False
        return True

game = MyGame()
game.start()