from enum import Enum

class StatusCode(Enum):
    CONNECTION_FAILED = 0
    CONNECTION_SUCCESS = 1
    GAME_START = 2
    GAME_STATE = 3
    CARD_DRAW = 4
    INITIAL_DRAW = 5
    CARD_PLAY = 6

class UnoMessage:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self.data = data