import random

#HAve to think do I maybe instead want to decouple this so that the solver doesn't have anything to do with the eventSystem
#Otherewise I have to worry about wrapping every little edge case. Solver causes most of the events, makes sense for it to raise them
from WordleSolver.Events import EventSystem
from WordleSolver.Events.Events import *

import WordleLibrary.GUI as GUI
from .Guess import *
from .CharCommonality import *
from .Database import *
from .WebScraper import *

# TODO LIST
# - Instead of randomly generated word, interface with the wordle site (de-prioritised)
# - Allow the user to play it as a game by randomly selecting a word
# - Make an exe for easy windows deployment
# - Create a GUI pop up for erros instead of print statements
# - Make a mobile deployment (BeeWare)
# - Make database accessible from any device (only for reading though)


#TODO it's getting messy. Get it to work using the class, then can remove the rest.

#should be created upon creating colverScreen
#Or could have a setup solver, and setup playGame funtion. Then I only need 1 class.
class WordleSolver:
    def __init__(self):
        self.db = WordleDB()
        self.validWords, self.allowedWords = self.db.GetWords()
        self.lookup = CharCommonality(self.validWords)
        self.curGuess = None
        self.guesses = 0

    def resetSolver(self):
        self.validWords, self.allowedWords = self.db.GetWords()
        self.lookup = CharCommonality(self.validWords)
        self.curGuess = None
        self.guesses = 0

    def GetNextGuess(self):
        try:
            self.curGuess, score = self.DetermineGuess()
        except InvalidWordLength as e:
            print(e.message)
            return
        except IndexError as err:
            print("Invalid selection. There are no valid words left.")
            EventSystem.EventOccured(ErrorOccuredEvent("Invalid selection. There are no valid words left.")) #TODO show popup with message
            #So new windows are not supported on andriod and ios. RIP
                #Seems the best way to do it would be to show a new screen instead of a popup
                #TODO: create a new event for this error and screenmanager should handle it by showing the ErrorScreen
            return

        #    print("Best guess is:", guess.word, " With a score of:", score)

        EventSystem.EventOccured(NewWordEvent(self.curGuess.word))
        #TODO: can maybe remove this return
        return self.curGuess.word

    def ProcessGuessResults(self, res: list[LetterColour]):
        if res == None:
            #TODO reset state?
            self.gui.SetMainScreen()
            return

        self.guesses += 1
        correctGuess = self.curGuess.UserValidateGuess(res)
        if correctGuess:
            #This should never happen. They should press the correct guess button!
            #TODO reset state?
            self.gui.SetMainScreen()
            return

        self.FilterWords()
        self.DetermineNumberOfOccurrences()
        
        #TODO: can maybe remove this return
        return self.GetNextGuess()

    def DetermineGuess(self) -> tuple[Guess, int]:
        # TODO Won't need to return bestScore once all setup
        bestScore = 0
        bestWord = []
        for word in self.validWords:
            score = self.lookup.RetriveCommonality(word)
            if score > bestScore:
                bestScore = score
                bestWord = [word]
            elif score == bestScore:
                bestWord.append(word)
        #print("bestGuesses:", bestWord, "    Remaining number of valid words:", len(self.validWords))

        try:
            if len(bestWord) >= 2 and 2 < len(self.validWords) < 7:
                # a commonality score for this word won't make sense, as some of the letters might be missing
                return Guess(self.PickVarietyWord(minLetters=2)), 0
            if len(bestWord) >= 4 and 3 < len(self.validWords) < 11:
                return Guess(self.PickVarietyWord(minLetters=4)), 0
            if len(bestWord) >= 4 and 11 < len(self.validWords) < 20:
                return Guess(self.PickVarietyWord(minLetters=5)), 0
        except InvalidWordLength as e:
            pass

        return Guess(bestWord[0]), bestScore
    
    def PickVarietyWord(self, minLetters: int = 2) -> str:
        # print("Looking for the least common letters:")
        letters = self.lookup.GetLeastCommonLetters(self.validWords)

        # print(letters)

        if len(letters) < 2:
            return "A variety word is not helpful here"

        letterCombs = ProcessLeastCommonLetters(letters)

        ii = min(5, len(letterCombs[0]))
        varietyWord = None
        while not varietyWord and ii >= minLetters:
            varietyWord = self.TryGetVarietyWord(letterCombs, ii)
            ii -= 1

        # Should never trigger but you know how things go
        if not varietyWord:
            return "Non-standard word length"

        return varietyWord["word"]
    
    def TryGetVarietyWord(self, lettersOptionsByWord: list[list[str]], maxLetters: int) -> str:
        letterCombs = []
        for letters in lettersOptionsByWord:
            letterCombs.extend(GetLetterCombinations(letters, maxLetters))

        filter = GetFilterForCombinations(letterCombs)
        return self.db.FindOneAllowedWord(filter)
    
    def FilterWords(self) -> list[str]:
        self.validWords = [word for word in self.validWords if self.curGuess.ConsistentWithGuess(word)]

    def DetermineNumberOfOccurrences(self):
        self.lookup = CharCommonality(self.validWords)


def PlayWordle():
    db = WordleDB()
    words, allowedWords = db.GetWords()
    answer = GetRandomWord(words)

    try:
        guess = Guess(GUI.GetGuessFromUser())
    except InvalidWordLength as e:
        GUI.DisplayErrorMessage(e.message)
        return
    correctGuess = guess.ValidateGuess(answer)
    guesses = 1
    GUI.DisplayGuessResult(guess)

    while not correctGuess and guesses < 6:
        GUI.DisplayGuessResult(guess)
        try:
            guess = Guess(GUI.GetGuessFromUser())
        except InvalidWordLength as e:
            GUI.DisplayErrorMessage(e.message)
            return
        correctGuess = guess.ValidateGuess(answer)
        guesses += 1
        GUI.DisplayGuessResult(guess)

    if guesses < 6:
        GUI.DisplayWonScreen()
    else:
        GUI.DisplayLostScreen()


def RunWithoutGUI():
    db = WordleDB()
    words, allowedWords = db.GetWords()

    TESTWORD = GetRandomWord(words)
    TESTWORD = "boxer"
    print("Randomly selected word is:", TESTWORD)

    commonalityLookup = DetermineNumberOfOccurrences(words)
    print("Took ", RunGame(words, commonalityLookup, TESTWORD, db), "guesses")


def RunWithUserInput():
    db = WordleDB()
    words, allowedWords = db.GetWords()
    commonalityLookup = DetermineNumberOfOccurrences(words)
    SolveFromUser(words, commonalityLookup, db)


#--> --> --> DEPRECEATED <-- <-- <--
def SolveFromUser(
    validWords: list[str], commonalityLookup: CharCommonality, db: WordleDB
) -> int:
    try:
        guess, score = DetermineGuess(commonalityLookup, validWords, db)
    except InvalidWordLength as e:
        print(e.message)
        return
    except IndexError as err:
        print("Invalid selection. There are no valid words left.")
        return

    #    print("Best guess is:", guess.word, " With a score of:", score)
    guiGuessResults = GUI.ObtainGuessResults(guess.word)
    if not guiGuessResults:
        return

    correctGuess = guess.UserValidateGuess(guiGuessResults)

    guesses = 1

    while not correctGuess:
        validWords = FilterWords(validWords, guess)
        # print("VALID WORDS:", validWords)
        commonalityLookup = DetermineNumberOfOccurrences(validWords)
        try:
            guess, score = DetermineGuess(commonalityLookup, validWords, db)
        except InvalidWordLength as e:
            print(e.message)
            return
        except IndexError as err:
            print("Invalid selection. There are no valid words left.")
            return
        #        print("Best guess is:", guess.word, " With a score of:", score)
        guiGuessResults = GUI.ObtainGuessResults(guess.word)
        if not guiGuessResults:
            return

        correctGuess = guess.UserValidateGuess(guiGuessResults)

        guesses += 1

    return guesses

#--> --> --> DEPRECEATED <-- <-- <--
def DetermineNumberOfOccurrences(words: list[str]) -> CharCommonality:
    charsLookup = CharCommonality()
    charsLookup.AddCommonality(words)
    return charsLookup

#--> --> --> DEPRECEATED <-- <-- <--
def DetermineGuess(
    commonalityLookup: CharCommonality, words: list[str], db: WordleDB
) -> tuple[Guess, int]:
    # TODO Won't need to return bestScore once all setup
    bestScore = 0
    bestWord = []
    for word in words:
        score = commonalityLookup.RetriveCommonality(word)
        if score > bestScore:
            bestScore = score
            bestWord = [word]
        elif score == bestScore:
            bestWord.append(word)
    print("bestGuesses:", bestWord, "    Remaining number of valid words:", len(words))

    try:
        if len(bestWord) >= 2 and 2 < len(words) < 7:
            # a commonality score for this word won't make sense, as some of the letters might be missing
            return Guess(PickVarietyWord(commonalityLookup, db, words, minLetters=2)), 0
        if len(bestWord) >= 4 and 3 < len(words) < 11:
            return Guess(PickVarietyWord(commonalityLookup, db, words, minLetters=4)), 0
        if len(bestWord) >= 4 and 11 < len(words) < 20:
            return Guess(PickVarietyWord(commonalityLookup, db, words, minLetters=5)), 0
    except InvalidWordLength as e:
        pass

    return Guess(bestWord[0]), bestScore


def LetterCombinations(letters: list[str], max: int = 5) -> list[list[str]]:
    if len(letters) == max:
        return [letters]
    return _LCR(letters, max, combs=[])


def _LCR(
    letters: list[str],
    max: int = 5,
    pos: int = 0,
    curIdx: int = 0,
    combs: list[list[str]] = [],
    curLetters: list[str] = [],
) -> list[list[str]]:
    if (max - pos) == 0:
        combs.append(curLetters.copy())
        return combs

    for ii in range(curIdx, len(letters) - (max - pos - 1)):
        curLetters.append(letters[ii])
        combs = _LCR(letters, max, pos + 1, ii + 1, combs, curLetters)
        del curLetters[-1]
    return combs

#--> --> --> DEPRECEATED <-- <-- <--
def PickVarietyWord(
    lookup: CharCommonality, db: WordleDB, words: list[str], minLetters: int = 2
) -> str:
    # print("Looking for the least common letters:")
    letters = lookup.GetLeastCommonLetters(words)

    # print(letters)

    if len(letters) < 2:
        return "A variety word is not helpful here"

    letterCombs = ProcessLeastCommonLetters(letters)

    ii = min(5, len(letterCombs[0]))
    varietyWord = None
    while not varietyWord and ii >= minLetters:
        varietyWord = TryGetVarietyWord(letterCombs, ii, db)
        ii -= 1

    # Should never trigger but you know how things go
    if not varietyWord:
        return "Non-standard word length"

    return varietyWord["word"]


# converts them from a per word basis to a list of letter combinations.
# GetLetterCombinations can then take these and convert them to combinations based on the number of required letters
# like a 5 choose 3 type situation.
def ProcessLeastCommonLetters(LCLetters: list[list[str]]) -> list[list[str]]:
    letterCombs = []
    for letter in LCLetters[0]:
        if len(LCLetters) > 1:
            combs = ProcessLeastCommonLetters(LCLetters[1:])
            for comb in combs:
                comb.append(letter)
                letterCombs.append(comb)
        else:
            letterCombs.append([letter])
    return letterCombs


def GetLetterCombinations(letters: list[str], maxLetters: int) -> list[list[str]]:
    if len(letters) >= maxLetters:
        return LetterCombinations(letters, maxLetters)

    # This will occur if there are less letters then the given maxLetters
    return LetterCombinations(letters, len(letters))

#--> --> --> DEPRECEATED <-- <-- <--
def TryGetVarietyWord(
    lettersOptionsByWord: list[list[str]], maxLetters: int, db: WordleDB
) -> str:
    letterCombs = []
    for letters in lettersOptionsByWord:
        letterCombs.extend(GetLetterCombinations(letters, maxLetters))

    filter = GetFilterForCombinations(letterCombs)
    return db.FindOneAllowedWord(filter)


def GetFilterForCombinations(combinations: list[list[str]]) -> str:
    if len(combinations) == 1:
        return GetAllLetterFilter(combinations[0])

    filter = "{"
    filter += "'$or': ["
    for combination in combinations:
        filter += GetAllLetterFilter(combination)
        filter += ", "
    filter = filter[:-2] + "]}"
    return filter


def GetAllLetterFilter(letters: list[str]) -> str:
    filter = "{'$and': ["

    for ii in range(min(len(letters), 5) - 1):

        filter += "{'word': {'$regex': '" + letters[ii] + "'}}, "
    filter += "{'word': {'$regex': '" + letters[min(len(letters) - 1, 4)] + "'}}]}"

    return filter

#--> --> --> DEPRECEATED <-- <-- <--
def FilterWords(words: list[str], guess: Guess) -> list[str]:
    return [word for word in words if guess.ConsistentWithGuess(word)]


def GetRandomWord(words: list[str]) -> str:
    return random.choice(words)


def RunGame(
    validWords: list[str], commonalityLookup: CharCommonality, answer: str, db: WordleDB
) -> int:
    try:
        guess, score = DetermineGuess(commonalityLookup, validWords, db)
    except InvalidWordLength as e:
        print(e.message)
        return

    #    print("Best guess is:", guess.word, " With a score of:", score)
    correctGuess = guess.ValidateGuess(answer)
    guesses = 1

    while not correctGuess:
        validWords = FilterWords(validWords, guess)
        # print("VALID WORDS:", validWords)
        commonalityLookup = DetermineNumberOfOccurrences(validWords)
        try:
            guess, score = DetermineGuess(commonalityLookup, validWords, db)
        except InvalidWordLength as e:
            print(e.message)
            return
        #        print("Best guess is:", guess.word, " With a score of:", score)
        correctGuess = guess.ValidateGuess(answer)
        guesses += 1

    return guesses


#OLD WORLD
def main():
    GUI.DisplayStartScreen()

if __name__ == "__main__":
    main()
