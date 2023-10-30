import pygame
from settings import Settings
from card import UnoCardView, UnoCardViewData, UnoCard, CardType, CardColor
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

        number_card = self.build_card(CardType.NINE, CardColor.GREEN)
        number_card.rect.topleft = (0, 0)  
        
        skip_card = self.build_card(CardType.SKIP, CardColor.BLUE)
        skip_card.rect.midtop = (self.settings.screen_width / 2, 0)  

        draw2_card = self.build_card(CardType.DRAW_TWO, CardColor.RED)
        draw2_card.rect.topright = (self.settings.screen_width, 0)  

        reverse_card = self.build_card(CardType.REVERSE, CardColor.YELLOW)
        reverse_card.rect.bottomleft = (0, self.settings.screen_height)  

        wild_card = self.build_card(CardType.WILD, CardColor.DARK)
        wild_card.rect.midbottom = (self.settings.screen_width / 2, self.settings.screen_height)  

        wild4_card = self.build_card(CardType.WILD_DRAW_FOUR, CardColor.DARK)
        wild4_card.rect.bottomright = (self.settings.screen_width, self.settings.screen_height)  

        # Create a sprite group
        self.card_group = pygame.sprite.Group()
        self.card_group.add(number_card)
        self.card_group.add(skip_card)
        self.card_group.add(draw2_card)
        self.card_group.add(reverse_card)
        self.card_group.add(wild_card)
        self.card_group.add(wild4_card)

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

    def build_card(self, card_type, card_color):
        card = UnoCard(card_type, card_color)
        card_view_dta = UnoCardViewData(card)
        card_view = UnoCardView(card_view_dta)

        return card_view


if __name__ == "__main__":
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
