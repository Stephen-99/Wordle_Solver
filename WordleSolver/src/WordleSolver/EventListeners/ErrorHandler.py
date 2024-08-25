from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

class ErrorHandler:
    def __init__(self):
        self.RegisterHandlers()

    def RegisterHandlers(self):
        EventSystem.subscribe(ErrorOccuredEvent, self.ErrorOccured)

    def ErrorOccured(self, event: ErrorOccuredEvent):
        print(event.errorMsg)
        #TODO, event will need to also have the screen it came from
        # Also have a function fro creating a box with the error message which can then be appended to the relevant screen.
            # Each screen should implement the generic screen which should have a method for adding temporary content to the bottom of the screen
            # Potentially this class should raise the event to take care of timeouts for the errors...
            # What about if they spam a button to raise a ton of errors. It will break the screen. We only want to allow for 1 at a time
                #This should be in the screen's implementation. They just have a box for it, and for each error set the content to that box
                    #This will mean the screen has knowledge of the last added error, so should be in charge of the tiemout.
