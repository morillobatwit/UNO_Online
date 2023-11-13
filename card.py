from enum import Enum

class CardType(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    REVERSE = 10
    SKIP = 11
    DRAW_TWO = 12
    WILD = 13
    WILD_DRAW_FOUR = 14
    NONE = 15

class CardColor(Enum):
    RED = (230, 71, 52)#(200, 0, 0)
    GREEN = (97, 176, 57)#(0, 200, 0)
    BLUE = (50, 105, 169)#(0, 0, 200)
    YELLOW = (242, 199, 69)#(200, 200, 0)
    DARK = (50, 50, 50)

class UnoCard:
    def __init__(self, card_type, card_color):
        """
        Represents an UNO card

        Parameters
        ----------
        card_type : CardType
            a CardType element(Example: CardType.ONE).
        card_color : CardColor
            a CardColor element(Example: CardType.RED).

        """
        self._type = card_type
        self._color = card_color

    @property
    def type(self):
        return self._type

    @property
    def color(self):
        return self._color    
        