from views import UnoCardView
from card import UnoCard, CardColor, CardType
import pygame

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
                uno_card, self._image_resources.WILD, ' ')
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
            Uno card to create the view of.
        center_img_dir : string
            directory path of center image.
        edge_label : string, optional
            label that will substitute edge content. The default is None.

        Returns
        -------
        UnoCardView
            View of created UNO action card.

        """
        center_content = self._resource_manager.get_image(center_img_dir)
        
        # resizes center content surface
        c_content_ratio = self._settings.CENTER_CONTENT_RATIO
        c_content_w = pygame.Surface.get_width(center_content) * c_content_ratio
        c_content_h = pygame.Surface.get_height(center_content) * c_content_ratio
        
        center_content = pygame.transform.scale(center_content,
                                      (c_content_w,
                                       c_content_h))  
        
        if edge_label:
            font = self._resource_manager.load_font(
                self._settings.FONT_DIR,
                self._settings.CARD_CENTER_FONT_SIZE)     

            edge_label = font.render(
                edge_label, True, self._settings.CARD_FONT_COLOR) 
        
        return self._build_view(uno_card, center_content, edge_label)
    
    def create_custom_card_view(self, uno_card, center_content, edge_label=None):
        return self._build_view(
            UnoCard(CardType.NONE, CardColor.DARK),
            center_content,
            edge_label)
        
