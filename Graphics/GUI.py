__author__ = 'User'

from Core.Component import ComponentManager
from Core.Input import pykey_to_key
from Graphics.Actor import Actor
from Utility.Geometry import Rectangle, Point
from Utility.DataTypes import Property
from Graphics.Utility import rectangle_surface
import pygame
'''
# TODO: Improve mouse_down and mouse_up events
'''
class GUIManager(ComponentManager):
    def __init__(self, game):
        ComponentManager.__init__(self, game)
        self.name = "gui_manager"
        # The currently selected GUI element
        self.active_component = None

        self.game.events.listen("mouse_down_1", self.on_mouse_click)

    def on_mouse_click(self, e):
        if "pos" not in e:
            return
        if self.active_component is not None:
                self.active_component.active = False
                self.active_component = None
        mouse_point = Point(e["pos"][0], e["pos"][1])
        # Create a temporary list of all clicked components, because clicking a component might remove another.
        to_trigger = []
        for c in self.components:
            if mouse_point in c.bounding_box:
                to_trigger.append(c)
        for c in to_trigger:
            # Trigger local event
            if self.active_component is not None:
                self.active_component.active = False
            self.active_component = c
            self.active_component.active = True
            self.log("%s is now active." % c.name)
            c.on_click()

    def set_active(self, component):
        if component is None:
            return
        if component not in self.components:
            self.log("Tried to make %s active, but no such component." %  component.name)
        else:
            self.active_component.on_decative()
            self.active_component.active = False
            self.active_component = component
            self.active_component.active = True
            self.active_component.on_active()

    def set_inactive(self, component):
        if component is None:
            return
        if component not in self.components:
            self.log("Tried to make a component active, but no such component.")
        elif component != self.active_component:
            self.log("Tried to make a component inactive, but it is already inactive.")
        else:
            self.active_component.on_decative()
            self.active_component.active = False
            self.active_component = None


class GUIActor(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)
        self.name = "gui_actor"

        # Gives the GUI property to the component. Checking is probably redundant
        if Property.GUI not in self.properties:
            self.properties.append(Property.GUI)

        # Box representing the clickable area. Coordinates are relative.
        self.bounding_box = Rectangle(0, 0, self.height, self.width)

        self.active = False
        self.value = "value"

    def resize(self, w, h):
        if w > 0 and h > 0:
            self.width = w
            self.height = h
            self.bounding_box.width = w
            self.bounding_box.height = h

    def on_click(self):
        # Invoke global click event
        self.game.events.invoke(self.name+"_click", None)
        print("yes")

    def get_value(self):
        return self.value

    def set_value(self, val):
        self.value = val

    def draw(self):
        box = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        box.fill((0 if self.active else 255,0,255))
        color = (0 if self.active else 255,0,255)
        box = rectangle_surface(self.height, self.width, color, border_width=3)
        self.game.screen.blit(box, (self.x, self.y))

    def set_position(self, x, y):
        self.bounding_box.x = x
        self.bounding_box.y = y
        Actor.set_position(self, x, y)

    # Local events
    def on_active(self):
        self.active = True

    def on_decative(self):
        self.active = False

class Label(GUIActor):

    # Text direction
    CENTER = 0
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    def __init__(self, game):
        GUIActor.__init__(self, game)
        self.name = "gui_label"
        self.resize(256, 48)

        self.font_size = 16
        self.font = pygame.font.SysFont("calibri", self.font_size)
        self.color = (0, 0, 0)

        # horizontal = x, vertical = y
        self.horizontal_mode = self.LEFT
        self.vertical_mode = self.CENTER

        self.show_frame = False

        self.padding = {"vertical":0, "horizontal":16}

    def draw(self):
        self.game.screen.blit(self.create_surface(), (self.x, self.y))

    def create_surface(self):
        #text = self.game.resources.load_font("default")
        font = self.font
        dummy_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        text = font.render(self.get_value(), 1, self.color)

        # Vertical alignement (y)
        y = self.get_y_offset(text)

        # Horizontal alignment (x)
        x = self.get_x_offset(text)

        if self.show_frame:
            dummy_surface.blit(rectangle_surface(self.width, self.height, border_width=2), (0,0))
        dummy_surface.blit(text, (x,y))
        return dummy_surface

    # Returns x offset of text
    def get_x_offset(self, text):
        x = 0
        if self.horizontal_mode == Label.CENTER:
            x =  self.width / 2 - text.get_width()/2
        elif self.horizontal_mode == Label.LEFT:
            x = 0
        else:
            x = self.width - text.get_width()
        return x +  self.padding["horizontal"]


    # Returns y offset of text
    def get_y_offset(self, text):
        y = 0
        if self.vertical_mode == Label.CENTER:
            y =  self.height / 2 - text.get_height()/2
        elif self.vertical_mode == Label.TOP:
            y = 0
        else:
            y = self.height - text.get_height()
        return y + self.padding["vertical"]

    def get_value(self):
        return self.name

# A textbox is a label that can be dynamically modified by the user.
class Textbox(Label):
    def __init__(self, game):
        Label.__init__(self, game)
        self.show_frame = True

        self.game.events.listen("key_down", self.start_get_input)
        self.game.events.listen("key_up", self.stop_get_input)

        # Allows to hold a key for prolonged input
        self.getting_input = False
        self.current_key = None
        self.last_handle_time = 0
        self.handle_delay_initial = 500
        self.handle_delay = 50

        # Pointer so we know where the text goes
        self.pointer = len(self.value)
        self.pointer_interval = 1000
        self.pointer_time_count = 0
        self.show_pointer = False

        # Text input direction left to right (True for any normal language, False for Hebrew/Arabic)
        self.ltr = True

        self.writeable = "0123456789abcdefghijklmnopqrstuvwxyz?.,"

    # Handles a single user input
    def handle_input(self, e):
        key = pykey_to_key(e)
        if key == "backspace" :
            if self.value!="" and self.pointer > 0:
                # Pointer is in the end
                if self.pointer == len(self.value):
                    self.value = self.value[0:-1]
                else:
                    self.value = self.value[0:self.pointer-1] + self.value[self.pointer:len(self.value)+1]
                self.pointer -= 1
        elif key == "space":
            self.value += " "
            self.pointer += 1
        elif key == "right_arrow":
            if len(self.value):
                self.pointer = (self.pointer + 1) if self.pointer < len(self.value) else self.pointer
        elif key == "left_arrow":
            if len(self.value):
                self.pointer = (self.pointer - 1) if self.pointer > 0 else 0
        elif key in self.writeable:
            self.value = self.value[0:self.pointer] + e["unicode"] + self.value[self.pointer:len(self.value)+1]
            self.pointer += 1

    # Gets input from the user until a key up event.
    def start_get_input(self, e):
        if not self.active:
            return False
        self.getting_input = True
        self.current_key = e
        self.handle_input(e)
        # We set the last handle time to the "future" to make the second handle delayed.
        self.last_handle_time = self.game.time + self.handle_delay_initial


    # Stop getting user input.
    def stop_get_input(self, e):
        if not self.active or not self.getting_input:
            return
        key = pykey_to_key(e)
        current_key = pykey_to_key(self.current_key)
        if key == current_key:
            self.getting_input = False
            self.current_key = None

    # Returns the effective value
    def get_value(self):
        # Draw pointer
        value = self.value

        '''
        # Old method of generating a pointer
        if self.active:
            ptr = "" if self.show_pointer else ""
            value = self.value[0:self.pointer] + ptr + self.value[self.pointer:len(self.value)+1]
        if not self.ltr:
            value = value[-1::-1]
        '''
        return value

    # Sets (actual) value
    def set_value(self, val):
        self.value = val
        self.pointer = len(val)

    def draw(self):
        dummy_surface = self.create_surface()

        # Draw pointer
        if self.active and self.show_pointer:

            before_ptr = self.value[0:self.pointer]

            before_render = self.font.render(before_ptr, 1, (0,0,0))
            all_render = self.font.render(self.value, 1, (0,0,0))

            ptr_surface = pygame.Surface((1, before_render.get_height()), pygame.SRCALPHA)
            ptr_surface.fill((0,0,0))

            x = self.get_x_offset(all_render)
            y = self.get_y_offset(all_render)

            ptr_x = x + before_render.get_width()
            ptr_y = y

            dummy_surface.blit(ptr_surface, (ptr_x, ptr_y))

        self.game.screen.blit(dummy_surface, (self.x, self.y))

    def update(self):
        if not self.active:
            return
        self.pointer_time_count += self.game.clock.get_time()
        if self.pointer_time_count > self.pointer_interval:
            self.show_pointer = not self.show_pointer
            self.pointer_time_count = 0

        # Check if we are still getting input
        if self.getting_input and self.current_key is not None:
            now = self.game.time
            if now - self.last_handle_time > self.handle_delay:
                self.handle_input(self.current_key)
                self.last_handle_time = now

'''
Rich text box. Should have the following features:
1. Colored text
2. Italic, bold, underscore
3. Images (Emojis)
Instead of a string, value is a tree-like datastructure.
'''

class Node:
    BLANK = 1
    TEXT = 2
    IMAGE = 3
    def __init__(self):
        self.type = Node.BLANK
        self.value = ""

class TextNode:
    def __init__(self):
        self.type = Node.TEXT
        self.value = ""
        self.color = (0,0,0)

        self.bold = False
        self.italic = False
        self.underline = False

        self.size = 16

class ImageNode:
    pass

class TextTree:
    pass

class RichTextbox(Textbox):
    def __init__(self, game):
        Textbox.__init__(self, game)
        self.name = "rich_textbox"
        self.resize(256, 256)
        self.vertical_mode = Label.TOP
        self.padding["vertical"] = 16

    def handle_input(self, e):
        key = pykey_to_key(e)
        if key == "enter":
            self.value += "\n"
            self.pointer += 1
        else:
            Textbox.handle_input(self, e)

    def draw(self):
        lines = self.value.split("\n")
        render_lines = [self.font.render(line, 1, self.color) for line in lines]
        x = self.get_x_offset(render_lines[0])
        y = self.get_y_offset(render_lines[0])
        background_surface = rectangle_surface(self.width, self.height, border_width=3)
        line_space = 16
        # Determine when to draw pointer
        ptr_count = self.pointer
        for line_id in range(len(lines)):
            rendered_line = render_lines[line_id]
            raw_line = lines[line_id]

            background_surface.blit(rendered_line, (x, y))


            if self.active and self.show_pointer and len(raw_line) >= ptr_count >= 0:

                before_ptr = raw_line[0:ptr_count]

                before_render = self.font.render(before_ptr, 1, (0,0,0))

                ptr_surface = pygame.Surface((1, before_render.get_height()), pygame.SRCALPHA)
                ptr_surface.fill((0,0,0))

                ptr_x = x + before_render.get_width()
                ptr_y = y

                background_surface.blit(ptr_surface, (ptr_x, ptr_y))
            y += line_space
            ptr_count -= len(raw_line)
        self.game.screen.blit(background_surface, (self.x, self.y))


class Button(Label):
    def __init__(self, game):
        Label.__init__(self, game)
        self.show_frame = True
        self.name = "gui_button"
        self.func = None

    def on_click(self):
        print("cicked")
        if self.func is not None:
            self.func()


