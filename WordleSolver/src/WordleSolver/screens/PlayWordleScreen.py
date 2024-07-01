#This will use s imilar section to the Solver screen. But not buttons. So don't actually create a reausable fragment type idea
#TODO:
#COMBINE WITH GETGUESSFROMUSER
    #We want to have a stacked list of words like in woordle itself.
    #bottom most one they can enter text in.
        #have it fixed with the 6 rows, just keep the last ones blank for now
    #After a guess the next row will become active, and the one above will get colours.

from .Screen import Screen

class PlayWordleScreen(Screen):
    def __init__(self):
        self.rows = None
        self.curRow = None

    def CreateScreen(self):
        pass
    
    def UpdateScreen(self):
        pass