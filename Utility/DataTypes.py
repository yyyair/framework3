__author__ = 'User'

'''
Collection of budget enums
'''

# Component properties
class Property:
    # Core properties
    GUI = 1
    COLLISION = 2
    ACTOR = 3
    THINKER = 4
    COLLISION_WALL = 5

    # Gameplay properties
    CAN_BE_PICKED = 100
    HAS_INVENTORY = CAN_PICK = 101
    HAS_INTERACTION  = CAN_BE_INTERACTED = 110
    CAN_INTERACT = 111
    UNIT = 120
    PLAYER = 121
    SHOP = 122
    PROJECTILE = 123

# Item IDs
class Item:
    APPLE = 1

class Direction:
    UP = TOP = 1
    DOWN = BOT = BOTTOM = 2
    LEFT = 3
    RIGHT = 4

class PositionType:
    # Absolute position (ignores everything)
    ABSOLUTE = 1
    # Position relative to parent
    RELATIVE = 2
    # Position is expressed as ratio
    PROPORTIONAL = 3
    # Position is expressed as ratio of parent object
    RELATIVE_PROPORTIONAL = 4


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
        return "Unnamed%s" % str(property)

def direction_str(dir):
    if dir == Direction.UP:
        return "up"
    elif dir == Direction.DOWN:
        return "down"
    elif dir == Direction.LEFT:
        return "left"
    elif dir == Direction.RIGHT:
        return "right"