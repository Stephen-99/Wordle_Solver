class CharCommonality:
    def __init__(self):
        #First one is number of words with that char, 2nd number of words with it twice etc.
        self.dicts = [{}, {}, {}]
    
    def AddCommonality(self, words):
        for word in words:
            charCount = CharCommonality.CharOccurrencesInWord(word)
            for char, count in charCount.items():
                for ii in range(count):
                    self._AddCharCommonality(char, ii)

    def RetriveCommonality(self, word):
        charCount = CharCommonality.CharOccurrencesInWord(word)

        commonality = 0
        for char, count in charCount.items():
            for ii in range(count):
                commonality += self._GetCharCommonality(char, ii)
        return commonality

    def GetLeastCommonLetters(self, inclDblAndTripleLetters = False):
        charsList = list(self.dicts[0].items())
        charsList.extend([((k[0], 2), k[1]) for k in self.dicts[1].items()])
        charsList.extend([((k[0], 3), k[1]) for k in self.dicts[2].items()])

        sortedList = sorted(charsList, key = lambda x: x[1])

        #TODO feels like bad code. Refactor it to be better
        leastCommonLetters = []
        lastVal = 0
        ii = -1
        count = 0
        #May need to adjust this so it doesn't stop a 5. Also may need to change alg, otherwise it may force dbl letters too early
        for charNVal in sortedList:
            if (count >= 5) and (charNVal[1] > lastVal):
                break
            if len(charNVal[0]) > 1:
                if (self._GetCharCommonality(charNVal[0][0], charNVal[0][1]-2)) <= charNVal[1]:
                    continue  
            if (charNVal[1] > lastVal):
                #Only add double/triple letters if there are more single or double letters for that char
                leastCommonLetters.append([])
                ii += 1
       
            leastCommonLetters[ii].append(charNVal[0])
            count += 1
            lastVal = charNVal[1]

        if not inclDblAndTripleLetters:
            #double/triple letters are always at the back.
            while type(leastCommonLetters[0][-1]) is tuple:
                del leastCommonLetters[0][-1]
                if len(leastCommonLetters[0]) == 0:
                    del leastCommonLetters[0]

        return leastCommonLetters

    def _GetCharCommonality(self, char, index):
        try:
            return self.dicts[index][char]
        except (IndexError, KeyError):
            #Not in dictionary
            return 0

    def _AddCharCommonality(self, char, index):
        try:
            if char in self.dicts[index]:
                self.dicts[index][char] += 1
            else:
                self.dicts[index][char] = 1
        except IndexError:
            print("\n\nERROR:\tCouldn't add commonality for a word with the same letter", index+1, "times\n\n")

    def CharOccurrencesInWord(word):
        charCount = {}
        for char in word:
            if char in charCount:
                charCount[char] += 1
            else:
                charCount[char] = 1
        return charCount
