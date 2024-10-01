import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from threading import Thread
from time import sleep

from .ScreenHelpers.PlayWordleRows import PlayWordleRows
from .Screen import Screen
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import RemoveErrorEvent


#TODO add keyboard.
    #Should auto pop up, but can add highlighting to show which letters are unavailable or should be used.
class PlayWordleScreen(Screen):
    def __init__(self, wordleRows: PlayWordleRows):
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.errorBox = toga.Box()
        self.errorThread = Thread(target=self.RemoveError)
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
        self.innerBox.remove(self.errorBox)
        self.errorBox = errorBox
        self.innerBox.add(self.errorBox)
        self.SetErrorTimeout()
    
        return self.outerBox
    
    def SetErrorTimeout(self): #Rename this as it doesn't set the timout
        if self.errorThread.is_alive():
            self.errorThread.cancel() #TODO need to set a flag and stuff to cancel the thread instead.
        self.errorThread = Thread(target=self.RemoveError)
        self.errorThread.start()

    def ErrorRemovalAfterTimeout(self):
        sleep(5)
        EventSystem.EventOccured(RemoveErrorEvent())
        #TODO create an event to remove error from current screen. Only the original thread can change the view.
            #Send the current screen too so that the screen manager can verify if the screen has changed
                #The screen could have changed, forward and back though. We might unwittingly remove the wrong error
                    #This will only be meaningful if we have another error, in which case we will have cancelled the first thread.

    def RemoveError(self):
        self.innerBox.remove(self.errorBox)
        return self.outerBox

