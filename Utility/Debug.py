__author__ = 'User'

class LogObject:
    def __init__(self):
        self.debug = False

    def debug(self, *msg):
        if self.debug:
            print(msg)
