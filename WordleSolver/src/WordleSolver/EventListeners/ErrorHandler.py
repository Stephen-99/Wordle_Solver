import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

class ErrorHandler:
    def __init__(self):
        self.RegisterHandlers()

#TODO: make sure this is getting created and called.
    def RegisterHandlers(self):
        EventSystem.subscribe(ErrorOccuredEvent, self.ErrorOccured)

    def ErrorOccured(self, event: ErrorOccuredEvent):
        event.errorInfo.screenWithError.ShowError(self.CreateErrorBox(event.errorInfo.msg))
        #Should instead call the screen manager to update the current screen with the error message
        #May need to do that by raising a new type fo event.

    def CreateErrorBox(self, errorMsg: str):
        box = toga.Box(style=Pack(direction=COLUMN, background_color="#FFEBEE", padding=10))
        msgLabel = toga.Label(text=errorMsg, style=Pack(color="#FF0000", font_size=16, text_align='center'))

        box.add(msgLabel)
        return box


        #TODO, event will need to also have the screen it came from
            #It now does. Needs to be created in the right places though

        # Also have a function fro creating a box with the error message which can then be appended to the relevant screen.
            # Each screen should implement the generic screen which should have a method for adding temporary content to the bottom of the screen
            # Potentially this class should raise the event to take care of timeouts for the errors...
            # What about if they spam a button to raise a ton of errors. It will break the screen. We only want to allow for 1 at a time
                #This should be in the screen's implementation. They just have a box for it, and for each error set the content to that box
                    #This will mean the screen has knowledge of the last added error, so should be in charge of the tiemout.
#NOTE:
    #seems to eb an issue where thing doesn't say what word is invalid.