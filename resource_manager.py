import pygame
class ResourceManager:
    """
    Manages game resources such as images and fonts.
    """    
    
    def __init__(self):
        """
        Initializes the ResourceManager instance.
        """        
        self.images = {}
        self.font_cache = {}
        
    def add_image(self, image_name, image):
        """
        Adds an image to the resource manager.

        Args:
            image_name (str): The name to associate with the image.
            image (pygame.Surface): The image to be added.
        """        
        self.images[image_name] = image
        
    def load_font(self, font_path, size):
        """
        Loads a font and caches it for reuse.

        Args:
            font_path (str): The path to the font file.
            size (int): The size of the font.

        Returns:
            pygame.font.Font: The loaded font.
        """        
        # Check if the font is already in the cache
        key = (font_path, size)
        if key in self.font_cache:
            return self.font_cache[key]

        # If not in cache, load the font and add it to the cache
        font = pygame.font.Font(font_path, size)
        self.font_cache[key] = font
        return font    
    
    def render_font(self, text, color, font_path, size):
        """
        Renders text with a specified font and color.

        Args:
            text (str): The text to be rendered.
            color (tuple): The color of the text in RGB format.
            font_path (str): The path to the font file.
            size (int): The size of the font.

        Returns:
            pygame.Surface: The rendered text surface.
        """        
        # Load font 
        font = self.load_font(font_path, size)

        text_surface = font.render(text, True, color) 
        return text_surface  # Returns Surface     

    def get_image(self, image_name):
        """
        Retrieves an image from the resource manager.

        Args:
            image_name (str): The name of the image to retrieve.

        Returns:
            pygame.Surface: The requested image surface.
        """        
        return self.images[image_name]
        
        
        