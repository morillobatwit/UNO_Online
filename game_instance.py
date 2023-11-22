import pygame
from states.start_screen import StartScreen
from client import Client

class GameInstance:
    """Represents an instance of the game"""

    _states = []

    def __init__(self, settings, resource_manager):
        """
        Initializes the current game instance.

        Args:
            settings (Settings): The settings instance for configuring the game.
            resource_manager (ResourceManager): The resource manager for 
                handling game assets.
        """

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

    def transition_to(self, state):
        """
        Changes from one screen to another (state).

        Args:
            state: The new screen (state) to transition to.
        """
        print(f"GameInstance: Transition to {type(state).__name__}")
        if len(self._states) > 0:
            self._states.pop()

        self._add_state(state)

    def append_screen(self, state):
        """
        Appends a new screen (state) to the game.

        Args:
            state: The new screen (state) to append.
        """
        print(f"GameInstance: Appending {type(state).__name__}")
        self._add_state(state)

    def _add_state(self, state):
        """
        Adds the state to the state list.

        Args:
            state: The screen (state) to add to the list.
        """
        self._states.append(state)

    def pop_screen(self):
        """
        Removes the last added screen (state).

        Returns:
            state: The removed screen (state).
        """
        if len(self._states) > 0:
            print(f"GameInstance: Popping {type(self._states[-1]).__name__}")
            return self._states.pop()
        return None

    def update_state(self):
        """
        Updates the current screen (state).
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
        """
        Returns the current screen (state).

        Returns:
            pygame.Surface: The current game screen.
        """
        return self.screen

    def get_screen_w(self):
        """
        Returns the width of the current screen (state).

        Returns:
            int: The width of the current game screen.
        """
        return self.screen.get_width()

    def get_screen_h(self):
        """
        Returns the height of the current screen (state).

        Returns:
            int: The height of the current game screen.
        """
        return self.screen.get_height()

    def get_rect(self):
        """
        Returns the rectangle of the current screen (state).

        Returns:
            pygame.Rect: The rectangle of the current game screen.
        """
        return self.screen_rect

    def blit(self, surface, pos):
        """
        Draws a surface onto the game screen.

        Args:
            surface (pygame.Surface): The surface to draw.
            pos (tuple): The position to draw the surface.
        """
        self.screen.blit(surface, pos)
        
    @property
    def client(self):
        """
        Returns the client instance.

        Returns:
            Client: The client instance for communication with the server.
        """
        return self._client      
        
        
        
