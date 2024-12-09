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
        #This is correct. we seem to lose some veritcal space to navigation bars, but the width is accurate.
        print("\n\n~~~~~~~ Screen Size:", self.screens[0].size.width , "~~~~~~~\n\n")
        self.main_window = toga.MainWindow(title=self.formal_name)
        db = WordleDB()
        validWords, allowedWords = db.GetWords()

        solver = Solver(db, validWords, allowedWords) #takes 1.6s, but onlly 0.2s cpu time
        wordleRows = PlayWordleRows()
        playWordleClient = PlayWordle(validWords, allowedWords)  #takes 1.26s but only 0.17s CPU time

        ListenerCreator().SetupListeners(self.ChangeScreen, solver, playWordleClient, wordleRows, self.screens[0].size.width)

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
    # Create a buy me a coffee link ~~ :D ~~
    # Make sure my app is compliant with all play store policies ~~ :D ~~ Looks like no issues
    # Update readme. ~~ :D ~~ Could add some screenshots still. Will also need play store link
    # Update windows msi to work with self-signed cert. ~~ It's not trusted anyway, and I don't want to pay for a cert, so not going to do this ~~
    # Take a 1024x500px feature graphic ~~ :D ~~
    # Course for publishing app ~~ :D ~~
    # Self-sign the android app bundle ~~ :D ~~
    # Test on my phone ~~ :D ~~
    # Create a store listing
    # Scale display based on device size -- currently solver doesn't work portrait mode TEST STILL
    


#  ~~~~~  Like to do before releasing to play store  ~~~~~  #
    # Play wordle, on clicking a box, set cursor to the start ~~ Don't seem to be able to move the cursor with Toga ~~
    # 2nd letter only highlight if it is in the word twice.
    # Update release version to be 1.0.0 not 0.0.1 ~~ Issues. On windows uninstall still shows 0.0.1 This is due to a bug. just accept it.
    # Allow backspace to work
    # On loss, say what the word was

#  ~~~~~  Would like to do  ~~~~~  #
    # putting GUI stuff on a separate thread. It's all single-threaded atm (done kinda)
    # Make it work for landscape, or enforce portrait mode --> only play wordle doesn't fit landscape
    # Nicer won and loss screens