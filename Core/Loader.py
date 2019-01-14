__author__ = 'User'

import pygame

class Loader:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, name, path):
        img = pygame.image.load(path)
        self.images[name] = img

    def load_sound(self, name):
        pass

    def load_font(self, name):
        pass

    def get_image(self, name):
        if name not in self.images:
            return None
        else:
            return self.images[name]