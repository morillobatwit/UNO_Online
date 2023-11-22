import pygame
from gui import Button
from states.screen import Screen
from status_code import StatusCode
from card import CardColor

class DialogScreen(Screen):
    """
    A class representing a dialog screen in a game.
    """
    
    def __init__(self, game_instance):
        """
        Initializes a new instance of the DialogScreen class.

        Args:
            game_instance (GameInstance): An instance of the game.
        """        
        super().__init__(game_instance)
        self.set_background_color((0, 0, 0, 100))
        self.resource_manager = game_instance.resource_manager
        self.settings = game_instance.settings
        self._title = self._content_surface = None
        self._buttons = []

    def set_title(self, text):
        """
        Sets the title of the dialog screen.

        Args:
            text (str): The text to be displayed as the title.
        """        
        self._title = self.resource_manager.render_font(
            text,
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            50)   
        self._title_rect = self._title.get_rect()
        self.organize_content()  
        
    def set_content(self, content_surface):
        """
        Sets the content of the dialog screen.

        Args:
            content_surface (Surface): 
                The surface containing the content to be displayed.
        """        
        self._content_surface = content_surface
        self._content_surf_rect = self._content_surface.get_rect()  
        self.organize_content()    
        
    def set_buttons(self, *args):
        """
        Sets the buttons for the dialog screen.

        Args:
            *args: Variable number of Button objects to be displayed.
        """        
        self._buttons = args
        self.organize_content()  
            
    def organize_content(self):
        """
        Organizes the layout of the dialog screen components, including title, content, and buttons.
        """        
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
        """
        Placeholder for any update logic needed for the dialog screen.
        """        
        pass

    def blit(self):
        """
        Renders and displays the dialog screen components.
        """        
        super().blit()
        if self._title:
            self.draw(self._title, rect=self._title_rect)

        if self._content_surface:            
            self.draw(self._content_surface, rect=self._content_surf_rect)
    
        for button in self._buttons:            
            button.blitme(self.surface)          
        
    def _check_events(self, event):
        """
        Checks events related to the dialog screen buttons and handles them.
    
        Args:
            event (Event): The event to be processed.
        """        
        for button in self._buttons:            
            button.handle_event(event) 
        
class ServerConnectionDialog(DialogScreen):
    """
    A specialized dialog screen for handling server connection attempts in a game.
    """
    def __init__(self, game_instance, screen, server_address, server_port):
        """
        Initializes a new instance of the ServerConnectionDialog class.

        Args:
            game_instance (GameInstance): An instance of the game.
            screen (Screen): The screen to navigate to after successful server connection.
            server_address (str): The address of the server to connect to.
            server_port (int): The port number for the server connection.
        """        
        super().__init__(game_instance)
        self.set_background_color((0, 0, 0, 230))
        self.start_screen = screen
        
        self.set_title("")
        self.update_status_msg(f"Connecting to {server_address}...")
        
        # Create "Back" button
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
        """
        Event handler for the "Back" button, 
        pops the current screen from the game's screen stack.
        """
        self.game_instance().pop_screen()

    def update(self):
        """
        Updates the connection status message based 
        on the received server response.
        """        
        if self.game_instance().client.response_received():
           r = self.game_instance().client.get_response()
           
           if r.status_code == StatusCode.CONNECTION_FAILED:
               self.update_status_msg("Connection failed, try again.")
               self._buttons[0].set_visibility(True)
           elif r.status_code == StatusCode.CONNECTION_SUCCESS:
               msg = "Connection successful. Waiting for other players to join..."
               self.update_status_msg(msg)
           elif r.status_code == StatusCode.GAME_START:
               self.start_screen.go_to_play_screen()
        
        
    def update_status_msg(self, status_msg):
        """
        Updates the content of the dialog screen with a new status message.

        Args:
            status_msg (str): The new status message to be displayed.
        """        
        new_content = self.resource_manager.render_font(
            status_msg,
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            35)
        
        self.set_content(new_content)
        
class ColorPickerDialog(DialogScreen):
    """
    A dialog for managing color picking in a game.
    """
    def __init__(self, game_instance, screen):
        """
        Initializes a new instance of the ColorPickerDialog class.

        Args:
            game_instance (GameInstance): An instance of the game.
            screen (Screen): The screen where color changes will be applied.
        """
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
        btn_red = self.create_color_button(CardColor.RED)
        btn_green = self.create_color_button(CardColor.GREEN)
        btn_blue = self.create_color_button(CardColor.BLUE)  
        btn_yellow = self.create_color_button(CardColor.YELLOW)   
        
        self.set_buttons(*[btn_red, btn_green, btn_blue, btn_yellow])


    def create_color_button(self, color_type):
        """
        Creates a color button based on the specified card color type.

        Args:
            color_type (CardColor): The color type for the button.

        Returns:
            ColorButton: The created color button.
        """        
        color_darker_ratio = 0.7
        darker_color = (
         color_type.value[0] * color_darker_ratio,
         color_type.value[1] * color_darker_ratio,
         color_type.value[2] * color_darker_ratio)
        
        btn_size = 50
        btn_text_surface = pygame.Surface((1,1))
        btn = ColorButton(
            0, 0, btn_size,
            btn_text_surface,
            color_type,
            darker_color)
        btn.set_on_click_callback(self.color_select_event)
        return btn


    def color_select_event(self, color_type):
        """
        Event handler for color selection, sets the wild color for the play screen.

        Args:
            color_type (CardColor): The selected color type.
        """        
        self.play_screen.set_wild_color_pick(color_type)
        self.game_instance().pop_screen()
  
        
class ColorButton(Button):
    """
    A specialized button class for handling color selection.
    """
    def __init__(self, x, y, size, text_surface, color_type, active_color):
        """
        Initializes a new instance of the ColorButton class.

        Args:
            x (int): The x-coordinate of the button's top-left corner.
            y (int): The y-coordinate of the button's top-left corner.
            size (int): The size of the button (both width and height).
            text_surface (Surface): The surface containing the button's text.
            color_type (CardColor): The color type associated with the button.
            active_color (tuple): The color of the button when it is active.
        """        
        super().__init__(
            x, y, size, size, text_surface, color_type.value, active_color) 
        
        self.color_type = color_type
        
    def on_click(self):
        """
        Overrides the on_click method to handle color selection events.
        """        
        self.on_click_callback(self.color_type)        
        
        
class GameEndingDialog(DialogScreen):
    """
    A dialog screen displayed at the end of the game to announce the winner.
    """
    
    def __init__(self, game_instance, client_name, winner):
        """
        Initializes a new instance of the GameEndingDialog class.

        Args:
            game_instance (GameInstance): An instance of the game.
            client_name (str): The name of the client player.
            winner (str): The name of the winning player.
        """        
        super().__init__(game_instance)
        title = ""
        if client_name == winner:
             title = "You Won"
        else:
             title = "You Lost"
            
        self.set_title(title)       
        
        content = self.resource_manager.render_font(
            f'{winner} was the winner',
            self.settings.CARD_FONT_COLOR,
            self.settings.FONT_DIR,
            35)
        
        self.set_content(content)
            
            
    
  
               
        
        

