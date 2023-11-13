import pygame
from game_instance import GameInstance
from settings import Settings
from resource_manager import ResourceManager


class Game:
    """Template class for PyGame."""

    def __init__(self):
        """Initializes the game's instance."""
        pygame.init()
        self._settings = Settings()
        self._resource_manager = ResourceManager()
        
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
        pygame.display.set_caption(self._settings.TITLE)
        
        
        self.game_instance = GameInstance(self._settings, self._resource_manager)
        self.clock = pygame.time.Clock()

    def run_game(self):
        """The main game loop."""
        while 1:
            self._check_events()
            self._update_screen()
            self._draw_screen()

            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        self.game_instance.check_state_events()

    def _update_screen(self):
        """Update game instance elements"""
        self.game_instance.update_state()

    def _draw_screen(self):
        """Draws game instance current screen(state)"""
        self.game_instance.blit_state()
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
