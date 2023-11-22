import random
from card import UnoCard, CardType, CardColor

class UnoDeck:
    """
    Represents a deck of Uno cards.
    """    
    def __init__(self):
        """
        Initializes the UnoDeck by generating a standard Uno deck.
        """        
        self._cards = self._generate_deck()

    def _generate_deck(self):
        """
        Private method to generate the standard Uno deck.
        """        
        deck = []
        for color in CardColor:
            if color == CardColor.DARK:
                continue
            deck.append(UnoCard(CardType.ZERO, color))
            for _ in range(2):
                for card_type in list(CardType)[1:13]:
                    deck.append(UnoCard(card_type, color))
        for _ in range(4):
            deck.append(UnoCard(CardType.WILD, CardColor.DARK))
            deck.append(UnoCard(CardType.WILD_DRAW_FOUR, CardColor.DARK))
        return deck

    def shuffle(self):
        """
        Shuffles the deck randomly.
        """        
        random.shuffle(self._cards)

    def draw_card(self):
        """
        Draws a card from the top of the deck.

        Returns:
            UnoCard: The drawn Uno card.

        Raises:
            ValueError: If the deck is empty.
        """        
        if self._cards:
            return self._cards.pop()
        else:
            raise ValueError("Cannot draw a card from an empty deck")

    def __len__(self):
        """
        Returns the number of cards in the deck.
        """        
        return len(self._cards)
    
    def add(self, uno_card):
        """
        Adds an UnoCard to the deck.

        Args:
            uno_card (UnoCard): The Uno card to be added.
        """        
        self._cards.add(uno_card)  

    @property
    def cards(self):
        """
        Returns a copy of the list of UnoCard objects in the deck.
        """        
        return self._cards.copy()
    
class UnoHand:
    """
    Represents a player's hand in Uno.
    """    
    def __init__(self, card_group, x = 0, y = 0):
        """
        Initializes the UnoHand.

        Args:
            card_group (SpriteGroup): A Pygame sprite group 
            containing UnoCard objects.
            x (int): X-coordinate position of the hand (default is 0).
            y (int): Y-coordinate position of the hand (default is 0).
        """        
        self.card_group = card_group
        self._x = x
        self._y = y
        
    def add_card(self, card_view):
        """
        Adds an UnoCard to the hand and organizes the cards.

        Args:
            card_view (UnoCard): The Uno card to be added.
        """        
        self.card_group.add(card_view)
        self.organize_cards()
        
    def organize_cards(self):
        """
        Organizes the cards in the hand.
        """        
        current_x = self._x
        current_y = self._y
        for card in self.card_group:
            card.rect.bottom = current_y
            card.rect.x = current_x
            card.set_initial_pos(card.rect.x, card.rect.y)
            current_x = card.rect.right + 10 # margin between cards

    @property
    def x(self):
        """
        Returns the X-coordinate position of the hand.
        """        
        return self._x
    
    @x.setter
    def x(self, value):
        """
        Sets the X-coordinate position of the hand and organizes the cards.

        Args:
            value (int): The new X-coordinate position.
        """        
        self._x = value
        self.organize_cards()

    def blitme(self, surface):
        """
        Draws the hand on the specified surface.

        Args:
            surface: The surface on which to draw the hand.
        """        
        self.card_group.draw(surface) 

    @property
    def cards(self):
        """
        Returns the Pygame sprite group containing UnoCard objects.
        """        
        return self.card_group              
            
