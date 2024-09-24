import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .ScreenHelpers.PlayWordleRows import PlayWordleRows
from .Screen import Screen


#TODO add keyboard.
    #Should auto pop up, but can add highlighting to show which letters are unavailable or should be used.
class PlayWordleScreen(Screen):
    def __init__(self, wordleRows: PlayWordleRows):
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.title = None
        self.submitButton = None
        self.rows = wordleRows

    def CreateScreen(self):
        self.title = toga.Label("Guess the word!", style=Pack(padding=(2,5), font_size=16, text_align='center')) #TODO: center and format text
        self.submitButton = toga.Button("Submit", on_press=self.SubmitWordHandler, style=Pack(padding=5, font_size=12, width=100))
        
        self.innerBox.add(self.title)
        self.rows.AddToBox(self.innerBox)
        self.innerBox.add(self.submitButton)
    
        self.outerBox.add(self.innerBox)

    def SubmitWordHandler(self, widget) -> None:
        self.rows.SetNewCurRow()

    def UpdateScreen(self):
        return self.outerBox
    
    def ShowError(self, errorBox: toga.Box):
        self.innerBox.add(errorBox)
        #TODO: set some timer or some way to remove the error box
        #Also need to reset it on updateScreen. 
            #Is there some way I can implement it once for all the screens?
                #Doesn't really make sense though. They could theoretically ahve dif logic for  showing and removing errors
                #Just need to know they can show an error

    def CreateErrorBox(self, errorMsg: str):

        return self.outerBox


