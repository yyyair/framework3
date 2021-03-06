__author__ = 'User'

import pygame

'''
Responsible for invoking key-specific events
'''


class Keyboard:
    def __init__(self, event_manager):
        self.events = event_manager

        # All pressed keys
        self.pressed = {}
        self.events.listen("key_down", self.on_key_down)
        self.events.listen("key_up", self.on_key_up)

    def on_key_down(self, e):
        key_code = e["key"]
        key = pykey_to_key(e)
        if key not in self.pressed:
            self.pressed[key] = e

        self.events.invoke("key_down_" + pykey_to_key(e), e)

    def on_key_up(self, e):
        key_code = e["key"]
        key = pykey_to_key(e)
        if key in self.pressed:
            del self.pressed[key]

        self.events.invoke("key_up_" + pykey_to_key(e), e)

# Converts pygame keycodes to string representation
def pykey_to_key(pykey_data):

        pykey = pykey_data["key"]
        keys = "abcdefghijklmnopqrstuvwxyz"
        numbers = "0123456789"
        if pykey_data["mod"] == 64:
            return "unknown"
        if 97 <= pykey <= 122:
            return keys[pykey - 97].lower()
        if 48 <= pykey <= 57:
            return numbers[pykey - 48].lower()
        elif pykey == pygame.K_UP:
            return "up_arrow"
        elif pykey == pygame.K_LEFT:
            return "left_arrow"
        elif pykey == pygame.K_RIGHT:
            return "right_arrow"
        elif pykey == pygame.K_DOWN:
            return "down_arrow"
        elif pykey == 44:
            return ","
        elif pykey == 47:
            return "?"
        elif pykey == 46:
            return "."
        elif pykey == 8:
            return "backspace"
        elif pykey == 9:
            return "tab "
        elif pykey == 301:
            return "caps_lock"
        elif pykey == 32:
            return "space"
        elif pykey == 13:
            return "enter"
        elif pykey == 282:
            return "f1"
        elif pykey == 283:
            return "f2"
        elif pykey == 284:
            return "f3"
        elif pykey == 285:
            return "f4"
        elif pykey == 286:
            return "f5"
        elif pykey == 287:
            return "f6"
        elif pykey == 288:
            return "f7"
        elif pykey == 289:
            return "f8"
        elif pykey == 290:
            return "f9"
        elif pykey == 291:
            return "f10"
        elif pykey == 292:
            return "f11"
        elif pykey == 293:
            return "f12"
        return "unknown_key"

'''
In pygame mouse events have 2 types: Mouse moved, mouse pressed.
When a button is pressed or released, it triggers the same event. This handler class tries to separate those.
'''
class Mouse:
    def __init__(self, events):
        self.events = events

        self.states = {
            "1": False,
            "2": False
        }

        # The line below listens to a global mouse event, currently it is disabled since it didn't seem useful.
        # self.events.listen("raw_mouse_click_1", self.mouse_1_click)

    # Handles mouse click events, either globally or locally.
    def mouse_1_click(self, e):
        if self.states["1"]:
            self.events.invoke("mouse_up_1", e)
        else:
            self.events.invoke("mouse_down_1", e)
        self.states["1"] = not self.states["1"]

    def is_mouse_1_pressed(self):
        return self.states["1"]

    def position(self):
        return pygame.mouse.get_pos()

    def get_x(self):
        return self.position()[0]

    def get_y(self):
        return self.position()[1]
