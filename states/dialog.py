import pygame
from gui import Button
from states.screen import Screen
from states.play_screen import PlayScreen
from status_code import StatusCode
from card import CardColor

class DialogScreen(Screen):
    """Screen in charge of displaying a dialog"""

    def __init__(self, game_instance):
        """Initializes three available perks"""
        super().__init__(game_instance)
        self.set_background_color((0, 0, 0, 100))
        self.resource_manager = game_instance.resource_manager
        self.settings = game_instance.settings
        self._title = self._content_surface = self._buttons = None

    def set_title(self, text):
        self._title = self.resource_manager.render_font(
            text,
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            50)   
        self._title_rect = self._title.get_rect()
        self.organize_content()  
        
    def set_content(self, content_surface):
        self._content_surface = content_surface
        self._content_surf_rect = self._content_surface.get_rect()  
        self.organize_content()    
        
    def set_buttons(self, *args):
        self._buttons = args
        self.organize_content()  
            
    def organize_content(self):
        if self._title:
            self._title_rect.centerx = self.rect.centerx
            self._title_rect.y = self.get_height() / 4
            
        if self._content_surface:
            self._content_surf_rect.midtop = self._title_rect.midbottom
            self._content_surf_rect.top += 5 # adds margin from title
            
        if self._buttons:
            margin = 10
            offset_x = self._content_surf_rect.centerx 
            offset_x -= self._buttons[0].rect.width * (len(self._buttons) / 2)
            offset_x -= margin * (len(self._buttons) / 2)
            for button in self._buttons:
                button.rect.top = self._content_surf_rect.bottom + 20
                button.rect.left = offset_x
                offset_x = button.rect.right + margin
            
    def update(self):
        pass

    def blit(self):
        super().blit()
        if self._title:
            self.draw(self._title, rect=self._title_rect)

        if self._content_surface:            
            self.draw(self._content_surface, rect=self._content_surf_rect)
    
        for button in self._buttons:            
            button.blitme(self.surface)          
            
        #self.textfield_ip.blitme(self.surface)
        #self.btn_join.blitme(self.surface)
        
    def _check_events(self, event):
        """Respond to base keypresses and mouse events."""
        for button in self._buttons:            
            button.handle_event(event) 
        
class ServerConnectionDialog(DialogScreen):
    """Dialog for client to server connection"""

    def __init__(self, game_instance, server_address, server_port):
        """Dialog which manages connection to server"""
        super().__init__(game_instance)
        self.set_background_color((0, 0, 0, 230))
        
        self.set_title("")
        self.update_status_msg(f"Connecting to {server_address}...")
        
        btn_back_x = 0
        btn_back_y = 0
        btn_back_w = 100
        btn_back_h = 50
        btn_back_text_surface = self.resource_manager.render_font(
            "Back",
            game_instance.settings.JOIN_BTN_TEXT_COLOR,
            game_instance.settings.FONT_DIR,
            35)
        btn_back = Button(
            btn_back_x, btn_back_y, btn_back_w, btn_back_h,
            btn_back_text_surface, game_instance.settings.JOIN_BTN_INACTIVE_COLOR,
            game_instance.settings.JOIN_BTN_ACTIVE_COLOR)
        btn_back.set_on_click_callback(self.back_event)
        btn_back.set_visibility(False)
        
        self.set_buttons(btn_back)
        
        # Attempt connection to server
        game_instance.client.connect_to_server(server_address, server_port)
        
    def back_event(self):
       self.game_instance().pop_screen()
     
    def update(self):
       # Updates connection status message once connection response received
       if self.game_instance().client.response_received():
           r = self.game_instance().client.get_response()
           
           if r.status_code == StatusCode.CONNECTION_FAILED:
               self.update_status_msg("Connection failed, try again.")
               self._buttons[0].set_visibility(True)
           elif r.status_code == StatusCode.CONNECTION_SUCCESS:
               msg = "Connection successful. Waiting for other players to join..."
               self.update_status_msg(msg)
           elif r.status_code == StatusCode.GAME_START:
               self.go_to_play_screen()
        
        
    def update_status_msg(self, status_msg):
        new_content = self.resource_manager.render_font(
            status_msg,
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            35)
        
        self.set_content(new_content)
        
    def go_to_play_screen(self):
        ps = PlayScreen(self.game_instance())
        # Close Dialog
        self.game_instance().pop_screen()
        # Transition to Play Screen
        self.game_instance().transition_to(ps)          
        
class ColorPickerDialog(DialogScreen):
    
    def __init__(self, game_instance, screen):
        """Dialog which manages color picking"""
        super().__init__(game_instance)
        
        self.play_screen = screen
        self.set_background_color((0, 0, 0, 230))
        self.set_title("Color Picker")
        
        new_content = self.resource_manager.render_font(
            'Choose the color to change the card to',
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            35)

        self.set_content(new_content)

        
        # Creates buttons
        btn_red = self.create_color_button(CardColor.RED.value)
        btn_green = self.create_color_button(CardColor.GREEN.value)
        btn_blue = self.create_color_button(CardColor.BLUE.value)  
        btn_yellow = self.create_color_button(CardColor.YELLOW.value)   
        
        self.set_buttons(*[btn_red, btn_green, btn_blue, btn_yellow])


    def create_color_button(self, color):
        color_darker_ratio = 0.7
        darker_color = (
         color[0] * color_darker_ratio,
         color[1] * color_darker_ratio,
         color[2] * color_darker_ratio)
        
        btn_size = 50
        btn_text_surface = pygame.Surface((1,1))
        btn = ColorButton(
            0, 0, btn_size,
            btn_text_surface,
            color,
            darker_color)
        btn.set_on_click_callback(self.color_select_event)
        return btn


    def color_select_event(self, color):
        self.play_screen.color_picked = color
        self.game_instance().pop_screen()
  
        
class ColorButton(Button):
    def __init__(self, x, y, size, text_surface, inactive_color, active_color):
        super().__init__(
            x, y, size, size, text_surface, inactive_color, active_color) 
        
        self.selection_color = inactive_color
        
    def on_click(self):
        self.on_click_callback(self.selection_color)        
  
               
        
        

