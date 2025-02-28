import pygame
import sys
import random
import argparse
from src.utils.constants import *
from src.entities.bird import Bird
from src.entities.obstacle import Obstacle
from src.entities.background import Background

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Flappy Bird Style Game')
    parser.add_argument('--show-hitboxes', action='store_true', help='Show collision hitboxes')
    args = parser.parse_args()

    # Initialize Pygame
    pygame.init()

    # Set up display with resizable flag
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    # Create a surface for rendering at original resolution
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    
    pygame.display.set_caption("Flappy Bird Style Game")

    # Clock for frame rate control
    clock = pygame.time.Clock()

    # Game objects
    bird = Bird(show_hitboxes=args.show_hitboxes)
    obstacles = []
    score = 0
    game_state = "start"
    background = Background()
    
    # Initialize font with anti-aliasing
    font = pygame.font.Font(None, 55)

    def reset_game():
        nonlocal bird, obstacles, score
        bird = Bird(show_hitboxes=args.show_hitboxes)
        obstacles = []
        score = 0

    while True:
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # Update the screen while maintaining aspect ratio
                window_width = event.w
                window_height = event.h
                
                # Calculate the scaling factor to maintain aspect ratio
                scale_w = window_width / WIDTH
                scale_h = window_height / HEIGHT
                scale_factor = min(scale_w, scale_h)
                
                # Calculate the new window size maintaining aspect ratio
                new_width = int(WIDTH * scale_factor)
                new_height = int(HEIGHT * scale_factor)
                
                # Update the screen with the new size
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_state == "start":
                        game_state = "playing"
                        reset_game()
                    elif game_state == "playing":
                        bird.flap()
                    elif game_state == "game_over":
                        game_state = "start"

        # Update background with current score
        background.update(dt, score)

        if game_state == "playing":
            # Store bird's previous position
            prev_x = bird.x
            prev_y = bird.y
            
            bird.update(dt, score)

            # Spawn obstacles
            if not obstacles or obstacles[-1].x < WIDTH - SPACING:
                gap_y = random.randint(GAP_HEIGHT // 2 + 50, HEIGHT - GROUND_HEIGHT - GAP_HEIGHT // 2 - 50)
                obstacles.append(Obstacle(WIDTH, gap_y, score, show_hitboxes=args.show_hitboxes))

            # Update obstacles and check for collisions
            for obs in obstacles[:]:
                prev_obs_x = obs.x
                obs.update(dt, score)
                
                # Check for score
                if obs.x < bird.x and not obs.passed:
                    obs.passed = True
                    score += 1
                
                # Remove if off screen
                if obs.x < -OBSTACLE_WIDTH:
                    obstacles.remove(obs)
                    continue
                
                # Collision detection
                top_rect, bottom_rect = obs.get_rects()
                if bird.collides_with_rect(top_rect) or bird.collides_with_rect(bottom_rect):
                    interpolation = 0.5
                    bird.x = prev_x * interpolation + bird.x * (1 - interpolation)
                    bird.y = prev_y * interpolation + bird.y * (1 - interpolation)
                    game_state = "game_over"
                    break
            
            # Ground and ceiling collision
            ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
            ceiling_rect = pygame.Rect(0, -GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
            
            if bird.collides_with_rect(ground_rect):
                interpolation = 0.5
                bird.y = prev_y * interpolation + bird.y * (1 - interpolation)
                bird.velocity = 0
                game_state = "game_over"
            elif bird.collides_with_rect(ceiling_rect):
                interpolation = 0.5
                bird.y = prev_y * interpolation + bird.y * (1 - interpolation)
                bird.velocity = 0
                game_state = "game_over"

        # Clear the game surface
        game_surface.fill((0, 0, 0))

        # Render game on game_surface
        background.draw(game_surface, show_hitboxes=args.show_hitboxes)
        
        if game_state == "playing":
            for obs in obstacles:
                obs.draw(game_surface)
            bird.draw(game_surface)
            
            # Draw score with shadow effect
            score_text = font.render(f"Score: {score}", True, BLACK)
            shadow_text = font.render(f"Score: {score}", True, (50, 50, 50))
            game_surface.blit(shadow_text, (12, 12))
            game_surface.blit(score_text, (10, 10))
            
            # Draw current speed multiplier
            speed_mult = get_speed_multiplier(score)
            speed_text = font.render(f"Speed: {speed_mult:.1f}x", True, BLACK)
            speed_shadow = font.render(f"Speed: {speed_mult:.1f}x", True, (50, 50, 50))
            game_surface.blit(speed_shadow, (12, 52))
            game_surface.blit(speed_text, (10, 50))
            
        elif game_state == "start":
            start_text = font.render("Press SPACE to Start", True, WHITE)
            shadow_text = font.render("Press SPACE to Start", True, BLACK)
            text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            game_surface.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
            game_surface.blit(start_text, text_rect)
            
        elif game_state == "game_over":
            texts = [
                ("Game Over", -50),
                (f"Score: {score}", 0),
                ("Press SPACE to Restart", 50)
            ]
            
            for text, y_offset in texts:
                rendered_text = font.render(text, True, WHITE)
                shadow_text = font.render(text, True, BLACK)
                text_rect = rendered_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
                game_surface.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
                game_surface.blit(rendered_text, text_rect)

        # Scale the game surface to the window size
        window_size = screen.get_size()
        # Calculate scaling factors
        scale_w = window_size[0] / WIDTH
        scale_h = window_size[1] / HEIGHT
        scale_factor = min(scale_w, scale_h)
        
        # Calculate the scaled dimensions
        scaled_width = int(WIDTH * scale_factor)
        scaled_height = int(HEIGHT * scale_factor)
        
        # Calculate position to center the game
        x_offset = (window_size[0] - scaled_width) // 2
        y_offset = (window_size[1] - scaled_height) // 2
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Scale and blit the game surface
        scaled_surface = pygame.transform.smoothscale(game_surface, (scaled_width, scaled_height))
        screen.blit(scaled_surface, (x_offset, y_offset))

        pygame.display.update()

if __name__ == "__main__":
    main() 