__author__ = 'User'

from Core.Component import Component
from Core.Loader import Loader
from Core.Events import EventManager, Event
from Core.Input import Keyboard, Mouse

# Scene setups
from Graphics.Scene import Scene
from Mechanics.Collision import CollisionManager
from Graphics.GUI import GUIManager
from Gameplay.DialogBox import DialogBoxContainer
import pygame

MAX_FPS = 120

'''
Core game object.
Contains global draw, update, load, and initialization methods.
'''
class Game(Component):
    def __init__(self):
        Component.__init__(self)
        self.name = "game"

        # Default screen size
        self.default_width = 480
        self.default_height = 320

        # PyGame objects

        # The main window for the app
        self.screen = None
        # Game clock
        self.clock = None
        self.time = 0
        # Resource manager
        self.loader = None
        # Event manager
        self.events = None
        # Input handler
        self.keyboard = None
        self.mouse = None

        # Current game frame
        self.frame = 0

        # Controls the game loop
        self.running = True

        # Background surface
        self.background = None
        self.background_color = (255, 255, 255)
        self.default_font = None

        # Game window name
        self.win_name = "PyFrame3"

        # Scene stuff
        self.scenes = {}
        self.current_scene = None

        self.debug_time = ""

    # Initalize internal game stuff
    def start(self):
        self.log("Starting game!")
        pygame.init()

        # Initalize the screen. Pygame uses width, height
        self.screen = pygame.display.set_mode((self.default_width, self.default_height))


        # Initialize clock
        self.clock = pygame.time.Clock()

        # Initialize basic game features
        self.loader = Loader(self)
        self.events = EventManager(self)
        self.keyboard = Keyboard(self.events)
        self.mouse = Mouse(self.events)

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((250,250,250))
        self.default_font = pygame.font.SysFont("calibri", 14)

        self.load()
        self.init()
        self.game_loop()

    def game_loop(self):
        while self.running:
            self.frame += 1
            self.time += self.clock.get_time()

            # Run game logic
            self.update()
            update_time = self.clock.get_time()
            self.time += update_time

            # Draw scene
            self.draw()
            draw_time = self.clock.get_time()
            self.time += draw_time

            # Limits game FPS
            self.clock.tick(MAX_FPS)
            self.debug_time = "Update: %s, Draw: %s" % (update_time, draw_time)

    def init(self):
        # Set window name and icon
        self.events.listen("key_down", self.log)
        pygame.display.set_caption(self.win_name)

    def update(self):
        # Handle user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Keyboard events
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                event_name = "key_" + ("down" if event.type == pygame.KEYDOWN else "up")
                self.events.invoke(event_name, event.__dict__)
            # Mouse events, can be either click or move
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEMOTION:
                # Click event
                if "button" in event.__dict__:
                    # Trigger a local mouse event, which then triggers a global event.
                    # Can also trigger raw_mouse_click as a global event, but it didn't seem useful so I dropped it.
                    self.mouse.mouse_1_click(event.__dict__)
                # Move vent
                elif "buttons" in event.__dict__:
                    pass
        scene = self.get_scene()
        #self.log(self.clock.get_fps())
        if scene is not None:
            scene.update()

    def draw(self):
        # Background color
        self.screen.fill(self.background_color)
        # Draw background
        if self.background is not None:
            self.screen.blit(self.background, (0,0))
        scene = self.get_scene()
        if scene is not None:
            scene.draw()

        # print debug info
        self.default_font.set_bold(True)
        text = self.default_font.render("FPS: %s" %self.clock.get_fps(), 0, (255,255,0), (0,0,0))
        self.screen.blit(text, (0,0))
        text = self.default_font.render(self.debug_time, 0, (255,255,0), (0,0,0))
        self.screen.blit(text, (0,16))
        self.default_font.set_bold(False)

        # Finish drawing
        pygame.display.flip()

    # Manage scenes

    def add_scene(self, scene):
        if not isinstance(scene, Scene):
            self.log("Can't add scene, got bad object")
            return False
        elif scene.name in self.scenes:
            self.log("Cant add scene, scene already exists.")
            return False
        elif not isinstance(scene.name, str):
            self.log("Cant add scene, illegal scene name")

        # Add GUI manager if needed
        if scene.gui is None:
            gui_manager = GUIManager(self)
            gui_manager.name = "gui_manager_"+scene.name
            scene.setup_gui(gui_manager)

            # Add dialog support to scene
            dialog_container = DialogBoxContainer(self)
            scene.dialog_container = dialog_container
            gui_manager.add(dialog_container)


        # Add collision if needed
        if scene.collision is None:
            collision_manager = CollisionManager(self)
            collision_manager.name = "collision_manager_"+scene.name
            scene.setup_collision(collision_manager)

        self.scenes[scene.name] = scene

    def remove_scene(self, scene_name):
        if scene_name not in self.scenes:
            self.log("Tried to remove scene %s but there is no such scene." % scene_name)
            return
        del self.scenes[scene_name]

    def get_scene(self):
        if self.current_scene not in self.scenes:
            self.log("Tried to get scene %s, but no such scene." % self.current_scene)
            return None
        return self.scenes[self.current_scene]

    def set_scene(self, scene_name):
        if scene_name not in self.scenes:
            self.log("Tried to set %s scene but no such scene" % scene_name)
            return False
        self.current_scene = scene_name
        return True


    # Returns true if a given component can listen to an event
    def can_listen(self, component, event_name="any"):
        return True









