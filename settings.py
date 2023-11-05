from enum import Enum

class Settings:
    """A class to store all settings for a UNO game"""
    
    class ImageResources(Enum):
        SKIP_DIR = 'resources/skip.png'
        REVERSE_DIR = 'resources/reverse.png'
        DRAW_TWO_DIR = 'resources/draw_two.png'
        DRAW_FOUR_DIR = 'resources/draw_four.png'

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.title = 'UNO'
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (0, 16, 62, 255)
        
        # Font settings
        self.FONT_DIR = 'resources/arial.ttf'
        self.CARD_CENTER_FONT_SIZE = 90
        self.CARD_EDGE_FONT_SIZE = self.CARD_CENTER_FONT_SIZE - 60
        self.CARD_FONT_COLOR = (255, 255, 255) 

        # Card settings   
        self.CARD_WIDTH = 175
        self.CARD_HEIGHT = self.CARD_WIDTH * 1.5
        self.CARD_INNER_WIDTH = self.CARD_WIDTH - 10
        self.CARD_INNER_HEIGHT = self.CARD_HEIGHT - 15
        self.FONT_SIZE = 100
        self.FONT_COLOR = (255, 255, 255) 
        self.EDGE_CONTENT_RATIO = 0.3 
        
        # Card Edge Labels
        self.DRAW_TWO_EDGE_CONTENT = '+2'
        self.DRAW_FOUR_EDGE_CONTENT = '+4'
        