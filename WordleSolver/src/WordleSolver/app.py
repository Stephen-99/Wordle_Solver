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
            #THIS HAS BBECOME IMPORTANT. I'm now passing wordle rows everywhere :(
        solver = Solver()
        wordleRows = PlayWordleRows()
        playWordleClient = PlayWordle()
        ListenerCreator().SetupListeners(self.ChangeScreen, self.app.exit, solver, playWordleClient, wordleRows)


    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()


def main():
    return WordleSolver()

# This is a better place for updates:    
# I figured that to update the andorid build I need to run:   briefcase build android -u -r
# When doing that I finally got an update requirements installed, and it actually built!
# I ran it on the emulator, and it crashed :( But a start, and a way forward!

#fixed the missing packages, now crashing because it can't access the db since it doesn't have the password file
    #Need a longer term soln for this. Don't really want to ship with the password, although We could...

    #Could just send the password with itfor now as a temp soln. Or make separate account with less access so they can't erite, only read