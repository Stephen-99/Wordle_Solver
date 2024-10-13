import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from threading import Thread
import threading
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
        self.threadCancellations = []
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
    
    #Or could I do this some different way, ending the thread before rmoving the error so that another thread removes it.
    def SetErrorTimeout(self): #Rename this as it doesn't set the timout
        if self.errorThread.is_alive():
            self.threadCancellations[-1].set()
        self.errorThread = Thread(target=self.ErrorRemovalAfterTimeout)
        self.threadCancellations.append(threading.Event())
        self.errorThread.start()
        print("thread cancellations after starting thread:", self.threadCancellations)

    def ErrorRemovalAfterTimeout(self):
        sleep(5)
        print("thread cancellations before trying to raise event:", self.threadCancellations)
        if not self.threadCancellations[0].is_set():
            EventSystem.EventOccured(RemoveErrorEvent(PlayWordleScreen))
        del self.threadCancellations[0]
        #Only the original thread can change the view.
            #unfortunately, this means I will have to setup an architecture to send things to and from the gui thread.
            #Look how I did it in sec for the robots assignment.
        

    def RemoveError(self):
        self.innerBox.remove(self.errorBox)
        return self.outerBox

