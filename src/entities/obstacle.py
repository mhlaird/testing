import pygame
import random
from src.utils.constants import *

class Obstacle:
    def __init__(self, x, gap_y, score=0, show_hitboxes=False):
        self.x = x
        self.gap_y = gap_y
        self.passed = False
        self.show_hitboxes = show_hitboxes
        self.score = score
        
        # Create obstacle surfaces
        self.top_surface = pygame.Surface((OBSTACLE_WIDTH, HEIGHT), pygame.SRCALPHA)
        self.bottom_surface = pygame.Surface((OBSTACLE_WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Define cute colors
        pipe_main = (67, 205, 94)  # Main pipe color (matching grass)
        pipe_light = (87, 225, 114)  # Highlight color
        pipe_dark = (47, 185, 74)  # Shadow color
        pipe_outline = (39, 143, 59)  # Dark outline
        
        # Store cap height for hitbox calculations
        self.cap_height = 30
        
        # Draw both pipes
        self._draw_pipe(self.top_surface, self.gap_y - GAP_HEIGHT/2, True)
        self._draw_pipe(self.bottom_surface, HEIGHT - (self.gap_y + GAP_HEIGHT/2), False)
        
        # Add particle effects
        self.particles = []

    def _draw_pipe(self, surface, height, is_top=True):
        # Define cute colors
        pipe_main = (67, 205, 94)  # Main pipe color (matching grass)
        pipe_light = (87, 225, 114)  # Highlight color
        pipe_dark = (47, 185, 74)  # Shadow color
        pipe_outline = (39, 143, 59)  # Dark outline
        
        # Main pipe body
        pygame.draw.rect(surface, pipe_main, 
                       (5, 0 if is_top else HEIGHT-height, 
                        OBSTACLE_WIDTH-10, height))
        
        # Left edge highlight
        pygame.draw.rect(surface, pipe_light,
                       (5, 0 if is_top else HEIGHT-height,
                        3, height))
        
        # Right edge shadow
        pygame.draw.rect(surface, pipe_dark,
                       (OBSTACLE_WIDTH-8, 0 if is_top else HEIGHT-height,
                        3, height))
        
        # Outline
        pygame.draw.rect(surface, pipe_outline,
                       (5, 0 if is_top else HEIGHT-height,
                        OBSTACLE_WIDTH-10, height), 2)
        
        # Draw end cap
        cap_height = 30
        cap_y = (height if is_top else HEIGHT-height-cap_height)
        
        # Cap main body
        pygame.draw.rect(surface, pipe_main,
                       (0, cap_y, OBSTACLE_WIDTH, cap_height))
        
        # Cap highlight
        pygame.draw.rect(surface, pipe_light,
                       (0, cap_y, 3, cap_height))
        
        # Cap shadow
        pygame.draw.rect(surface, pipe_dark,
                       (OBSTACLE_WIDTH-3, cap_y, 3, cap_height))
        
        # Cap outline
        pygame.draw.rect(surface, pipe_outline,
                       (0, cap_y, OBSTACLE_WIDTH, cap_height), 2)
        
        # Decorative rings
        ring_spacing = 40
        start_y = cap_y + cap_height if is_top else HEIGHT-height
        end_y = height if is_top else HEIGHT-height-cap_height
        
        for y in range(int(start_y), int(end_y), ring_spacing):
            pygame.draw.rect(surface, pipe_light,
                           (5, y, OBSTACLE_WIDTH-10, 4))
            pygame.draw.rect(surface, pipe_outline,
                           (5, y, OBSTACLE_WIDTH-10, 4), 1)

    def update(self, dt, score=None):
        if score is not None:
            self.score = score
        speed_multiplier = get_speed_multiplier(self.score)
        self.x -= BASE_OBSTACLE_SPEED * speed_multiplier * dt
        
        # Update particles
        for particle in self.particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
            else:
                particle['x'] += particle['dx'] * dt
                particle['y'] += particle['dy'] * dt
                particle['size'] *= 0.95

    def get_rects(self):
        # Return full-size rectangles for accurate collision detection
        # Top pipe: Include the cap at the bottom
        top_rect = pygame.Rect(
            self.x,
            0,
            OBSTACLE_WIDTH,
            self.gap_y - GAP_HEIGHT/2 + self.cap_height  # Extended to include cap
        )
        
        # Bottom pipe: Include the cap at the top
        bottom_rect = pygame.Rect(
            self.x,
            self.gap_y + GAP_HEIGHT/2 - self.cap_height,  # Start higher to include cap
            OBSTACLE_WIDTH,
            HEIGHT - (self.gap_y + GAP_HEIGHT/2 - self.cap_height)
        )
        return top_rect, bottom_rect

    def draw(self, screen):
        # Draw obstacles
        screen.blit(self.top_surface, (self.x, 0))
        screen.blit(self.bottom_surface, (self.x, 0))
        
        # Add some ambient particles
        if random.random() < 0.1:
            particle_color = (
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(200, 255)
            )
            self.particles.append({
                'x': self.x + random.randint(0, OBSTACLE_WIDTH),
                'y': self.gap_y + random.randint(-GAP_HEIGHT//2, GAP_HEIGHT//2),
                'dx': random.uniform(-20, 20),
                'dy': random.uniform(-20, 20),
                'size': random.uniform(2, 4),
                'life': random.uniform(0.3, 0.8),
                'color': particle_color
            })
        
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 1.5))
            surf = pygame.Surface((int(particle['size']), int(particle['size'])), pygame.SRCALPHA)
            color_with_alpha = (*particle['color'], alpha)
            pygame.draw.circle(surf, color_with_alpha, 
                             (int(particle['size']/2), int(particle['size']/2)), 
                             int(particle['size']/2))
            screen.blit(surf, (particle['x'], particle['y']))
        
        # Draw hitboxes if enabled
        if self.show_hitboxes:
            top_rect, bottom_rect = self.get_rects()
            pygame.draw.rect(screen, (255, 0, 0), top_rect, 1)
            pygame.draw.rect(screen, (255, 0, 0), bottom_rect, 1) 