import random

from Guess import *
from CharCommonality import *
from Database import *
from WebScraper import *

#TODO test against the whole dataset if my 2 word starting combo performs better.

#TODO LIST
    # - Make the variety word work to completion
    # - Instead of randomly generated word, interface with the wordle site
    # - Make the solver avialable giving 1 word at a time, and getting the result from the user.
    # - Make that work through a simple GUI
    # - Allow the user to play it as a game by randomly selecting a word


def main():
    words, allowedWords = GetWords()

    TESTWORD = GetRandomWord(words)
    #TESTWORD = "boxer"
    #TESTWORD = "blame"
    #TESTWORD = "corer"
    TESTWORD = "bobby"
    print("Randomly selected word is:", TESTWORD)
    
    commonalityLookup = DetermineNumberOfOccurrences(words)
    print("Took ", RunGame(words, commonalityLookup, TESTWORD), "guesses")

def DetermineNumberOfOccurrences(words):
    charsLookup = CharCommonality()
    charsLookup.AddCommonality(words)
    return charsLookup

def DetermineGuess(commonalityLookup, words, numKnownLetters=0):
    #TODO Won't need to return bestScore once all setup
    bestScore = 0
    bestWord = []
    for word in words:
        score = commonalityLookup.RetriveCommonality(word)
        if score > bestScore:
            bestScore = score
            bestWord = [word]
        elif score == bestScore:
            bestWord.append(word)
    print("bestGuesses:", bestWord, "\n")

    #NOTE When we get a variety word for when there's still a lot of letters left, it only makes sense if we can get one with 4 or 5 letters otherwise we should return and use the best guess
        #same for when going down to 1 letter in variety. Should stop if can't find one with 2. --> Or even 3?

    #What if instead we look at num of different letters?
        #Compare that to the num known letters from last guess
    #print("NUMBER OF DIFFERENT LETTERS:", len(commonalityLookup.dicts[0]))
    
    #having a hard time with some of those double letters now.
        #Getting a vairety word doesn't currently take that into account, but now it might need to.

    try:
        if len(bestWord) >= 3 and len(words) < 8:
            #a commonality score for this word won't make sense, as some of the letters might be missing
            return Guess(PickVarietyWord(commonalityLookup, len(bestWord), minLetters=2)), 0
        if 3 < len(words) < 11:
            return Guess(PickVarietyWord(commonalityLookup, len(bestWord), minLetters=4)), 0
        if 11 < len(words) < 20:
            return Guess(PickVarietyWord(commonalityLookup, len(bestWord), minLetters=5)), 0
    except:
        print("Tried to get a variety word and failed")
        pass
            
    return Guess(bestWord[0]), bestScore

def LetterCombinations(letters, max=5):
    if len(letters) == max:
        return [letters]
    return _LCR(letters, max, combs=[])

def _LCR(letters, max=5, pos=0, curIdx=0, combs = [], curLetters = []):
    if (max-pos) == 0:
        combs.append(curLetters.copy())
        return combs

    for ii in range(curIdx, len(letters) - (max-pos-1)):
        curLetters.append(letters[ii])
        combs = _LCR(letters, max, pos+1, ii+1, combs, curLetters)
        del curLetters[-1]
    return combs

#TODO: Use this better alg for Picking a virety word:
#Different idea is to go through the valid words, keep track of the ones that contain the most of the letters we want.
        #exit as soon as there is one word with 5 of the letters we want
        #will need to check as we go also using the letters in letters[1] and letters[2] in case none match perfectly
            #maybe have some sort of score to give them, and keep track of the best word

        #NOTE: THIS^ is a better approach. Less calls to db, so faster. Also 1 pass of the data not multiple...

#Update this to work with double letters. Also maybe look at maybe using 2nd most common letters etc. when can't find a 4 or 5 letter word. 
    #becausee double/triple letters make this harder.
def PickVarietyWord(lookup, numWords, minLetters=2):
    print("Looking for the least common letters:")
    letters = lookup.GetLeastCommonLetters(numWords)
    print(letters)

    if len(letters) == 0:
        return "test non standard length word"
        #Is this ever triggered?

    ii = min(5, sum([len(k) for k in letters]))
    varietyWord = None
    while not varietyWord and ii >= minLetters:
        varietyWord = TryGetVarietyWord(letters, ii)
        ii -= 1

    #Should never trigger but you know how things go
    if not varietyWord:
        return "Non-standard word length"

    return varietyWord["word"]

def GetLetterCombinations(letters, maxLetters):
    if len(letters[0]) >= maxLetters:
        return LetterCombinations(letters[0], maxLetters)
    
    if len(letters) > 1:
        #Ahh yeah. Now we need to do something about this one!

        remNumLetters = 5 - len(letters[0])
        #TODO possibly, need to combine more than just the second lot. Possibly after all the combining, theres still not enough letters..
        #becomes tricky. cos, we want to prioritise ones in earlier lots
        remLettersCombs = LetterCombinations(letters[1], max = 5-remNumLetters)

        #so ffor each combonation, combine the first letters with the ones in the first set of letters.
        for comb in remLettersCombs:
            for letter in letters[0]:
                comb.append(letter)
        
        return remLettersCombs

        # so ahhh.
        #     THIS IS AN ISSUE
        #     TODO: MAYBE LETS DO THIS FIRST

        #use all the letters in all the sections but the last one
            #supplement to 5 letters from the last section. Make an or query using all such 5-letter combinations

            #The combinations will be different cos might be use these 3 letters, and all the 2 letter combs from the last one.
                #use _LCR to get the 2* letter combs and use a list comp to combine the others with it into a list of lists of 5 letters.
        pass

    #This shouldn't occur since maxLetters should be set correctly
    #It would occur if there are less letters then the given maxLetters
    return LetterCombinations(letters[0], len(letters[0]))

def TryGetVarietyWord(letters, maxLetters):
    letterCombs = GetLetterCombinations(letters, maxLetters)
    filter = GetFilterForCombinations(letterCombs)
    return FindOneAllowedWord(filter)

def GetFilterForCombinations(combinations):
    if (len(combinations) == 1):
        return GetAllLetterFilter(combinations[0])

    filter = "{"
    filter += "'$or': ["
    for combination in combinations:
        filter += GetAllLetterFilter(combination)
        filter += ", "
    filter = filter[:-2] + "]}"
    return filter

def GetAllLetterFilter(letters):
    filter = "{'$and': ["

    #Edit range to go one further, and then use -ve indexes to remove the comma
    #Then add the ending on last
    #TODO: add the check for if it's a double or triple letter...
    for ii in range(min(len(letters), 5)-1):

        filter += "{'word': {'$regex': '" + letters[ii] + "'}}, "
    filter += "{'word': {'$regex': '" + letters[min(len(letters)-1, 4)] + "'}}]}"

    return filter

def FilterWords(words, guess):
    return [word for word in words if guess.ConsistentWithGuess(word)]

def GetRandomWord(words):
    return random.choice(words)

def RunGame(validWords, commonalityLookup, answer):
    try:
        guess, score = DetermineGuess(commonalityLookup, validWords)
    except InvalidWordLength as e:
        print(e.message)
        return
    
    print("Best guess is:", guess.word, " With a score of:", score)
    correctGuess = guess.ValidateGuess(answer)
    guesses = 1

    while not correctGuess:
        validWords = FilterWords(validWords, guess)
        print("VALID WORDS:", validWords)
        commonalityLookup = DetermineNumberOfOccurrences(validWords)
        try:
            guess, score = DetermineGuess(commonalityLookup, validWords)
        except InvalidWordLength as e:
            print(e.message)
            return
        print("Best guess is:", guess.word, " With a score of:", score)
        correctGuess = guess.ValidateGuess(answer)
        guesses += 1
        
    return guesses

if __name__ == "__main__":
    main()
