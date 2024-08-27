from WordleSolver.screens.Screen import Screen

class ErrorInfo:
    def __init__(self, msg: str, screenWithError: Screen):
        self.msg = msg
        self.screenWithError = screenWithError