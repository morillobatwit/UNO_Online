import pygame

class TextField:
    def __init__(self, x, y, width, height, font, max_characters):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self._text = ""
        self.active = False
        self._text_surface = None
        self._max_characters = max_characters
        self._color = (255, 255, 255)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self._color = (0, 255, 0)
            else:
                self.active = False
                self._color = (255, 255, 255)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self._remove_text()
            elif len(self._text) < self._max_characters:
                self._add_text(event.unicode)  
        
    def blitme(self, surface):
        # Draw the text field
        pygame.draw.rect(surface, self._color, self.rect,2)
        
        # Blit the text
        if not self._text_surface == None:
            #self.rect.w = max(100, self._text_surface.get_width()+10)
            surface.blit(self._text_surface, (self.rect.x + 5, self.rect.y + 5))
        
    def _add_text(self, text):
        self._text += text
        self._render_surface()
        
    def _remove_text(self):
        self._text = self._text[:-1]
        self._render_surface()
        
    def _render_surface(self):
        self._text_surface = self.font.render(self._text, True, (255, 255, 255))   
        
    def reset(self):
        self._text = ""
        self._render_surface()      
        
    @property
    def text(self):
        return self._text
    
class IpTextField(TextField):
    def _add_text(self, text):
        if text >= '0' and text <= '9':
            
            text_to_check = self._text + text
            ip_parts = text_to_check.split('.')
            last_ip_part = ip_parts[-1]

            if (len(ip_parts) >= 4 and 
                (int(last_ip_part) > 255 or 
                 (last_ip_part[0] == '0' and len(last_ip_part) > 1))):
                return 
            
            if (int(last_ip_part) > 255 or
                len(last_ip_part) > 3 or 
                (last_ip_part[0] == '0' and len(last_ip_part) > 1)):
                text = '.' + text
                
                
        elif text == '.':
            # Dont allow consecutive dots
            if self._text[-1:] == '.' and text == '.':
                return
            elif self._text.count('.') >= 3:
                return
        else:
            return
            
        super()._add_text(text)
    
        
class Button:
    def __init__(self, x, y, width, height, text_surface, inactive_color, active_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.color = inactive_color
        self.clicked = False
        self.text_surface = text_surface
        self.text_surface_rect = text_surface.get_rect(center=self.rect.center)
        self.on_click_callback = None
        self._visible = True
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.active_color
            else:
                self.color = self.inactive_color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1 and 
                self.rect.collidepoint(event.pos) and 
                self.clicked):
                self.on_click()
                self.clicked = False
                
    def on_click(self):
        self.on_click_callback()
                
    def set_on_click_callback(self, callback):
        self.on_click_callback = callback
                
    def blitme(self, surface):
        if self.text_surface_rect.center != self.rect.center:
            self.text_surface_rect.center = self.rect.center
        
        if self._visible:
            pygame.draw.rect(surface, self.color, self.rect)
            surface.blit(self.text_surface, self.text_surface_rect) 
        
    def set_visibility(self, status):
        self._visible = status       
