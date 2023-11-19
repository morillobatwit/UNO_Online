from enum import Enum

class Settings:
    """A class to store all settings for a UNO game"""
    
    class ImageResources(Enum):
        SKIP = 'resources/skip.png'
        REVERSE = 'resources/reverse.png'
        DRAW_TWO = 'resources/draw_two.png'
        DRAW_FOUR = 'resources/draw_four.png'
        WILD = 'resources/draw_four.png'

    def __init__(self):
        """Initialize the game's settings."""
        
        self.SERVER_PORT = 1234
        
        # Screen settings
        self.TITLE = 'UNO Online'
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 750
        self.BG_COLOR = (0, 16, 62, 255)
        
        # Start Screen
        self.START_SCREEN_BG_COLOR = (0, 0, 51, 255)
        self.JOIN_BTN_INACTIVE_COLOR = (0, 204, 0, 255)
        self.JOIN_BTN_ACTIVE_COLOR = (0, 153, 0, 255)
        self.JOIN_BTN_TEXT_COLOR = (255, 255, 255, 255)
        self.IP_TF_FONT_SIZE = 35
        self.IP_TF_WIDTH = self.IP_TF_FONT_SIZE * 8 # 8 seemed like a correct multiplier
        self.IP_TF_HEIGHT = 50
        self.IP_TF_MAX_CHARACTERS = 15
        
        
        # Start Screen
        self.PLAY_SCREEN_BG_COLOR = (25, 0, 51, 255)
        
        # Font settings
        self.FONT_DIR = 'resources/arial.ttf'
        self.CARD_CENTER_FONT_SIZE = 70
        self.CARD_BACK_FONT_SIZE = 35
        #self.CARD_EDGE_FONT_SIZE = self.CARD_CENTER_FONT_SIZE - 10
        self.CARD_FONT_COLOR = (255, 255, 255) 

        # Card settings   
        self.CARD_WIDTH = 120
        self.CARD_HEIGHT = self.CARD_WIDTH * 1.5
        self.CARD_INNER_WIDTH = self.CARD_WIDTH - 10
        self.CARD_INNER_HEIGHT = self.CARD_HEIGHT - 15
        #self.FONT_SIZE = 100
        self.FONT_COLOR = (255, 255, 255) 
        self.EDGE_CONTENT_RATIO = 0.4 
        self.CENTER_CONTENT_RATIO = 0.67
        
        # Card Edge Labels
        self.DRAW_TWO_EDGE_CONTENT = '+2'
        self.DRAW_FOUR_EDGE_CONTENT = '+4'
        
        # Player Name List
        self.PLAYER_LIST_FONT_SIZE = 30
        self.PLAYER_LIST_FONT_COLOR = (255, 255, 255)
        self.PLAYER_LIST_IN_TURN_COLOR = (0, 255, 0)
        