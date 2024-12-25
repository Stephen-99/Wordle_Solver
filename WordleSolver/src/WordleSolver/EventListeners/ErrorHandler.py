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

    async def ErrorOccured(self, event: ErrorOccuredEvent):
        #event.errorInfo.screenWithError.ShowError(self.CreateErrorBox(event.errorInfo.msg))
        errorBox = self.CreateErrorBox(event.msg)
        EventSystem.EventOccured(ShowErrorContentEvent(errorBox))

        #Should instead call the screen manager to update the current screen with the error message
        #May need to do that by raising a new type fo event.

    def CreateErrorBox(self, errorMsg: str):
        box = toga.Box(style=Pack(direction=COLUMN, background_color="#FFEBEE", padding=10))
        msgLabel = toga.Label(text=errorMsg, style=Pack(color="#FF0000", font_size=16, text_align='center'))

        box.add(msgLabel)
        return box
