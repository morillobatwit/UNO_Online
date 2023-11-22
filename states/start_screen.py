from states.screen import Screen
from states.play_screen import PlayScreen
import pygame
from gui import IpTextField, Button
from states.dialog import ServerConnectionDialog

class StartScreen(Screen):
    """
    Represents the starting screen of the UNO Online game.
    """    
    def __init__(self, game_instance):
        """
        Initializes a new instance of the StartScreen class.

        Args:
            game_instance (GameInstance): An instance of the game.
        """        
        super().__init__(game_instance)
        
        # Sets the background color
        bg_color = game_instance.settings.START_SCREEN_BG_COLOR
        self.set_background_color(bg_color)
        
        # Adds UNO Online Title to screen
        resource_manager = game_instance.resource_manager
        self.main_title = resource_manager.render_font(
            "UNO Online",
            game_instance.settings.CARD_FONT_COLOR,
            game_instance.settings.FONT_DIR,
            game_instance.settings.CARD_CENTER_FONT_SIZE)

        self.main_title_rect = self.main_title.get_rect()
        self.main_title_rect.centerx = self.rect.centerx
        self.main_title_rect.y = self.get_height() / 4
        
        # Add Form
        self.form = pygame.Surface(
            (self.get_width() / 3,
             self.get_height() / 3))
        self.form_rect = self.form.get_rect()
        self.form_rect.centerx = self.rect.centerx
        self.form_rect.centery = self.rect.centery + self.get_height() / 10
        
        # Adds IP text field to screen
        ip_textfield_x = self.main_title_rect.left
        ip_textfield_y = self.main_title_rect.bottom
        ip_textfield_w = game_instance.settings.IP_TF_WIDTH
        ip_textfield_h = game_instance.settings.IP_TF_HEIGHT
        ip_textfield_font = resource_manager.load_font(
            game_instance.settings.FONT_DIR,
            game_instance.settings.IP_TF_FONT_SIZE)
        max_c = game_instance.settings.IP_TF_MAX_CHARACTERS
        self.textfield_ip = IpTextField(
            ip_textfield_x, ip_textfield_y,
            ip_textfield_w, ip_textfield_h,
            ip_textfield_font, max_c)
        self.textfield_ip.rect.topleft = self.form_rect.topleft

        self.inputted_ip = ""
        
        # Adds join button to screen
        join_btn_x = self.textfield_ip.rect.right + 5
        join_btn_y = self.textfield_ip.rect.top
        join_btn_w = 100
        join_btn_h = 50
        join_btn_text_surface = resource_manager.render_font(
            "Join",
            game_instance.settings.JOIN_BTN_TEXT_COLOR,
            game_instance.settings.FONT_DIR,
            35)
        self.btn_join = Button(
            join_btn_x, join_btn_y, join_btn_w, join_btn_h,
            join_btn_text_surface, game_instance.settings.JOIN_BTN_INACTIVE_COLOR,
            game_instance.settings.JOIN_BTN_ACTIVE_COLOR)
        self.btn_join.set_on_click_callback(self.join_event)
        
        
    def update(self):
        """
        Placeholder method for updating the screen.

        """        
        pass

    def blit(self):
        """
        Draws the components of the start screen.
        """        
        super().blit()
        self.draw(self.main_title, rect=self.main_title_rect)
        self.textfield_ip.blitme(self.surface)
        self.btn_join.blitme(self.surface)

        
    def _check_events(self, event):
        """
        Responds to base keypresses and mouse events.

        Args:
            event: The event to handle.
        """
        self.textfield_ip.handle_event(event)
        self.btn_join.handle_event(event)   
        
        
    def join_event(self):
        """
        Handles the join event, 
        creating a ServerConnectionDialog and transitioning to it.
        """        
        server_address = self.textfield_ip.text
        self.textfield_ip.reset()
        
        cd = ServerConnectionDialog(self.game_instance(), self,
                              server_address,
                              self.game_instance().settings.SERVER_PORT)
        self.game_instance().append_screen(cd)   
        
    def go_to_play_screen(self):
        """
        Transitions to the PlayScreen after initializing it.
        """        
        ps = PlayScreen(self.game_instance())
        # Close Dialog
        self.game_instance().pop_screen()
        # Transition to Play Screen
        self.game_instance().transition_to(ps)          

        