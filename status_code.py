from enum import Enum

class StatusCode(Enum):
    CONNECTION_FAILED = 0
    CONNECTION_SUCCESS = 1
    GAME_START = 2
    IN_TURN = 3
    NOTIFICATION = 4
    CARD_DRAW = 5
    INITIAL_DRAW = 6

class UnoResponse:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self.data = data
        
class UnoRequest:
    def __init__(self, status_code):
        self.status_code = status_code