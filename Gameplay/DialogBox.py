__author__ = 'User'

from Graphics.GUI import GUIBundle

'''
Implements dialog between NPC and the player.
'''

class DialogType:
    TREE = 1
    DEFAULT = 2
    CHOICE = 3
    INPUT = 4

'''
A tree structure of DialogBox objects.
'''
class DialogTree:
    def __init__(self):
        self.name = "dialog_tree"
        self.start = None
        self.current = None
        self.on_finish = None

'''
Simple rectangle with text in it.
'''
class DialogBox:
    def __init__(self):
        self.type = DialogType.DEFAULT
        self.name = "dialog_box"
        self.next = None


'''
DialogBox with buttons (choices).
'''
class ButtonDialogBox(DialogBox):
    def __init__(self):
        DialogBox.__init__(self)
        self.type = DialogType.DEFAULT
        self.name = "dialog_box"
        self.next = None

'''
DialogBox with textbox in it.
'''
class TextboxDialogBox(DialogBox):
     def __init__(self):
        DialogBox.__init__(self)
        self.type = DialogType.DEFAULT
        self.name = "dialog_box"
        self.next = None

'''
The actual container of the dialog.
'''
class DialogBoxContainer(GUIBundle):
    def __init__(self, game):
        GUIBundle.__init__(self, game)
        # The controlled tree
        self.tree = None

    def reset(self):
        pass

    def show(self):
        pass


'''
Creates a DialogTree object from a file.
Dialog files are in .json format.
A dialog file contains two fields: tree, and nodes.
tree: string, name of the first node
nodes: list, list of nodes

Each node has the following fields:
type: string, node type (default, button, textbox)
next: string, name of next node
text: string, text of DialogBox
data: object, additional data (mainly for design purposes)
'''
def ImportDialog():
    pass

