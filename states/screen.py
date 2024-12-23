from states.state import State
from abc import abstractmethod
import pygame
import sys

class Screen(State):
    """Represents a screen that will serve as a game's state"""

    def __init__(self, game_instance):
        """
        Initializes a new instance of the Screen class.

        Args:
            game_instance (Game): An instance of the game.
        """
        self.set_game_instance(game_instance)
        
        # Sets initial color for every screen to black
        self.set_background_color((0,0,0,0))

    def set_game_instance(self, game_instance):
        """
        Sets the game instance as context for the screen.

        Args:
            game_instance (GameInstance): An instance of the game.
        """
        self._surface = game_instance.get_screen()
        self._rect = self._surface.get_rect()
        self._screen_w = game_instance.get_screen_w()
        self._screen_h = game_instance.get_screen_h()
        
        self._bg_surface = pygame.Surface((self._screen_w, self._screen_h))
        self._bg_surface = self._bg_surface.convert_alpha()
        self.set_context(game_instance)

    def game_instance(self):
        """
        Returns the game instance associated with the screen.

        Returns:
            GameInstance: The game instance.
        """
        return self.get_context()

    def set_background_color(self, rgba):
        """
        Updates the screen's initial background color.

        Args:
            rgba (tuple): The RGBA values for the background color.
        """
        self._bg_surface.fill(rgba)

    def get_background_surface(self):
        """
        Returns the screen's initial background surface.

        Returns:
            pygame.Surface: The background surface.
        """
        return self._bg_surface

    def is_paused(self):
        """
        Checks if the screen is paused by noting if 
        it is the lastly added screen in the game.

        Returns:
            bool: True if the screen is paused, False otherwise.
        """
        return self.game_instance()._states[-1] != self
    
    def get_width(self):
        """
        Returns the width of the screen.

        Returns:
            int: The width of the screen.
        """
        return self._screen_w   
    
    def get_height(self):
        """
        Returns the height of the screen.

        Returns:
            int: The height of the screen.
        """
        return self._screen_h      

    def draw(self, surface, x=0, y=0, rect=None):
        """
        Draws on the game_instance screen.

        Args:
            surface: The surface to draw.
            x (int): The x-coordinate to draw on.
            y (int): The y-coordinate to draw on.
            rect (pygame.Rect): The rectangle to draw.
        """
        if not rect:
            self.game_instance().blit(surface, (x, y))
        else:
            self.game_instance().blit(surface, rect)

    def blit(self):
        """
        Draws the initial background surface.
        """
        self.draw(self._bg_surface, 0, 0)

    def _check_screen_events(self):
        """
        Checks events for the screen, including handling quit events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_instance().client.close_connection()
                sys.exit()
                
            self._check_events(event)
            
    @abstractmethod
    def update(self):
        """Updates screen"""
        pass
            
    @abstractmethod
    def _check_events(self, event):
        """Handles subclasses events"""
        pass   

    @property
    def surface(self):
        """Returns screen surface"""
        return self._surface
    
    @property
    def rect(self):
        """Returns screen rectangle"""
        return self._rect         
