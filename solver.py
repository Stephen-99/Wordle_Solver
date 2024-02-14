import random

from Guess import *
from CharCommonality import *
from Database import *
from WebScraper import *

#TODO LIST
    # - Make the variety word work to completion
    # - Instead of randomly generated word, interface with the wordle site
    # - Make the solver avialable giving 1 word at a time, and getting the result from the user.
    # - Make that work through a simple GUI
    # - Allow the user to play it as a game by randomly selecting a word


#TODO: add type hinting on method signatures
def main():
    db = WordleDB()
    words, allowedWords = db.GetWords()

    TESTWORD = GetRandomWord(words)
    TESTWORD = "match"
    print("Randomly selected word is:", TESTWORD)
    
    commonalityLookup = DetermineNumberOfOccurrences(words)
    print("Took ", RunGame(words, commonalityLookup, TESTWORD, db), "guesses")

def DetermineNumberOfOccurrences(words):
    charsLookup = CharCommonality()
    charsLookup.AddCommonality(words)
    return charsLookup

def DetermineGuess(commonalityLookup, words, db, numKnownLetters=0):
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
    #print("bestGuesses:", bestWord, "    Remaining number of valid words:", len(words))

    #NOTE When we get a variety word for when there's still a lot of letters left, it only makes sense if we can get one with 4 or 5 letters otherwise we should return and use the best guess
        #same for when going down to 1 letter in variety. Should stop if can't find one with 2. --> Or even 3?

    #What if instead we look at num of different letters?
        #Compare that to the num known letters from last guess
    #print("NUMBER OF DIFFERENT LETTERS:", len(commonalityLookup.dicts[0]))
    
    #having a hard time with some of those double letters now.
        #Getting a vairety word doesn't currently take that into account, but now it might need to.

    

    try:
        #Add extra condition for if len(bestWord) == len(words) and len(bestWords) >= 3
        if len(bestWord) >= 2 and 2 < len(words) < 7:
            #a commonality score for this word won't make sense, as some of the letters might be missing
            return Guess(PickVarietyWord(commonalityLookup, db, words, minLetters=2)), 0
        if len(bestWord) >= 4 and 3 < len(words) < 11:
            return Guess(PickVarietyWord(commonalityLookup, db, words, minLetters=4)), 0
        if len(bestWord) >= 4 and 11 < len(words) < 20:
            return Guess(PickVarietyWord(commonalityLookup, db, words, minLetters=5)), 0
    except InvalidWordLength as e:
        #print("Tried to get a variety word and failed")
        #print(e)
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

def PickVarietyWord(lookup, db, words, minLetters=2):
    #print("Looking for the least common letters:")
    letters = lookup.GetLeastCommonLetters(words)

    #print(letters)

    if len(letters) < 2:
        return "A variety word is not helpful here"

    if len(letters) == 0:
        return "test non standard length word"
        #Is this ever triggered?

    letterCombs = ProcessLeastCommonLetters(letters)
    #TODO use new letterCombs instead of letters


    #ii = min(5, sum([len(k) for k in letters]))
    ii = min(5, len(letterCombs[0]))
    varietyWord = None
    while not varietyWord and ii >= minLetters:
        varietyWord = TryGetVarietyWord(letterCombs, ii, db)
        ii -= 1

    #Should never trigger but you know how things go
    if not varietyWord:
        return "Non-standard word length"

    return varietyWord["word"]

#converts them from a per word basis to a list of letter combinations.
#GetLetterCombinations can then take these and convert them to combinations based on the number of required letters
#like a 5 choose 3 type situation.
#TODO see if an iterative or cached (dynamic porgramming) soln would be significantly faster.
    #It doesn't appear to be slow for the 2000+ word test where all the words get solved.
def ProcessLeastCommonLetters(LCLetters):
    letterCombs = []
    #TODO, breaks on empty lists for a word. So need a recursive wrapper to remove these empty lists.
    for letter in LCLetters[0]:
        if len(LCLetters) > 1:
            combs = ProcessLeastCommonLetters(LCLetters[1:])
            for comb in combs:
                comb.append(letter)
                letterCombs.append(comb)
        else:
            letterCombs.append([letter])     
    return letterCombs

def GetLetterCombinations(letters, maxLetters):
    if len(letters) >= maxLetters:
        return LetterCombinations(letters, maxLetters)
    
    #This will occur if there are less letters then the given maxLetters
    return LetterCombinations(letters, len(letters))

def TryGetVarietyWord(lettersByWord, maxLetters, db):
    letterCombs = []
    for letters in lettersByWord:
        letterCombs.extend(GetLetterCombinations(letters, maxLetters))
    
    filter = GetFilterForCombinations(letterCombs)
    return db.FindOneAllowedWord(filter)

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

def RunGame(validWords, commonalityLookup, answer, db):
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
        #print("VALID WORDS:", validWords)
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

if __name__ == "__main__":
    main()
