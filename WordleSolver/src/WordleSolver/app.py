"""
This is an app that solves the wordle with you! It also allows you to play a wordle replica
"""
import toga

from WordleLibrary.solver import WordleSolver as Solver
from WordleLibrary.Database import WordleDB
from WordleLibrary.PlayWordle import PlayWordle
from WordleSolver.screens.ScreenHelpers.PlayWordleRows import PlayWordleRows
from .EventListeners.ListenerCreator import ListenerCreator

class WordleSolver(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        db = WordleDB()
        validWords, allowedWords = db.GetWords()

        solver = Solver(db, validWords, allowedWords) #takes 1.6s, but onlly 0.2s cpu time
        wordleRows = PlayWordleRows()
        playWordleClient = PlayWordle(validWords, allowedWords)  #takes 1.26s but only 0.17s CPU time

        ListenerCreator().SetupListeners(self.ChangeScreen, solver, playWordleClient, wordleRows)

    def ChangeScreen(self, screenContent):
        self.main_window.content = screenContent
        self.main_window.show()    

def main():
    return WordleSolver()

#  ~~~~~  Must do before releasing to play store  ~~~~~  #
    # Fix text not fitting on home screen ~~ :D ~~
    # Register for google play Developer account ~~ :D ~~
    # Create a 512x512px icon and use it for the app ~~ :D ~~
    # Take 2+ screenshots using the emulator ~~ :D ~~
    # Take a 1024x500px feature graphic
    # Create a store listing
    # Create a buy me a coffee link ~~ :D ~~
    # Update readme. ~~ :D ~~ Could add some screenshots still. Will also need play store link

#  ~~~~~  Like to do before releasing to play store  ~~~~~  #
    # Play wordle, jump to next box after entering a letter ~~ :D ~~
    # Play wordle, on clicking a box, set cursor to the start ~~ Don't seem to be able to move the cursor with Toga ~~
    # Cause errors to not send back to the home screen ~~ :D ~~
    # Add back buttons to playWordle and solver screens ~~ :D ~~
    # Allow players to input their own word choices and results so far ~~ :D ~~
    # Fix long initial load times --> Reduced ~~ :D ~~
    # Make it work on Windows ~~ :D ~~
    # 2nd letter only highlight if it is in the word twice.
    # Update release version to be 1.0.0 not 0.0.1

#  ~~~~~  Would like to do  ~~~~~  #
    # putting GUI stuff on a separate thread. It's all single-threaded atm (done kinda)
    # Make it work for landscape, or enforce portrait mode --> only play wordle doesn't fit landscape
    # Nicer won and loss screens