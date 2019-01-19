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
# TODO: Add local GUI events (value changed, hover, etc)
'''
class GUIManager(ComponentManager):
    def __init__(self, game):
        ComponentManager.__init__(self, game)
        self.name = "gui_manager"
        # The currently selected GUI element
        self.active_component = None
        # Can the user select new UI element
        self.locked = False

        self.game.events.listen("mouse_down_1", self.on_mouse_click)
        #self.game.events.listen("mouse_up_1", self.on_mouse_click)

    def on_mouse_click(self, e):
        if "pos" not in e:
            return
        if not self.locked and self.active_component is not None:
                self.active_component.active = False
                self.active_component.on_deactive()
                self.active_component = None
        mouse_point = Point(e["pos"][0], e["pos"][1])
        if self.locked and self.active_component is not None:
            if mouse_point in self.active_component.bounding_box:
                self.active_component.on_click()
            return
        # Create a temporary list of all clicked components, because clicking a component might remove another.
        to_trigger = []
        for c in self.components:
            if not c.hidden and mouse_point in c.bounding_box:
                to_trigger.append(c)
        for c in to_trigger:
            if not c.dead:
                c.on_click()
        if len(to_trigger) > 0:
            self.set_active(to_trigger[0])


    def set_active(self, component):
        if component is None:
            return
        if component not in self.components:
            self.log("Tried to make %s active, but no such component." %  component.name)
        else:
            if self.active_component is not None:
                self.active_component.on_decative()
                self.active_component.active = False
            self.active_component = component
            self.active_component.active = True
            self.active_component.on_active()
            self.log("%s is now active." % component.name)

    def set_inactive(self, component):
        if component is None:
            return
        if component not in self.components:
            self.log("Tried to make a component active, but no such component.")
        elif component != self.active_component:
            self.log("Tried to make a component inactive, but it is already inactive.")
        else:
            self.active_component.on_deactive()
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

        self.hidden = False

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
        if not self.hidden:
            return self.draw_on(self.game.screen)

    def set_position(self, x, y):
        self.bounding_box.x = x
        self.bounding_box.y = y
        Actor.set_position(self, x, y)

    # Local events
    def on_active(self):
        self.active = True

    def on_deactive(self):
        self.active = False

    def on_value_changed(self):
        pass

    def on_hover(self):
        pass

    def kill(self):
        if self.active:
            self.parent.set_inactive(self)
        Actor.kill(self)

    def draw_on(self, surface):
        box = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        box.fill((0 if self.active else 255,0,255))
        color = (0 if self.active else 255,0,255)
        box = rectangle_surface(self.height, self.width, color, border_width=3)
        surface.blit(box, (self.x, self.y))

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

    def draw_on(self, surface):
        surface.blit(self.create_surface(), (self.x, self.y))

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
        return self.value

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
        self.show_pointer = True
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
            self.show_pointer = False

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

    def draw_on(self, surface):
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

        surface.blit(dummy_surface, (self.x, self.y))

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
            #self.value += "\n"
            self.value = self.value[0:self.pointer] + "\n" + self.value[self.pointer:len(self.value)+1]
            self.pointer += 1
        elif key == "up_arrow":
            for i in range(self.pointer-1, -1, -1):
                if self.value[i] == "\n":
                    self.pointer = i
                    break
        elif key == "down_arrow":
            for i in range(self.pointer+1, len(self.value), 1):
                if self.value[i] == "\n":
                    self.pointer = i + 1
                    break
        else:
            Textbox.handle_input(self, e)

    def draw_on(self, surface):
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
            ptr_count -= len(raw_line) + 1
        surface.blit(background_surface, (self.x, self.y))


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

class ScrollBar(GUIActor):
    def __init__(self, game):
        GUIActor.__init__(self, game)

        self.current_index = 0
        self.max_index = 0

        self.max_y = self.y + self.height
        self.min_y = self.y

        self.max_y_offset = 0
        self.min_y_offset = 0

        self.min_height = 8

        self.scale_width = False

        self.debug = True
        self.captured = False
    def resize(self, w, h):
        GUIActor.resize(self, w, h)
        self.max_y = self.y + self.height + self.max_y_offset

    def set_position(self, x, y):
        GUIActor.set_position(self, x, y)
        self.max_y = self.y + self.height + self.max_y_offset
        self.min_y = self.y + self.min_y_offset

    def draw_on(self, surface):
        container = rectangle_surface(self.width, self.height, border_width=1, color=(189,195,199))
        scroller = rectangle_surface(self.width, max(self.min_height, self.height / (self.max_index+1)), border_width=1, color=(236,240,241))
        y = self.height * self.current_index/(self.max_index+1)
        container.blit(scroller, (0, y if ((self.y + self.height) - y) > self.min_height else self.y + self.height - self.min_height))
        surface.blit(container, (self.x, self.y))

    def update(self):
        GUIActor.update(self)
        if self.active and self.game.mouse.is_mouse_1_pressed():
            scroller_y = self.height * self.current_index/(self.max_index+1) + self.min_y
            scroller_height = self.height / (self.max_index+1)
            scroller = Rectangle(self.x, scroller_y, self.width, max(self.min_height, scroller_height))
            mouse = Point(self.game.mouse.get_x(), self.game.mouse.get_y())
            self.log(scroller, mouse)
            if self.captured:

                y = mouse.y
                if y < self.min_y:
                    self.current_index = 0
                elif y > self.max_y:
                    self.current_index = self.max_index
                else:
                    y -= self.y
                    self.current_index = int(y / scroller_height)
            if mouse in scroller:
                self.captured = True
        elif not self.game.mouse.is_mouse_1_pressed():
            self.captured = False

class GUIBundle(GUIActor):
    def __init__(self, game):
        GUIActor.__init__(self, game)
        self.components = []
        self.active_component = None
        self.name = "gui_bundle"
        self.debug = True

    def draw_on(self, surface):
        container = rectangle_surface(self.width, self.height, border_width=1)
        for component in self.components:
            component_surface = rectangle_surface(component.width, component.height, border_width=2, color=(255,0,0))
            #container.blit(component_surface, (component.x - self.x, component.y - self.y))
            component.set_position(component.x - self.x, component.y - self.y)
            component.draw_on(container)
            component.set_position(component.x + self.x, component.y + self.y)
        surface.blit(container, (self.x, self.y))

    def on_click(self):
        x, y = self.game.mouse.position()
        self.log(x, y)
        for component in self.components:
            component_rect = Rectangle(component.x, component.y, component.width, component.height)
            mouse_point = Point(x, y)
            if mouse_point in component_rect:
                self.log("Setting ", component, "as active")
                component.active = True
                self.active_component = component
                component.on_active()
                component.on_click()
                break


    def on_deactive(self):
        self.log("Deactivating", self.active)
        if self.active_component is not None:
            self.active_component.active = False
            self.active_component.on_deactive()
            self.active_component = None
    def update(self):
        for component in self.components:
            component.update()

    def resize(self, w, h):
        old_w, old_h = self.width, self.height
        GUIActor.resize(self, w, h)
        self.log("I am", self.width, self.height)
        w_ratio = float(self.width) / old_w
        h_ratio = float(self.height) / old_h
        self.log(w_ratio, old_w, self.width)
        for component in self.components:
            #component.resize(component.width * w_ratio, component.height * h_ratio)
            component.scale(w_ratio, h_ratio)
            component.set_position((component.x - self.x) * w_ratio + self.x, (component.y - self.y) * h_ratio + self.y)
            self.log(component.x, component.y, component.width, component.height)

    def set_position(self, x, y):
        dx, dy = x - self.x, y - self.y
        GUIActor.set_position(self, x, y)
        for component in self.components:
            component.set_position(component.x+dx, component.y+dy)
            self.log(component.x, component.y)


class TestCanvas(GUIBundle):
    def __init__(self, game):
        GUIBundle.__init__(self, game)
        self.resize(256, 256)
        scroller = ScrollBar(self.game)
        scroller.resize(16, 96)
        scroller.set_position(96, 0)
        scroller.max_index = 5000
        scroller.min_y_offset = scroller.max_y_offset = 0

        textbox = RichTextbox(self. game)
        textbox.resize(96, 96)

        self.components.append(scroller)
        self.components.append(textbox)

class ScrollableTextbox(GUIBundle):
    def __init__(self, game):
        GUIBundle.__init__(self, game)

class MessageBox(GUIBundle):
    def __init__(self, game):
        GUIBundle.__init__(self, game)
        self.resize(240, 120)
        self.title = "MessageBox"

        close_btn = Button(self.game)
        close_btn.resize(60, 20)
        close_btn.set_position(90, 90)
        close_btn.value = "Close"
        close_btn.func = self.close
        self.components.append(close_btn)

    def draw_on(self, surface):
        container = rectangle_surface(self.width, self.height, border_width=0, color=(255,0,0))

        old_x, old_y = self.x, self.y
        self.set_position(0, 0)
        GUIBundle.draw_on(self, container)
        self.set_position(old_x, old_y)
        s_width, s_height = surface.get_size()
        x, y = s_width/2 - self.width/2, s_height/2 - self.height/2
        surface.blit(container, (self.x, self.y))

    def close(self):
        print("abcd")
        self.kill()

    def on_created(self):
        self.parent.set_active(self)
        self.parent.locked = True

    def on_deactive(self):
        self.parent.locked = False
