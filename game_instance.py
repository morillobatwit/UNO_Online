import pygame
from states.start_screen import StartScreen
from states.play_screen import PlayScreen
from client import Client

class GameInstance:
    """Represents an instance of the game"""

    _states = []

    def __init__(self, settings, resource_manager):
        """Initializes current game instance"""

        self.settings = settings
        self.resource_manager = resource_manager
        flags = pygame.DOUBLEBUF

        # Initializes initial screen surface
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT),
            flags, 8
        )
        
        self.screen_rect = self.screen.get_rect()

        # Initializes the client
        self._client = Client()

        # Transitions the game screen to the start screen
        self.transition_to(StartScreen(self))
        # self.transition_to(PlayScreen(self))


    def transition_to(self, state):
        """
        Changes from screen to screen(state)
        """
        print(f"GameInstance: Transition to {type(state).__name__}")
        if len(self._states) > 0:
            self._states.pop()

        self._add_state(state)

    def append_screen(self, state):
        """
        Appends a new screen(state) to the game
        """
        print(f"GameInstance: Appending {type(state).__name__}")
        self._add_state(state)

    def _add_state(self, state):
        """
        adds the state to the state list
        """
        self._states.append(state)

    def pop_screen(self):
        """
        Removes last added screen(state)
        """
        if len(self._states) > 0:
            print(f"GameInstance: Popping {type(self._states[-1]).__name__}")
            return self._states.pop()
        return None

    def update_state(self):
        """
        updates current screen(state)
        """
        for state in self._states:
            state.update()

    def blit_state(self):
        """Blits current screen(state)"""
        for state in self._states:
            state.blit()

    def check_state_events(self):
        """checks current screen(state) input events"""
        return self._states[-1]._check_screen_events()

    def get_screen(self):
        """returns the current screen(state)"""
        return self.screen

    def get_screen_w(self):
        """returns the current screen(state) width"""
        return self.screen.get_width()

    def get_screen_h(self):
        """returns the current screen(state) height"""
        return self.screen.get_height()

    def get_rect(self):
        """returns the current screen(state) rectangle"""
        return self.screen_rect

    def blit(self, surface, pos):
        """Draws surface onto screen"""
        self.screen.blit(surface, pos)
        
    @property
    def client(self):
        """Returns the client"""
        return self._client      
        
        
        
