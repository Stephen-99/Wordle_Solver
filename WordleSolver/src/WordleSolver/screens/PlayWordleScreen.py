import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import asyncio
from threading import Thread

from .ScreenHelpers.PlayWordleRows import PlayWordleRows
from .Screen import Screen
from ..Events import EventSystem 
from ..Events.Events import ReturnToMainMenuEvent

#TODO add keyboard.
    #Should auto pop up, but can add highlighting to show which letters are unavailable or should be used.
class PlayWordleScreen(Screen):
    def __init__(self, wordleRows: PlayWordleRows, screenWidth):
        super().__init__(screenWidth)
        self.outerBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.innerBox = toga.Box(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.buttonBox = toga.Box(style=Pack(direction=ROW, alignment="center"))
        self.title = None
        self.submitButton = None
        self.backButton = None
        self.rows = wordleRows
        self.eventLoop = asyncio.get_event_loop()

    def CreateScreen(self):
        self.title = toga.Label("Guess the word!", style=Pack(padding=(2,5), font_size=self.ScaleValue(18), text_align='center'))
        self.submitButton = toga.Button("Submit", on_press=self.SubmitWordHandler, style=Pack(padding=5, font_size=self.ScaleValue(14), width=100))
        self.backButton = toga.Button("Back", on_press=self.BackButtonHandler, style=Pack(padding=5, font_size=self.ScaleValue(14), width=100))
        
        self.innerBox.add(self.title)
        self.rows.AddToBox(self.innerBox)
        self.buttonBox.add(self.submitButton, self.backButton)
        self.innerBox.add(self.buttonBox)
    
        self.outerBox.add(self.innerBox)

    def SubmitWordHandler(self, widget) -> None:
        self.rows.SetNewCurRow()

    def BackButtonHandler(self, widget) -> None:
        EventSystem.EventOccured(ReturnToMainMenuEvent())

    def UpdateScreen(self):
        return self.outerBox
    
    def ShowError(self, errorBox: toga.Box):
        self.innerBox.remove(self.errorBox)
        self.errorBox = errorBox
        self.innerBox.add(self.errorBox)
        self.SetErrorTimeout()
    
        return self.outerBox
    
    async def RemoveError(self):
        self.innerBox.remove(self.errorBox)

