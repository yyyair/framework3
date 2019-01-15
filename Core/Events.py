__author__ = 'User'

'''
We divided events into 2 types::
1. Global events, can be invoked and listened to by any component. For example, keyboard events
2. Local events, invoked by a component directly to another. For example, collision
'''

class Event:
    def __init__(self):
        self.name = "event_name"
        self.handlers = []
        self.verifier = lambda c, n: True

    def invoke(self, event_data):
        for handler in self.handlers:
            if self.verifier(handler.owner, self.name):
                handler.method(event_data)

class EventHandler:
    def __init__(self, method):
        self.method = method
        self.owner = None

class EventManager:
    def __init__(self, game):
        self.events = {}
        self.game = game

        self.debug = True
    def log(self, x):
        if self.debug:
            print("events: " + str(x))

    def invoke(self, event_name, event_data):
        if event_name in self.events:
            self.log("Invoking %s" % event_name)
            self.events[event_name].invoke(event_data)
        else:
            self.log("Tried invoking %s, no such event" % event_name)

    def add(self, event):
        if event.name not in self.events:
            self.events[event.name] = event
        else:
            # Combine methods of two events with identical names
            self.events[event.name].methods = self.events[event.name].methods + event.methods

    # Adds an event handler to an event
    def listen(self, event_name, event_handler, owner=None):
        handler = event_handler
        # Make sure handler is actually a handler, useful mostly for shortcuts
        if not isinstance(event_handler, EventHandler):
            handler = EventHandler(event_handler)
            handler.owner = owner
        # Add event handler
        if event_name not in self.events:
            self.log("No event %s. Creating one!" % event_name)
            e = Event()
            e.name = event_name
            e.verifier = self.game.can_listen
            self.add(e)
        self.events[event_name].handlers.append(handler)



