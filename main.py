__author__ = 'User'

from Core.Game import Game
from Graphics.Scene import Scene
from Graphics.Actor import Actor
from Graphics.Sprite import default_animated_sprite
from Graphics.GUI import *

from Addons.Player import Player
from Addons.World import World
from Addons.Item import ItemEntity
from Addons.Shop import Shop

from Mechanics.CollisionActor import Wall
class MyGame(Game):
    def __init__(self):
        Game.__init__(self)
        self.default_height = 840
        self.default_width = 1480


    def load(self):
        self.loader.load_image("default", "Images/default.png")
        self.loader.load_json_resources("Data/resources.json")
        x = self.loader.scene_from_file("Data/Scenes/main.json")
        self.add_scene(x)

    def init(self):
        Game.init(self)

        # Create test scene
        s = Scene(game)
        s.name = "main_scene"
        # Setup GUI
        gui = GUIManager(game)
        s.setup_gui(gui)

        test_button = Button(game)
        test_button.set_position(0, 512)
        test_button.resize(96, 32)
        test_button.func = lambda: self.start_game()
        s.add(test_button)

        # # Player object
        # player = Actor(game)
        # player.x, player.y = 256, 256
        # player.sprite = default_animated_sprite()
        # player.sprite.material = self.loader.get_image("default")
        # s.add(player)
        #
        # # Player movement
        # player.debug = False
        # amount = 0.0020
        # self.events.listen("key_down_w", lambda e: player.move_acceleration(0, -amount), player)
        # self.events.listen("key_up_w", lambda e: player.move_acceleration(0, amount), player)
        #
        # self.events.listen("key_down_s", lambda e: player.move_acceleration(0, amount), player)
        # self.events.listen("key_up_s", lambda e: player.move_acceleration(0, -amount), player)
        #
        # self.events.listen("key_down_d", lambda e: player.move_acceleration(amount, 0), player)
        # self.events.listen("key_up_d", lambda e: player.move_acceleration(-amount, 0), player)
        #
        # self.events.listen("key_down_a", lambda e: player.move_acceleration(-amount, 0), player)
        # self.events.listen("key_up_a", lambda e: player.move_acceleration(amount, 0), player)
        #
        # self.events.listen("key_up_space", lambda e: player.set_position(self.screen.get_height()/2,self.screen.get_width()/2))

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
        player.x, player.y = 512, 416
        world.camera.following = player
        world.add(player)

        # Add item
        item = ItemEntity(self)
        item.x, item.y = 512, 512
        world.add(item)

        # Add shop
        shop = Shop(self)
        shop.set_position(256, 512)
        world.add(shop)


        # Add temporary wall
        wall = Wall(self)
        #world.add(wall)

        # Setup world room
        world_room = World(self)
        world_room.setup_room(world, world_room.width * 3, world_room.height * 3)
        world.add(world_room)

        self.background_color = (0,0,0)
        self.background = None

        self.events.listen("key_up_f1", lambda e: self.toggle_debug(world.collision), None)

        self.set_scene("world")

    def toggle_debug(self, component):
        component.debug = not component.debug
        component.debug_draw = not component.debug_draw

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