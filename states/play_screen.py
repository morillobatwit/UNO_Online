import pygame
from states.screen import Screen
from states.dialog import ColorPickerDialog
from card_collections import UnoHand
from card import CardColor, UnoCard
from card_builder_director import UnoCardViewBuilder, UnoCardViewDirector
from status_code import StatusCode

class PlayScreen(Screen):
    """Represents the play screen when the playing happens"""

    def __init__(self, game_instance):
        """Initializes play screen"""
        super().__init__(game_instance)
        self.settings = game_instance.settings
        self.resource_manager = game_instance.resource_manager
        self.client = game_instance.client
        
        # Request initial cards from server
        self.client.request_initial_cards()
        
        # Request initial discard card from server
        self.client.request_discard_card()
        
        # Sets the background color
        bg_color = self.settings.PLAY_SCREEN_BG_COLOR
        self.set_background_color(bg_color)
        
        # Loads all card images
        for img in self.settings.ImageResources:
            self.resource_manager.add_image(img, pygame.image.load(img.value))
        
        self.card_builder = UnoCardViewBuilder()
        self.card_director = UnoCardViewDirector(
            self.card_builder,
            self.resource_manager,
            self.settings)
        
        self._hand = UnoHand(
            pygame.sprite.Group(),
            self.rect.left,
            self.rect.bottom)        
        
        # Creates card view for the deck
        turned_over_card_v = self.resource_manager.render_font(
            "UNO",
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            self.settings.CARD_BACK_FONT_SIZE)
        
        edge_label = self.resource_manager.render_font(
            " ",
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            self.settings.CARD_BACK_FONT_SIZE)
        
        self._deck = self.card_director.create_custom_card_view(
            None, turned_over_card_v, edge_label)
        self._deck.rect.bottom = self.rect.centery 
        self._deck.rect.right = self.rect.centerx - 20
        
        self.color_picked = None
        self.mouse_x = self.mouse_y = 0
        self.grabbed_card = None
        self.in_turn = False
        self.discard_card = None
        self.wild_type = None
       
            
    def _check_events(self, event):
        """Respond to base keypresses and mouse events."""
        for card in self._hand.cards:
            card.handle_event(event)
            
        # if deck is touched request card from server 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._deck.rect.collidepoint(event.pos) and self.in_turn:
                self.client.request_card_draw()
                self.finish_turn()
               
        if event.type == pygame.MOUSEMOTION:
            # Update mouse position on motion
            self.mouse_x, self.mouse_y = event.pos        
                
                
    def update(self):
        """Updates Play Screen"""
        self.handle_server_responses()
        
        for card in self._hand.cards:
            if card.grabbed:
                self.grabbed_card = card

        # If the grabbed_card was dropped
        if (self.grabbed_card and not self.grabbed_card.grabbed):
            
            card_collision = pygame.sprite.collide_rect(
                self.grabbed_card, self.discard_card)
            # If card was dropped on the discard pile
            if (self.in_turn and self.discard_card and card_collision and
                self.card_matches_discard(self.grabbed_card)):
                self._hand.cards.remove(self.grabbed_card)
                self._hand.x = 0
                self._hand.organize_cards()
                
                if self.grabbed_card.uno_card.color == CardColor.DARK:
                    self.wild_type = self.grabbed_card.uno_card.type
                    c_d = ColorPickerDialog(self.game_instance(), self)
                    self.game_instance().append_screen(c_d)
                else:
                    self.client.request_card_play(self.grabbed_card.uno_card)
                    self.finish_turn()
            else:
                self.grabbed_card.reset_pos()
                
            self.grabbed_card = None
                
        
        # Manages Hand Movement
        if len(self._hand.cards) > 9 and not self.grabbed_card:
            last_card_in_hand = self._hand.cards.sprites()[-1]
            first_card_in_hand = self._hand.cards.sprites()[0]
            r_movement_trigger_x = self.rect.right - self.rect.width / 8
            l_movement_trigger_x = self.rect.left + self.rect.width / 8
            
            # Move to the right until last card completely visible
            if (self.mouse_x > r_movement_trigger_x and
                last_card_in_hand.rect.right > self.rect.right):
                self._hand.x -= 6         

            # Move to the right until last card completely visible
            if (self.mouse_x < l_movement_trigger_x and
                first_card_in_hand.rect.left < self.rect.left):
                self._hand.x += 6
                
    def reset_discard_pos(self):
        self.discard_card.rect.bottom = self.rect.centery
        self.discard_card.rect.left = self.rect.centerx + 20
        
    def blit(self):
        """Draws Plays screen"""
        super().blit()
        if self.discard_card:
            self.draw(self.discard_card.image, rect=self.discard_card.rect)
        self.draw(self._deck.image, rect=self._deck.rect)
        self._hand.blitme(self.surface)
        
        
    def handle_server_responses(self):        
        # Updates connection status message once connection response received
        if self.game_instance().client.response_received():
            u_response = self.game_instance().client.get_response()
            r_status_code = u_response.status_code
            r_dta = u_response.data
            
            if r_status_code == StatusCode.INITIAL_DRAW:
                for card in r_dta:
                    card_view = self.card_director.create_card_view(card)
                    self._hand.add_card(card_view)
                    
            if r_status_code == StatusCode.CARD_DRAW:
                for c in r_dta:
                    card_view = self.card_director.create_card_view(c)
                    self._hand.add_card(card_view)      
                
            if r_status_code == StatusCode.DISCARD_CARD:
                card_view = self.card_director.create_card_view(r_dta)
                self.discard_card = card_view
                print(self.discard_card)
                self.reset_discard_pos()
                
            if r_status_code == StatusCode.CARD_PLAY_NOTIFICATION:
                card_view = self.card_director.create_card_view(r_dta[1])
                self.discard_card = card_view
                self.reset_discard_pos()  
                
            if r_status_code == StatusCode.IN_TURN:
                self.in_turn = True                             

    def card_matches_discard(self, card):
        return (card.type == self.discard_card.type or
            card.color == self.discard_card.color or
            card.color == CardColor.DARK)
    
    def finish_turn(self):
        self.in_turn = False
            
    def set_wild_color_pick(self, color_type):
        self.client.request_card_play(UnoCard(self.wild_type, color_type))
        self.wild_type = None
        self.finish_turn()
        
        

