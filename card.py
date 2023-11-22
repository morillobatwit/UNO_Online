from enum import Enum

class CardType(Enum):
    """
    Enum representing the types of UNO cards.


    Example Usage:
        card_type = CardType.ONE
        print(card_type)  # Output: CardType.ONE
    """    
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
    """
    Enum representing the colors of UNO cards.
    """    
    RED = (230, 71, 52)
    GREEN = (97, 176, 57)
    BLUE = (50, 105, 169)
    YELLOW = (242, 199, 69)
    DARK = (50, 50, 50)

class UnoCard:
    """
    Represents an UNO card(DTO).
    """    
    def __init__(self, card_type, card_color):
        """
        Initializes a new instance of the UnoCard class.

        Args:
            card_type (CardType): The type of the UNO card.
            card_color (CardColor): The color of the UNO card.
        """
        self._type = card_type
        self._color = card_color

    @property
    def type(self):
        """
        Gets the type of the UNO card.

        Returns:
            CardType: The type of the UNO card.
        """        
        return self._type

    @property
    def color(self):
        """
        Gets the color of the UNO card.

        Returns:
            CardColor: The color of the UNO card.
        """        
        return self._color    
        