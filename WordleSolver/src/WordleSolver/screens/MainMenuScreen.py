import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import Screen


class MainMenuScreen(Screen):
    def __init__(self):
        self.mainBox = toga.Box(style=Pack(direction=COLUMN, alignment='center'))