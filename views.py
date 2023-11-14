import pygame
from pygame.math import Vector2

class UnoCardView(pygame.sprite.Sprite):

    def __init__(self, uno_card, width, height, inner_width, inner_height,
                 center_content, edge_content=None): 
        super().__init__()
        self._uno_card = uno_card
        self._position = Vector2(0, 0)
        self._card_color = self._uno_card.color.value
        self._grabbed = False
        self._initial_pos = Vector2(0, 0)
        
        # CARD OUTER RECTANGLE
        self.rect = pygame.Rect(self._position, (width,
                                                 height))
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        # CARD INNER RECTANGLE
        self._inner_rect_size = (inner_width,
                                inner_height)
        self._inner_rect = pygame.Rect(self._position, self._inner_rect_size)
        self._inner_rect.center = (self.rect.width / 2, self.rect.height /2)
        
        # Sets the center content of the card
        self._center_content = center_content
        self._center_content_rect = center_content.get_rect(center=self._inner_rect.center)
        
        # Edge content
        self._edge_content = edge_content if edge_content else center_content
        
        # Sets the top left content of the card
        self.tl_content = self._edge_content
        self.tl_content.set_alpha(127)
        self.tl_content_rect = self.tl_content.get_rect(topleft=self._inner_rect.topleft)
        
        # Sets the bottom right content of the card
        self.br_content = self._edge_content
        self.br_content.set_alpha(127)
        self.br_content_rect = self.br_content.get_rect(bottomright=self._inner_rect.bottomright)

        self.draw_card()
        
    def draw_card(self):
        pygame.draw.rect(self.image, self._card_color, self.rect, border_radius=15)
        self.image.blit(self._center_content, self._center_content_rect)
        self.image.blit(self.tl_content, self.tl_content_rect)
        self.image.blit(self.br_content, self.br_content_rect) 
    
    @property
    def uno_card(self):
        return self._uno_card     
    
    @uno_card.setter
    def uno_card(self, uno_card):
        self._uno_card = uno_card
    
    @property
    def center_content(self):
        return self._center_content      
    
    @property
    def edge_content(self):
        return self._edge_content  

    @property
    def color(self):
        return self._uno_card.color

    @property
    def type(self):
        return self._uno_card.type   
    
    @property
    def position(self):
        return self._position  
    
    @property
    def grabbed(self):
        return self._grabbed      

    def set_initial_pos(self, x, y):
         self._initial_pos.x = x
         self._initial_pos.y = y
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.rect.collidepoint(event.pos) and 
                self._grabbed == False):
                self._grabbed = True
                self._initial_grab_x = event.pos[0]
                self._initial_grab_y = event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            self._grabbed = False    
            
        if self._grabbed and event.type == pygame.MOUSEMOTION:
            pos_x = self.rect.x + event.pos[0] - self._initial_grab_x
            pos_y = self.rect.y + event.pos[1] - self._initial_grab_y
            self.rect.x = pos_x
            self.rect.y = pos_y
            
            self._initial_grab_x = event.pos[0]
            self._initial_grab_y = event.pos[1]
            
    def reset_pos(self):
            self.rect.x = self._initial_pos.x
            self.rect.y = self._initial_pos.y