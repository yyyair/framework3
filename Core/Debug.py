__author__ = 'User'

class Debugger:
    ANY = 0
    ERROR = 1
    GENERIC = 2

def log(creator, msg, type=Debugger.GENERIC):
    debug_types = [Debugger.ANY]
    if type in debug_types or Debugger.ANY in debug_types:
        print("%s: %s" % (creator, msg))