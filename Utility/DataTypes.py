__author__ = 'User'

class Property:
    GUI = 1
    COLLISION = 2
    ACTOR = 3
    THINKER = 4
    COLLISION_WALL = 5
    CAN_BE_PICKED = 6
    HAS_INVENTORY = 7
    HAS_INTERACTION  = 8
    CAN_INTERACT = 9

class Direction:
    UP = TOP = 1
    DOWN = BOT = BOTTOM = 2
    LEFT = 3
    RIGHT = 4


def property_str(property):
    if property == Property.GUI:
        return "gui"
    elif property == Property.COLLISION:
        return "collision"
    elif property == Property.ACTOR:
        return "actor"
    elif property == Property.THINKER:
        return "thinker"
    else:
        return "unknown"

def direction_str(dir):
    if dir == Direction.UP:
        return "up"
    elif dir == Direction.DOWN:
        return "down"
    elif dir == Direction.LEFT:
        return "left"
    elif dir == Direction.RIGHT:
        return "right"