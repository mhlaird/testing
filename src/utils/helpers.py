import os
import pygame

def load_scaled_image(filename, size):
    """Load and scale an image from the assets directory."""
    try:
        image = pygame.image.load(os.path.join('assets', 'images', filename))
        return pygame.transform.scale(image, size)
    except:
        # Create a transparent surface if image loading fails
        surface = pygame.Surface(size, pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Completely transparent
        return surface 