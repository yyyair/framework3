__author__ = 'User'
'''
Used to link json-text to python class pointers.
'''

import Graphics.GUI as DefaultGUI
from Addons.Player import Player
GUI_dict = {
    "label": DefaultGUI.Label,
    "textbox": DefaultGUI.Textbox,
    "button": DefaultGUI.Button
}

Gameplay_dict = {}

Addon_dict = {
    "player": Player
}

def get_class(class_name):
    dicts = [GUI_dict, Gameplay_dict, Addon_dict]
    for _dict in dicts:
        if class_name in _dict:
            return _dict[class_name]