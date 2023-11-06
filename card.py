from enum import Enum
import pygame 
from pygame.math import Vector2

class CardType(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    REVERSE = 10
    SKIP = 11
    DRAW_TWO = 12
    WILD = 13
    WILD_DRAW_FOUR = 14

class CardColor(Enum):
    RED = (230, 71, 52)#(200, 0, 0)
    GREEN = (97, 176, 57)#(0, 200, 0)
    BLUE = (50, 105, 169)#(0, 0, 200)
    YELLOW = (242, 199, 69)#(200, 200, 0)
    DARK = (50, 50, 50)

class UnoCard:
    def __init__(self, card_type, card_color):
        """
        Represents an UNO card

        Parameters
        ----------
        card_type : CardType
            a CardType element(Example: CardType.ONE).
        card_color : CardColor
            a CardColor element(Example: CardType.RED).

        """
        self._type = card_type
        self._color = card_color

    @property
    def type(self):
        return self._type

    @property
    def color(self):
        return self._color    

class UnoCardView(pygame.sprite.Sprite):

    def __init__(self, uno_card, width, height, inner_width, inner_height,
                 center_content, edge_content=None): 
        super().__init__()
        self._uno_card = uno_card
        self._position = Vector2(0, 0)
        self._card_color = self._uno_card.color.value
       
        
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

    
class UnoCardViewBuilder:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._uno_card = \
        self._center_content = \
        self._edge_content = \
        self._width = \
        self._height = \
        self._i_width = \
        self._i_height = None
        
    def set_uno_card(self, uno_card):
        self._uno_card = uno_card
        
    def set_center_content(self, center_content):
        self._center_content = center_content

    def set_edge_content(self, edge_content):
        self._edge_content = edge_content  
        
    def set_view_width(self, width):
        self._width = width     
        
    def set_view_height(self, height):
        self._height = height   
        
    def set_inner_view_width(self, width):
        self._i_width = width     
        
    def set_inner_view_height(self, height):
        self._i_height = height         
        
        
    def build_view(self):
        uno_card_view = UnoCardView(self._uno_card,
                                      self._width,
                                      self._height,
                                      self._i_width,
                                      self._i_height,
                                      self._center_content,
                                      self._edge_content)
        
        self.reset()
        return uno_card_view
    
class UnoCardViewDirector:
    """
    In charge of constructing the predefined(SKIP, REVERSE...) UNO view cards
    """
    
    def __init__(self, builder, resource_manager, settings):
        self._builder = builder
        self._resource_manager = resource_manager
        self._settings = settings
        self._image_resources = self._settings.ImageResources
        
    def create_card_view(self, uno_card):  
        """
        Creates a view for any UNO card

        Parameters
        ----------
        uno_card : UnoCard
            UnoCard to create the view of..

        Returns
        -------
        UnoCardView
            created view.

        """
        
        # SKIP 
        if uno_card.type == CardType.SKIP:
            return self._create_action_card_view(
                uno_card, self._image_resources.SKIP)
        # REVERSE 
        elif uno_card.type == CardType.REVERSE:
            return self._create_action_card_view(
                uno_card, self._image_resources.REVERSE)
        # DRAW TWO
        elif uno_card.type == CardType.DRAW_TWO:
            return self._create_action_card_view(
                uno_card,
                self._image_resources.DRAW_TWO,
                self._settings.DRAW_TWO_EDGE_CONTENT)
        # WILD DRAW FOUR
        elif uno_card.type == CardType.WILD_DRAW_FOUR:
            return self._create_action_card_view(
                uno_card,
                self._image_resources.WILD,
                self._settings.DRAW_FOUR_EDGE_CONTENT)
        # WILD
        elif uno_card.type == CardType.WILD:
            return self._create_action_card_view(
                uno_card, self._image_resources.WILD)
        # NUMBER
        else:
            return self._create_number_card_view(uno_card)        

    def _build_view(self, uno_card, center_content, edge_content=None):
        """
        Builds the view for a UNO card

        Parameters
        ----------
        uno_card : UnoCard
            object which holds type and color of card.
        center_content : Surface
            surface to be displayed on the center of the card.
        edge_content : Surface, optional
            surface to be displayed on the top-left and bottom right
            of the card. The default is None.

        Returns
        -------
        UnoCardView
            View of uno card.

        """
        # Creates the the necesarry edge content for the card if needed
        if not edge_content:
            edge_content = center_content.copy()

        # resizes edge content surface
        edge_content_ratio = self._settings.EDGE_CONTENT_RATIO
        edge_content_w = pygame.Surface.get_width(edge_content) * edge_content_ratio
        edge_content_h = pygame.Surface.get_height(edge_content) * edge_content_ratio
        
        edge_content = pygame.transform.scale(edge_content,
                                      (edge_content_w,
                                       edge_content_h))   
        
        # Uses builder to build the uno view card
        self._builder.set_uno_card(uno_card)
        self._builder.set_center_content(center_content)
        self._builder.set_edge_content(edge_content)
        self._builder.set_view_width(self._settings.CARD_WIDTH)
        self._builder.set_view_height(self._settings.CARD_HEIGHT)
        self._builder.set_inner_view_width(self._settings.CARD_INNER_WIDTH)
        self._builder.set_inner_view_height(self._settings.CARD_INNER_HEIGHT)
        
        return self._builder.build_view()        

    def _create_number_card_view(self, uno_card):
        """
        Creates a view for a UNO Number card

        Parameters
        ----------
        uno_card : UnoCard
            UnoCard to create the view of.

        Returns
        -------
        UnoCardView
            View of card.

        """
        font = self._resource_manager.load_font(
            self._settings.FONT_DIR,
            self._settings.CARD_CENTER_FONT_SIZE)

        center_content = font.render(
            str(uno_card.type.value),
            True,
            self._settings.CARD_FONT_COLOR)
        
        return self._build_view(uno_card, center_content)
    
    
    def _create_action_card_view(self, uno_card, center_img_dir, edge_label=None):
        """
        Creates a view for a UNO Action card

        Parameters
        ----------
        uno_card : UnoCard
            UnoCard to create the view of.

        Returns
        -------
        UnoCardView
            View of card.

        """
        center_content = self._resource_manager.get_image(center_img_dir)
        
        if edge_label:
            font = self._resource_manager.load_font(
                self._settings.FONT_DIR,
                self._settings.CARD_CENTER_FONT_SIZE)     

            edge_label = font.render(
                edge_label, True, self._settings.CARD_FONT_COLOR) 
        
        return self._build_view(uno_card, center_content, edge_label)
        