import pygame
class ResourceManager:
    
    def __init__(self):
        self.images = {}
        self.font_cache = {}
        
    def add_image(self, image_name, image):
        self.images[image_name] = image
        
    def load_font(self, font_path, size):
        # Check if the font is already in the cache
        key = (font_path, size)
        if key in self.font_cache:
            return self.font_cache[key]

        # If not in cache, load the font and add it to the cache
        font = pygame.font.Font(font_path, size)
        self.font_cache[key] = font
        return font      

    def get_image(self, image_name):
        return self.images[image_name]
        
        
        