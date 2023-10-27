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
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (0, 0, 200)
    YELLOW = (200, 200, 0)
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

class UnoCardView(pygame.sprite.Sprite):
    # Constants for card dimensions
    WIDTH = 200
    HEIGHT = 300
    FONT_SIZE = 100
    FONT_COLOR = (255, 255, 255)    

    def __init__(self, uno_card):
        super().__init__()
        self._uno_card = uno_card
        self._position = Vector2(0, 0)
        
        self.rect = pygame.Rect(self._position, (UnoCardView.WIDTH, UnoCardView.HEIGHT))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        self.card_color = self._uno_card.color.value

        font = pygame.font.SysFont('arial', UnoCardView.FONT_SIZE)
        self.text_surface = font.render(str(self._uno_card.type.value), True, UnoCardView.FONT_COLOR)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.draw_card()

    def draw_card(self):
        pygame.draw.rect(self.image, self.card_color, self.rect, border_radius=30)
        self.image.blit(self.text_surface, self.text_rect)


  

    
