import pygame
import os

# Initialize Pygame
pygame.init()

# Create images directory if it doesn't exist
os.makedirs('assets/images', exist_ok=True)

# Helper function to create and save surfaces
def save_surface(surface, filename):
    pygame.image.save(surface, os.path.join('assets', 'images', filename))

# Create background layers
for layer, (r, g, b) in enumerate([
    (100, 150, 255),  # Far background
    (120, 170, 255),  # Mid background
    (140, 190, 255)   # Near background
]):
    surf = pygame.Surface((800, 600))
    surf.fill((r, g, b))
    
    # Add some clouds or details
    for i in range(10):
        pygame.draw.circle(surf, (255, 255, 255, 128), 
                         (i * 80, 100 + (layer * 50)), 
                         30 + (layer * 10))
    
    save_surface(surf, f'bg_{["far", "mid", "near"][layer]}.png')

# Create bird frames
for i in range(3):
    bird = pygame.Surface((50, 50), pygame.SRCALPHA)
    
    # Bird body
    pygame.draw.ellipse(bird, (255, 220, 0), (10, 10, 30, 30))
    
    # Wing position based on frame
    wing_y = 20 + (i * 5)
    pygame.draw.polygon(bird, (255, 200, 0), 
                       [(15, wing_y), (5, wing_y + 10), (25, wing_y + 5)])
    
    # Eye
    pygame.draw.circle(bird, (0, 0, 0), (35, 20), 3)
    
    save_surface(bird, f'bird_{i}.png')

# Create obstacle (pipe/tree)
obstacle = pygame.Surface((80, 600), pygame.SRCALPHA)
for y in range(0, 600, 20):
    color = (34, 139, 34) if y % 40 == 0 else (40, 160, 40)
    pygame.draw.rect(obstacle, color, (0, y, 80, 20))
pygame.draw.rect(obstacle, (45, 180, 45), (5, 0, 70, 600))

save_surface(obstacle, 'obstacle_top.png')
save_surface(obstacle, 'obstacle_bottom.png')

print("Assets generated successfully!") 