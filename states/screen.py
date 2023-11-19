from states.state import State
from abc import abstractmethod
import pygame
import sys

class Screen(State):
    """Represents a screen that will serve as a game's state"""

    def __init__(self, game_instance):
        """Initiallizes screen"""
        self.set_game_instance(game_instance)
        
        # Sets initial color for every screen to black
        self.set_background_color((0,0,0,0))

    def set_game_instance(self, game_instance):
        """Sets game instance as context"""
        self._surface = game_instance.get_screen()
        self._rect = self._surface.get_rect()
        self._screen_w = game_instance.get_screen_w()
        self._screen_h = game_instance.get_screen_h()
        
        self._bg_surface = pygame.Surface((self._screen_w, self._screen_h))
        self._bg_surface = self._bg_surface.convert_alpha()
        self.set_context(game_instance)

    def game_instance(self):
        """Returns game instance"""
        return self.get_context()

    def set_background_color(self, rgba):
        """Updates screen's initial background color"""
        self._bg_surface.fill(rgba)

    def get_background_surface(self):
        """Returns screen's initial background surface"""
        return self._bg_surface

    def is_paused(self):
        """
        Checks if the screen is paused by noting
        if it is the lastly added screen in the game
        """
        return self.game_instance()._states[-1] != self
    
    def get_width(self):
        """Returns this screens width"""
        return self._screen_w   
    
    def get_height(self):
        """Returns this screens height"""
        return self._screen_h      

    def draw(self, surface, x=0, y=0, rect=None):
        """Draws on the game instance"""
        if not rect:
            self.game_instance().blit(surface, (x, y))
        else:
            self.game_instance().blit(surface, rect)

    def blit(self):
        """Draws initial background surface"""
        self.draw(self._bg_surface, 0, 0)

    def _check_screen_events(self):
        """checks events for the screen"""
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
