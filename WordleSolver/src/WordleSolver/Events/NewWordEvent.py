from typing import List

#TODO make all events data classes
class NewWordEvent:
    def __init__(self, word: List[str]):
        self.word = word