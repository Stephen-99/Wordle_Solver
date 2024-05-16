import random

import WordleLibrary.GUI as GUI 
from WordleLibrary.Guess import *
from WordleLibrary.CharCommonality import *
from WordleLibrary.Database import *
from WordleLibrary.WebScraper import *

# TODO LIST
# - Instead of randomly generated word, interface with the wordle site (de-prioritised)
# - Allow the user to play it as a game by randomly selecting a word
# - Make an exe for easy windows deployment
# - Create a GUI pop up for erros instead of print statements
# - Make a mobile deployment (BeeWare)
# - Make database accessible from any device (only for reading though)

#TODO: either make this into a class or pass the new WordleSolverGui areound everywhere
    #It should be a class.

class WordleSolver:
    def __init__(self, gui):
        self.db = WordleDB()
        self.lookup = CharCommonality()
        self.words, self.allowedWords = self.db.GetWords()
        self.gui = gui

    #To migrate from this:
        #DetermineGuess
        #GUI.ObtainGuessResult
        #FilterWords
        #DetermineNumberOfOccurrences
        #
    def SolveFromUser(self, validWords: list[str]) -> int:
        try:
            guess, score = DetermineGuess(self.lookup, validWords, self.db)
        except InvalidWordLength as e:
            print(e.message)
            return
        except IndexError as err:
            print("Invalid selection. There are no valid words left.")
            return

        #    print("Best guess is:", guess.word, " With a score of:", score)

        self.gui.SetSolverScreen(guess.word)

        #TODO: Have to set it up to wait here for GUI results...
            #Need state. May need multiple classes so solver aspect is separate
                #look after things like number of guesses etc.
                #Then we can easily pass a callback function to get called with results when thingo
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
                guess, score = DetermineGuess(commonalityLookup, validWords, self.db)
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


def DetermineNumberOfOccurrences(words: list[str]) -> CharCommonality:
    charsLookup = CharCommonality()
    charsLookup.AddCommonality(words)
    return charsLookup


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
