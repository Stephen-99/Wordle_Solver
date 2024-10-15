import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from threading import Thread
import threading
from time import sleep

from .ScreenHelpers.PlayWordleRows import PlayWordleRows
from .Screen import Screen

#TODO add keyboard.
    #Should auto pop up, but can add highlighting to show which letters are unavailable or should be used.
class PlayWordleScreen(Screen):
    def __init__(self, wordleRows: PlayWordleRows):
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.errorBox = toga.Box()
        self.errorThread = Thread(target=self.RemoveError)
        self.threadCancellations = []
        self.title = None
        self.submitButton = None
        self.rows = wordleRows
        self.eventLoop = asyncio.get_event_loop()

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
    
    #Once it's all sorted out, these 4 functions can be defined in some error handling class that Screen can inherit from.
    #This way all screens get it for free. This threads logic shouldn't have to be repeated everywhere.
    #This ShowError msg might be different for each screen. 
        #I could have a public method in errorHandler which gets called when the error occurs, and in turn calls the method in screen.
        #That way I can wrap it to always SetErrorTimeout. The screen shouldn't neeed to know about that.
    def ShowError(self, errorBox: toga.Box):
        self.innerBox.remove(self.errorBox)
        self.errorBox = errorBox
        self.innerBox.add(self.errorBox)
        self.SetErrorTimeout()
    
        return self.outerBox
    
    def SetErrorTimeout(self): #Rename this as it doesn't set the timout
        if self.errorThread.is_alive():
            self.threadCancellations[-1].set()
        self.errorThread = Thread(target=self.ErrorRemovalAfterTimeout)
        self.threadCancellations.append(threading.Event())
        self.errorThread.start()

    #Currently no check if it's still the same screen. 
    #This is ok since we want to remove the error from it even if it's not the current screen
        #Potentially if they go forward and back screens, we want the screen to refresh without the error
        #Then the remove error could be triggered when we don't want it to
            #This should be very easy to fix. Simply set all the cancellations.
    
    def ErrorRemovalAfterTimeout(self):
        sleep(5)
        if not self.threadCancellations[0].is_set():
            asyncio.ensure_future(self.RemoveError(), loop=self.eventLoop)
        del self.threadCancellations[0]

    async def RemoveError(self):
        self.innerBox.remove(self.errorBox)
        return self.outerBox
