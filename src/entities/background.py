import pygame
import random
from src.utils.constants import *
from src.entities.cloud import Cloud

class Background:
    def __init__(self):
        # Base speeds for each layer
        self.base_speeds = [30, 60, 90]
        self.layers = [
            {
                'speed': self.base_speeds[0],
                'position': 0,
                'clouds': [
                    Cloud(
                        random.randint(0, WIDTH),
                        random.randint(50, HEIGHT//3),
                        self.base_speeds[0],
                        scale=1.2
                    ) for _ in range(NUM_CLOUDS_PER_LAYER)
                ]
            },
            {
                'speed': self.base_speeds[1],
                'position': 0,
                'clouds': [
                    Cloud(
                        random.randint(0, WIDTH),
                        random.randint(30, HEIGHT//3),
                        self.base_speeds[1],
                        scale=1.0
                    ) for _ in range(NUM_CLOUDS_PER_LAYER)
                ]
            },
            {
                'speed': self.base_speeds[2],
                'position': 0,
                'clouds': [
                    Cloud(
                        random.randint(0, WIDTH),
                        random.randint(20, HEIGHT//4),
                        self.base_speeds[2],
                        scale=0.8
                    ) for _ in range(NUM_CLOUDS_PER_LAYER)
                ]
            }
        ]
        
        # Create ground surface with double width for seamless scrolling
        self.ground_width = WIDTH * 2
        self.ground_position = 0
        self.ground_speed = BASE_OBSTACLE_SPEED  # Match obstacle speed
        self.ground_surface = pygame.Surface((self.ground_width, GROUND_HEIGHT))
        
        # Define cute colors for the ground layers
        grass_top = (67, 205, 94)      # Bright grass
        grass_mid = (52, 174, 75)      # Mid grass
        grass_bottom = (39, 143, 59)   # Dark grass
        dirt_top = (161, 103, 49)      # Light dirt
        dirt_bottom = (130, 83, 39)    # Dark dirt
        
        # Create layered ground effect
        grass_height = int(GROUND_HEIGHT * 0.4)  # Top 40% is grass
        
        # Fill the base with dark dirt
        self.ground_surface.fill(dirt_bottom)
        
        # Add dirt gradient
        for y in range(grass_height, GROUND_HEIGHT):
            progress = (y - grass_height) / (GROUND_HEIGHT - grass_height)
            color = (
                dirt_top[0] + (dirt_bottom[0] - dirt_top[0]) * progress,
                dirt_top[1] + (dirt_bottom[1] - dirt_top[1]) * progress,
                dirt_top[2] + (dirt_bottom[2] - dirt_top[2]) * progress
            )
            pygame.draw.line(self.ground_surface, color, (0, y), (self.ground_width, y))
        
        # Add grass layers
        for y in range(grass_height):
            progress = y / grass_height
            if progress < 0.3:  # Top layer
                color = grass_top
            elif progress < 0.6:  # Middle layer
                color = grass_mid
            else:  # Bottom layer
                color = grass_bottom
            pygame.draw.line(self.ground_surface, color, (0, y), (self.ground_width, y))
        
        # Add grass tufts
        for _ in range(100):
            x = random.randint(0, self.ground_width)
            height = random.randint(4, 8)
            width = random.randint(3, 6)
            pygame.draw.ellipse(self.ground_surface, grass_top, 
                              (x, 0, width, height))
        
        # Add small flowers randomly
        flower_colors = [
            (255, 255, 255),  # White
            (255, 220, 100),  # Yellow
            (255, 182, 193),  # Pink
        ]
        
        for _ in range(40):
            x = random.randint(0, self.ground_width)
            y = random.randint(2, grass_height - 4)
            color = random.choice(flower_colors)
            size = random.randint(2, 3)
            pygame.draw.circle(self.ground_surface, color, (x, y), size)
        
        # Create a gradient sky
        self.sky = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            color = (
                135 - (y / HEIGHT) * 30,
                206 - (y / HEIGHT) * 40,
                235 - (y / HEIGHT) * 30
            )
            pygame.draw.line(self.sky, color, (0, y), (WIDTH, y))

    def update(self, dt, score=0):
        speed_multiplier = get_speed_multiplier(score)
        
        # Update cloud layers with scaled speed
        for i, layer in enumerate(self.layers):
            scaled_speed = self.base_speeds[i] * speed_multiplier
            layer['position'] = (layer['position'] - scaled_speed * dt) % WIDTH
            # Update clouds in this layer with scaled speed
            for cloud in layer['clouds']:
                cloud.speed = scaled_speed
                cloud.update(dt)
        
        # Update ground position with scaled speed
        scaled_ground_speed = self.ground_speed * speed_multiplier
        self.ground_position = (self.ground_position - scaled_ground_speed * dt) % WIDTH

    def draw(self, screen, show_hitboxes=False):
        # Draw the gradient sky background
        screen.blit(self.sky, (0, 0))
        
        # Draw the clouds for each layer
        for layer in self.layers:
            for cloud in layer['clouds']:
                cloud.draw(screen)
        
        # Draw scrolling ground
        ground_y = HEIGHT - GROUND_HEIGHT
        screen.blit(self.ground_surface, (self.ground_position, ground_y))
        screen.blit(self.ground_surface, (self.ground_position - self.ground_width/2, ground_y))
        
        # Draw ground hitbox if enabled
        if show_hitboxes:
            ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT + 2, WIDTH, GROUND_HEIGHT - 2)
            pygame.draw.rect(screen, (255, 0, 0), ground_rect, 1)
            pygame.draw.line(screen, (255, 0, 0), (0, HEIGHT - GROUND_HEIGHT),
                           (WIDTH, HEIGHT - GROUND_HEIGHT), 2) 