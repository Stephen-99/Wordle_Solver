import toga

import asyncio
from threading import Thread
import threading
from time import sleep

class Screen:
    def __init__(self):
        self.errorThread = Thread(target=self.ErrorRemovalAfterTimeout)
        self.threadCancellations = []
        self.errorBox = toga.Box()

    def CreateScreen(self):
        raise NotImplementedError("This should be implemented by all child classes")
    
    def UpdateScreen(self):
        raise NotImplementedError("This should be implemented by all child classes")
    
    def ShowError(self, errorBox: toga.Box):
        raise NotImplementedError("This should be implemented by all child classes")
    
    async def RemoveError(self):
        raise NotImplementedError("This should be implemented by all child classes")
    
    
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

