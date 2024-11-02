"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga

from WordleLibrary.solver import WordleSolver as Solver
from WordleLibrary.PlayWordle import PlayWordle
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows
from .EventListeners.ListenerCreator import ListenerCreator

class WordleSolver(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        #TODO: Move these 2 into the Injector
        #I could instead do lazy initialization for the solver and playWordle objects. Have them as singletons
        #The listeners can create them as needed.
        solver = Solver()
        wordleRows = PlayWordleRows()
        playWordleClient = PlayWordle()

        ListenerCreator().SetupListeners(self.ChangeScreen, solver, playWordleClient, wordleRows)

    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()    

def main():
    return WordleSolver()

#  ~~~~~  Must do before releasing to play store  ~~~~~  #
    # Fix text not fitting on home screen ~~ :D ~~

#  ~~~~~  Like to do before releasing to play store  ~~~~~  #
    # Play wordle, jump to next box after entering a letter ~~ :D ~~
    # Play wordle, on clicking a box, set cursor to the start ~~ Don't seem to be able to move the cursor with Toga ~~
    # Cause errors to not send back to the home screen ~~ :D ~~
    # Add back buttons to playWordle and solver screens ~~ :D ~~
    # Allow players to input their own word choices and results so far
    # Fix long load times
    # 2nd letter only highlight if it is in the word twice.

#  ~~~~~  Would like to do  ~~~~~  #
    # putting GUI stuff on a separate thread. It's all single-threaded atm (done kinda)
    # Make it work for landscape, or enforce portrait mode
    # Nicer won and loss screens
    # An app logo