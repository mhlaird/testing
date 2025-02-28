import pygame
import math
import os
from src.utils.constants import *
from src.utils.helpers import load_scaled_image

class Bird:
    def __init__(self, show_hitboxes=False):
        self.x = 200
        self.y = HEIGHT // 2
        self.velocity = 0
        self.frame = 0
        self.animation_time = 0
        self.angle = 0
        self.show_hitboxes = show_hitboxes
        self.score = 0  # Track score for speed scaling
        
        # Load new bird animation frames
        self.frames = [
            load_scaled_image(os.path.join('Transparent PNG', 'flying', f'frame-{i+1}.png'), (BIRD_SIZE, BIRD_SIZE))
            for i in range(2)
        ]
        
        # Add motion blur effect
        self.motion_trail = []
        
        # Elliptical hitbox parameters
        self.hitbox_width = int(BIRD_SIZE * 0.6)  # Width of ellipse
        self.hitbox_height = int(BIRD_SIZE * 0.5)  # Height of ellipse
        self.hitbox_offset_x = (BIRD_SIZE - self.hitbox_width) // 2
        self.hitbox_offset_y = (BIRD_SIZE - self.hitbox_height) // 2

    def get_rotated_position(self, x, y, cx, cy, angle_deg):
        # Convert angle to radians
        angle_rad = math.radians(angle_deg)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        # Translate point to origin
        dx = x - cx
        dy = y - cy
        
        # Rotate point
        new_x = dx * cos_angle - dy * sin_angle + cx
        new_y = dx * sin_angle + dy * cos_angle + cy
        
        return new_x, new_y

    def get_hitbox_center(self):
        # Calculate the center of the sprite
        sprite_center_x = self.x + BIRD_SIZE // 2
        sprite_center_y = self.y + BIRD_SIZE // 2
        
        # Calculate the offset from sprite center to hitbox center
        offset_x = 0  # No horizontal offset needed as hitbox is centered
        offset_y = 0  # No vertical offset needed as hitbox is centered
        
        # Apply rotation to the offset
        final_x, final_y = self.get_rotated_position(
            sprite_center_x + offset_x,
            sprite_center_y + offset_y,
            sprite_center_x,
            sprite_center_y,
            -self.angle
        )
        
        return (final_x, final_y)

    def point_in_ellipse(self, point, center, width, height, angle_deg):
        # Convert angle to radians
        angle_rad = math.radians(angle_deg)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        # Translate point to origin
        dx = point[0] - center[0]
        dy = point[1] - center[1]

        # Rotate point
        x_rot = dx * cos_angle + dy * sin_angle
        y_rot = -dx * sin_angle + dy * cos_angle

        # Scale to unit circle
        x_scaled = x_rot / (width / 2)
        y_scaled = y_rot / (height / 2)

        # Check if point is inside ellipse
        return (x_scaled * x_scaled + y_scaled * y_scaled) <= 1

    def collides_with_rect(self, rect):
        # Get hitbox parameters
        center = self.get_hitbox_center()
        
        # Check multiple points along each edge of the rectangle
        num_points = 8  # Number of points to check on each edge
        
        # Top edge points
        for i in range(num_points):
            x = rect.left + (rect.width * i / (num_points - 1))
            point = (x, rect.top)
            if self.point_in_ellipse(point, center, self.hitbox_width, self.hitbox_height, -self.angle):
                return True
        
        # Bottom edge points
        for i in range(num_points):
            x = rect.left + (rect.width * i / (num_points - 1))
            point = (x, rect.bottom)
            if self.point_in_ellipse(point, center, self.hitbox_width, self.hitbox_height, -self.angle):
                return True
        
        # Left edge points
        for i in range(num_points):
            y = rect.top + (rect.height * i / (num_points - 1))
            point = (rect.left, y)
            if self.point_in_ellipse(point, center, self.hitbox_width, self.hitbox_height, -self.angle):
                return True
        
        # Right edge points
        for i in range(num_points):
            y = rect.top + (rect.height * i / (num_points - 1))
            point = (rect.right, y)
            if self.point_in_ellipse(point, center, self.hitbox_width, self.hitbox_height, -self.angle):
                return True
        
        # Check if the center of the bird is inside the rectangle
        bird_center = self.get_hitbox_center()
        if rect.collidepoint(bird_center):
            return True
        
        return False

    def flap(self):
        # Flap strength remains constant regardless of speed
        self.velocity = -FLAP_STRENGTH

    def draw(self, screen):
        # Draw motion trail
        for i, (trail_x, trail_y) in enumerate(self.motion_trail[:-1]):
            alpha = int(i * 50)
            trail_surf = self.frames[self.frame].copy()
            trail_surf.set_alpha(alpha)
            rotated = pygame.transform.rotate(trail_surf, -self.angle)
            trail_rect = rotated.get_rect(center=(trail_x + BIRD_SIZE//2, trail_y + BIRD_SIZE//2))
            screen.blit(rotated, trail_rect.topleft)
        
        # Draw bird
        rotated = pygame.transform.rotate(self.frames[self.frame], -self.angle)
        bird_rect = rotated.get_rect(center=(self.x + BIRD_SIZE//2, self.y + BIRD_SIZE//2))
        screen.blit(rotated, bird_rect.topleft)
        
        # Draw elliptical hitbox if enabled
        if self.show_hitboxes:
            center = self.get_hitbox_center()
            hitbox_surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
            pygame.draw.ellipse(hitbox_surface, (255, 0, 0, 128), 
                              (self.hitbox_offset_x, self.hitbox_offset_y, 
                               self.hitbox_width, self.hitbox_height))
            rotated_hitbox = pygame.transform.rotate(hitbox_surface, -self.angle)
            hitbox_rect = rotated_hitbox.get_rect(center=center)
            screen.blit(rotated_hitbox, hitbox_rect.topleft)

    def update(self, dt, score=None):
        if score is not None:
            self.score = score
            
        # Get current speed multiplier
        speed_multiplier = get_speed_multiplier(self.score)
        
        # Store previous position for collision check
        prev_x = self.x
        prev_y = self.y
        
        # Scale the time delta instead of the physics values
        # This makes the bird move through the same arc faster without changing the arc itself
        scaled_dt = dt * speed_multiplier
        
        # Apply gravity with constant values (unscaled)
        self.velocity = min(self.velocity + GRAVITY * scaled_dt, MAX_FALL_SPEED)
        self.y += self.velocity * scaled_dt
        
        # Update animation (modified for 2 frames instead of 3)
        self.animation_time += dt
        if self.animation_time > 0.1:
            self.frame = (self.frame + 1) % 2
            self.animation_time = 0
        
        # Update rotation based on velocity
        target_angle = max(-30, min(self.velocity * 0.2, 90))
        self.angle += (target_angle - self.angle) * scaled_dt * 10
        
        # Update motion trail with centered positions
        self.motion_trail.append((self.x, self.y))
        if len(self.motion_trail) > 5:
            self.motion_trail.pop(0) 