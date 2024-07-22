#This will use s imilar section to the Solver screen. But not buttons. So don't actually create a reausable fragment type idea
#TODO:
#COMBINE WITH GETGUESSFROMUSER
    #We want to have a stacked list of words like in woordle itself.
    #bottom most one they can enter text in.
        #have it fixed with the 6 rows, just keep the last ones blank for now
    #After a guess the next row will become active, and the one above will get colours.

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .ScreenHelpers.PlayWordleRows import PlayWordleRows
from .Screen import Screen


#TODO add keyboard.
    #Should auto pop up, but can add highlighting to show which letters are unavailable or should be used.
class PlayWordleScreen(Screen):
    def __init__(self):
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.title = None
        self.rows = PlayWordleRows()

    def CreateScreen(self):
        self.title = toga.Label("Guess the word!", style=Pack(padding=(2,5), font_size=16, text_align='center')) #TODO: center and format text
        self.innerBox.add(self.title)

        self.rows.AddToBox(self.innerBox)
        self.innerBox.add(toga.Button("Submit", on_press=self.SubmitWordHandler, style=Pack(padding=5, font_size=12)))
        self.outerBox.add(self.innerBox)

    def SubmitWordHandler(self, widget) -> None:
        self.rows.SetNewCurRow()
    
        #TODO: create an event for managing this
            #Only if we need to call the new 'solver' class

    def UpdateScreen(self):
        return self.outerBox


