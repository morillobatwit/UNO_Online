import pygame
from settings import Settings
from card import UnoCardView, UnoCard, CardType, CardColor
import sys

class Game:
    """Template class for PyGame."""

    def __init__(self):
        """Initializes the game's instance."""
        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        self.settings = Settings()
        self.clock = pygame.time.Clock()

        # Initializes initial screen surface
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()      

        card = UnoCardView(UnoCard(CardType.THREE, CardColor.RED))
        card.rect.center = (self.settings.screen_width / 2, self.settings.screen_height / 2)

        # Create a sprite group
        self.card_group = pygame.sprite.Group()
        self.card_group.add(card)

    def run_game(self):
        """The main game loop."""
        while 1:
            self._check_events()
            self._update_screen()
            self._draw_screen()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        #self.game_instance.check_state_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                     

    def _update_screen(self):
        """Update game instance elements"""
        #self.game_instance.update_state()

    def _draw_screen(self):
        """Draws game instance current screen(state)"""
        self.card_group.update()
        self.card_group.draw(self.screen)        
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
