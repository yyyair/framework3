__author__ = 'User'
# TODO: Can try to cache location

'''
Caches a surface that is generated by a method
params:
    surface factory - A parameter-less method that returns a surface
'''
class CachedSurface:
    def __init__(self, generator):
        self.generate = generator
        # Can be used to implement "memory" for cached surface
        self.max_history = 1

        self.surface = None

    # Returns a copy of the surface
    def surface(self):
        if self.surface is not None:
            return self.surface
        else:
            print("Tried getting ungenerated cached surface. Generating")
            self.surface = self.generate()
            return self.surface

    def refresh(self):
        self.surface = self.generate()

