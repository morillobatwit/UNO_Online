from enum import Enum
import pygame 
from pygame.math import Vector2

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

class CardColor(Enum):
    RED = (230, 71, 52)#(200, 0, 0)
    GREEN = (97, 176, 57)#(0, 200, 0)
    BLUE = (50, 105, 169)#(0, 0, 200)
    YELLOW = (242, 199, 69)#(200, 200, 0)
    DARK = (50, 50, 50)

class UnoCard:
    def __init__(self, card_type, card_color):
        self._type = card_type
        self._color = card_color

    @property
    def type(self):
        return self._type

    @property
    def color(self):
        return self._color    

class UnoCardViewData:
    # Constants for Unicode values
    SKIP = '\U0001F6C7'
    REVERSE = '\U0001F5D8'
    DRAW_TWO = '\u2BBA'

    def __init__(self, uno_card):
        super().__init__()
        self._uno_card = uno_card
        self._display_text = self._card_type_unicode_value(uno_card)

    @property
    def uno_card(self):
        return self._uno_card
    
    @property
    def display_text(self):
        return self._display_text

    def _card_type_unicode_value(self, uno_card):
        if uno_card.type == CardType.SKIP:
            return UnoCardViewData.SKIP
        if uno_card.type == CardType.REVERSE:
            return UnoCardViewData.REVERSE
        if uno_card.type == CardType.DRAW_TWO:
            return UnoCardViewData.DRAW_TWO        
        else:
            return str(uno_card.type.value)


class UnoCardView(pygame.sprite.Sprite):
    # Constants for card dimensions
    WIDTH = 175
    HEIGHT = WIDTH * 1.5
    INNER_WIDTH = WIDTH - 10
    INNER_HEIGHT = HEIGHT - 15
    FONT_SIZE = 100
    FONT_COLOR = (255, 255, 255)    

    def __init__(self, u_card_v_dta):
        super().__init__()
        self._uno_card = u_card_v_dta.uno_card
        self._display_text = u_card_v_dta.display_text
        self._position = Vector2(0, 0)
        self.card_color = self._uno_card.color.value
        
        # CARD 
        self.rect = pygame.Rect(self._position, (UnoCardView.WIDTH, UnoCardView.HEIGHT))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # INNER RECT 
        self.inner_rect = pygame.Rect(self._position, (UnoCardView.INNER_WIDTH, UnoCardView.INNER_HEIGHT))
        self.inner_rect.center = (self.rect.width / 2, self.rect.height /2)

        font = pygame.font.Font('assets/Noto.ttf', UnoCardView.FONT_SIZE)
        small_font = pygame.font.Font('assets/Noto.ttf', 40)

        self.text_surface = font.render(self._display_text, True, UnoCardView.FONT_COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.inner_rect.center)

        self.text_topright = small_font.render(self._display_text, True, UnoCardView.FONT_COLOR)   
        self.text_topright.set_alpha(127)
        self.text_recttr = self.text_topright.get_rect(topleft=self.inner_rect.topleft)     

        self.text_botright = small_font.render(self._display_text, True, UnoCardView.FONT_COLOR)  
        self.text_botright.set_alpha(127) 
        self.text_rectbr = self.text_botright.get_rect(bottomright=self.inner_rect.bottomright)  

        self.draw_card()

    def draw_card(self):
        pygame.draw.rect(self.image, self.card_color, self.rect, border_radius=15)
        
        self.image.blit(self.text_surface, self.text_rect)
        self.image.blit(self.text_topright, self.text_recttr)
        self.image.blit(self.text_botright, self.text_rectbr)  
        


  

    
