from GUI import LetterColour, WordleStates


class Guess:
    def __init__(self, word: str):
        # TODO seems like a bad idea to have an exception in the constructor maybe make a GuessFactory to perform injection
        if len(word) != 5:
            raise InvalidWordLength()
        self.word = word
        self.correct = [False, False, False, False, False]
        self.misplaced = [False, False, False, False, False]
        self.incorrect = [False, False, False, False, False]

    def ValidateGuess(self, correctWord: str) -> bool:
        for ii in range(len(self.word)):
            if self.word[ii] == correctWord[ii]:
                self.correct[ii] = True
            elif self.word[ii] in correctWord:
                self.misplaced[ii] = True
            else:
                self.incorrect[ii] = True

        if False not in self.correct:
            return True
        return False

    def ValidateGuess(self, GUIReults: list[LetterColour]) -> bool:
        for result, ii in enumerate(GUIReults):
            match result.state:
                case WordleStates.INCORRECT:
                    self.incorrect[ii] = True
                case WordleStates.MISPLACED:
                    self.misplaced[ii] = True
                case WordleStates.CORRECT:
                    self.correct[ii] = True

        if False not in self.correct:
            return True
        return False

    def ConsistentWithGuess(self, word: str) -> bool:
        for ii in range(len(word)):
            if self.correct[ii] and (self.word[ii] != word[ii]):
                return False
            if self.incorrect[ii] and (self.word[ii] in word):
                return False
            if self.misplaced[ii] and (
                (self.word[ii] == word[ii]) or (self.word[ii] not in word)
            ):
                return False
        return True


class InvalidWordLength(Exception):
    def __init__(self, length: int = 5, message: str = "Word length must be "):
        self.message = message + str(length)
        super().__init__(self.message)
