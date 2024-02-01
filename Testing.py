from solver import *

#This project is just for FUN. The testing here is minimal. 

class Testing:
    def __init__(self):
        self.wordsLostTo = ['foyer', 'goner', 'homer', 'boxer']
        self.db = WordleDB()   
        #self.wordsLostTo = ['joker', 'match', 'paste', 'watch', 'safer', 'taste']

    def TestWordsLostTo(self):
        self.words = self.db.GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        scores = []
        for word in self.wordsLostTo:
            guesses = RunGame(self.words, lookup, word, self.db)
            scores.append(guesses)
            print("\n", 50 * '-', "\n")
        print("\n\nNUMBER OF GUESSES FOR EACH WORD:\n", scores)

    #TODO set a flag to remove printing in code...
    def TestAllWords(self):
        self.words = self.db.GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        scores = []
        count = 0
        for word in self.words:
            guesses = RunGame(self.words, lookup, word, self.db)
            scores.append(guesses)
            if (guesses > 6):
                print(word, "This word failed taking", guesses, "guesses")
            count += 1
            if count % 20 == 0:
            #if count > 1460:  #got up to 213. 214 fails..
                print("just finished number", count)

        print("\n\nRESULTS:\n", scores)
        print("\nAverage: ", sum(scores)/len(scores))
        print("\nNum losses: ", len([k for k in scores if k > 6]))
    
    def TestOneWord(self):
        ii = -336
        
        self.words = self.db.GetAnswers()
        lookup = DetermineNumberOfOccurrences(self.words)
        print("word is: ", self.words[ii])
        res = RunGame(self.words, lookup, self.words[ii], self.db)
        print("\n\nTOOK: ", res, " GUESSES")

    def TestGetAllLettersFilter(self):
        allowedWords = self.db.GetAllowedWords()

        #5 letters with no valid words
        filter = GetAllLetterFilter(['a', 'b', 'c', 'd', 'e'])
        res = allowedWords.find_one(eval(filter))
        assert res == None
        
        #5 letters with one valid word
        filter = GetAllLetterFilter(['a', 'i', 'u', 'd', 'e'])
        res = allowedWords.find_one(eval(filter))
        assert res['word'] == 'adieu'


    #just prints what the results were for future reference.
    def LookupUpdateImpact(self):
        print("avg with lookup updates: 3.692")
        print("avg without lookup updates: 3.810")

        print("Number of times lookup was better:", 738)
        print("Number of times without lookup was better:", 565)
        print("Number of times they were equal:", 1006)
        print("Number of times lookup lost:", 18)
        print("Number of times without lookup lost:", 36)

        #UPDATED:
            #4 & 7: L - 4, avg - 3.67

        #TODO: check which are the ones that lose tho
        #3 & 9: 3.692 avg Losses = 5
        #3 & 8: 3.686 avg Losses = 4
        #3 & 7: 3.682 avg Losses = 4
        #3 & 6: 3.683 avg Losses = 4
        #3 & 5: 3.689 avg losses = 4
        #3 & 4: 3.698 avg losses = 19

        #4 & 7: 3.665 avg losses = 4

        #5 & 7: 3.674 avg losses = 5
        #2 & 11: 3.848 avg losses = 7

        #HYBRID:
        #3 & 8,  2 & 11  avg = 3.719  losses = 4


    def TestGetLetterCombinations(self):
        result = GetLetterCombinations([['a', 'b'], ['c', 'd']], 5)
        print(f"Result from using the letters [['a', 'b'], ['c', 'd']]: {result}")
        result = GetLetterCombinations([['a', 'b'], ['c'], ['d']], 5)
        print(f"Result from using the letters [['a', 'b'], ['c'], ['d']]: {result}")
        result = GetLetterCombinations([['a', 'b'], ['c'], ['d', 'e', 'f']], 5)
        print(f"Result from using the letters [['a', 'b'], ['c'], ['d', 'e', 'f']]: {result}")

            #also if we have: [[a, b,], [c], [d], [e]]
#Testing().TestWordsLostTo()
#Testing().TestGetAllLettersFilter()
Testing().TestAllWords()
#Testing().TestGetLetterCombinations()
#Testing().TestOneWord()