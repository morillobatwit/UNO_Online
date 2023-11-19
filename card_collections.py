import random
from card import UnoCard, CardType, CardColor

class UnoDeck:
    def __init__(self):
        self._cards = self._generate_deck()

    def _generate_deck(self):
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
        random.shuffle(self._cards)

    def draw_card(self):
        if self._cards:
            return self._cards.pop()
        else:
            raise ValueError("Cannot draw a card from an empty deck")

    def __len__(self):
        return len(self._cards)
    
    def add(self, uno_card):
        self._cards.add(uno_card)  

    @property
    def cards(self):
        return self._cards.copy()
    
class UnoHand:
    def __init__(self, card_group, x = 0, y = 0):
        self.card_group = card_group
        self._x = x
        self._y = y
        
    def add_card(self, card_view):
        self.card_group.add(card_view)
        self.organize_cards()
        
    def organize_cards(self):
        current_x = self._x
        current_y = self._y
        for card in self.card_group:
            card.rect.bottom = current_y
            card.rect.x = current_x
            card.set_initial_pos(card.rect.x, card.rect.y)
            current_x = card.rect.right + 10 # margin between cards

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.organize_cards()

    def blitme(self, surface):
        self.card_group.draw(surface) 

    @property
    def cards(self):
        return self.card_group              
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        