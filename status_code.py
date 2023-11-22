from enum import Enum

class StatusCode(Enum):
    """
    Enumeration of status codes used in the UNO Messages.

    Attributes:
        CONNECTION_FAILED (int): Status code indicating a failed connection.
        CONNECTION_SUCCESS (int): Status code indicating a successful connection.
        GAME_START (int): Status code indicating the start of the game.
        GAME_STATE (int): Status code indicating the current game state.
        CARD_DRAW (int): Status code indicating a card draw action.
        INITIAL_DRAW (int): Status code indicating the initial draw of cards.
        CARD_PLAY (int): Status code indicating a card play action.
    """    
    CONNECTION_FAILED = 0
    CONNECTION_SUCCESS = 1
    GAME_START = 2
    GAME_STATE = 3
    CARD_DRAW = 4
    INITIAL_DRAW = 5
    CARD_PLAY = 6

class UnoMessage:
    """
    Represents a client/server message in the networked UNO game.
    """    
    def __init__(self, status_code, data=None):
        """
        Initializes a new UnoMessage instance.

        Args:
            status_code (StatusCode): The status code of the message.
            data (Any, optional): Additional data associated with the message.
        """        
        self.status_code = status_code
        self.data = data