__author__ = 'User'

import pygame

class Sprite:
    def __init__(self):
        # The pygame image object
        self.material = None

        # Sprite (not texture)
        self.width = 32
        self.height = 32

        # Texture dimensions
        self.material_width = 32
        self.material_height = 32

        # How to crop spritesheet
        self.crop = (0, 0, 32, 32)

        self.debug = False

    def get_surface(self, dt):
        surface = pygame.Surface((self.material_width, self.material_height), pygame.SRCALPHA)
        surface.blit(self.material, (0,0), area=self.crop)
        surface = pygame.transform.scale(surface, (self.width, self.height))
        return surface

    def log(self, x):
        if self.debug:
            print(x)

class AnimatedSprite(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        # A dictionary whose values are crops for spritesheet
        self.frames = {}
        self.frame_order = []
        self.current_frame = None

        self.autoplay = False
        self.time_since_last = 0
        self.current_frame_index = 0

    def get_surface(self, dt=1):
        # Check if need to move to next frame
        if self.autoplay and len(self.frame_order) > 0:
            # Check if mismatch between current frame and frame index
            if self.frame_order[self.current_frame_index] != self.current_frame:
                self.log("Mismatch")
                if self.current_frame in self.frame_order:
                    self.current_frame_index = self.frame_order.index(self.current_frame)
                else:
                    self.current_frame = self.frame_order[0]

            # Check if we should switch frame
            if self.time_since_last >= self.frames[self.current_frame]["time"]:
                self.log("Switching, tsl=%s, current=%s" % (self.time_since_last, self.frames[self.current_frame]["time"]))
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frame_order)
                self.current_frame = self.frame_order[self.current_frame_index]
                self.time_since_last = 0
            else:
                self.log("adding %s" % dt)
                self.time_since_last += dt

        # Crop according to animation
        if self.current_frame in self.frames:
            crop = self.frames[self.current_frame]["crop"]
        else:
            crop = self.crop
        surface = pygame.Surface((self.material_width, self.material_height), pygame.SRCALPHA)
        surface.blit(self.material, (0,0), area=crop)
        surface = pygame.transform.scale(surface, (self.width, self.height))
        return surface

    def set_frame(self, name):
        if name not in self.frames:
            print("Can't go to frame %s: No such frame" % name)
        elif name in self.frame_order:
            self.current_frame = name
            self.current_frame_index = self.frame_order.index(name)
        else:
            self.current_frame = name

    def get_frame(self, frame_name):
        if frame_name in self.frames:
            return self.frames[frame_name]

    def add_frame(self, name, crop, time):
        if name not in self.frames:
            self.frames[name] = {"crop":crop, "time": time}

    def remove_frame(self, name):
        # Removes from dict
        if name in self.frames:
            del self.frames[name]
        # Remove from list
        if name in self.frame_order:
            self.frame_order.remove(name)
        # Update current frame
        if len(self.frame_order):
            self.current_frame = self.frame_order[0]
        else:
            self.current_frame = None

# Returns a sprite with the default image. Should only be used for testing
def default_sprite():
    s = Sprite()
    img = pygame.image.load("Images/default.png")
    s.material = img
    return s

def default_animated_sprite():
    s = AnimatedSprite()
    img = pygame.image.load("Images/default.png")
    s.material = img
    s.frames = {"up":{"crop":(0,0,32,32), "time":5000}, "down":{"crop":(32,0,32,32), "time":5000}}
    s.frame_order = ["up", "down"]
    s.frame = "up"
    s.autoplay = True
    return s

def sprite_factory(material, animated):
    if animated:
        return default_animated_sprite()
    sprite = Sprite()
    sprite.material = material
    return sprite
