from enum import Enum

class StatusCode(Enum):
    CONNECTION_FAILED = 0
    CONNECTION_SUCCESS = 1
    GAME_START = 2
    IN_TURN = 3
    DISCARD_CARD = 4
    CARD_DRAW = 5
    INITIAL_DRAW = 6
    CARD_PLAY = 7
    CARD_PLAY_NOTIFICATION = 8

class UnoMessage:
    def __init__(self, status_code, data=None):
        self.status_code = status_code
        self.data = data