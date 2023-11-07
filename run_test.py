import pygame
from settings import Settings
from card import UnoCard, CardType, CardColor, UnoCardViewBuilder, UnoCardViewDirector
from resource_manager import ResourceManager
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

        # Sets up game resources
        self.resource_manager = ResourceManager()
        for img in self.settings.ImageResources:
            self.resource_manager.add_image(img, pygame.image.load(img.value))
            
        # Sets up background
        self.bg_rect = pygame.Rect((0,0), (
            self.settings.screen_width, self.settings.screen_height))
        self.bg = pygame.Surface(self.bg_rect.size, pygame.SRCALPHA)
        self.bg.fill((0,0,50))
        
        # Card View Builder/Director
        card_builder = UnoCardViewBuilder()
        
        self.card_view_director = UnoCardViewDirector(card_builder,
                                                 self.resource_manager,
                                                 self.settings)



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
        
        self._mouse = pygame.mouse
        self._mouse_initial_grab_x = None
        self._mouse_initial_grab_y = None
        self._card_selected = False
        
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
        #print(self._mouse.get_pressed()[0])
        
        # Gets the current mouse position
        mouse_x, mouse_y = self._mouse.get_pos()
        
        # Check for collision between the mouse and sprites in the group
        if self._mouse.get_pressed()[0]:
            for card in self.card_group:
                if (card.rect.collidepoint(mouse_x, mouse_y) and 
                    self._card_selected == None):
                    self.card_group.remove(card)
                    self.card_group.add(card)
                    self._card_selected = card
                    self._mouse_initial_grab_x = mouse_x
                    self._mouse_initial_grab_y = mouse_y
                if not self._card_selected == None:
                    pos_x = self._card_selected.rect.x + mouse_x - self._mouse_initial_grab_x
                    pos_y = self._card_selected.rect.y + mouse_y - self._mouse_initial_grab_y
                    
                    self._card_selected.set_position(pos_x, pos_y)
                    self._mouse_initial_grab_x = mouse_x
                    self._mouse_initial_grab_y = mouse_y
                
        else:
            self._card_selected = None
                
                
        self.card_group.update()

    def _draw_screen(self):
        """Draws game instance current screen(state)"""
        self.screen.blit(self.bg, (0, 0))
        
        self.card_group.draw(self.screen)        
        pygame.display.flip()

    def build_card(self, card_type, card_color):
        card = UnoCard(card_type, card_color)
        return self.card_view_director.create_card_view(card)


if __name__ == "__main__":
    # Make a game instance, and run the game.
    game = Game()
    game.run_game()
