import random
from src.utils.constants import *
from src.utils.helpers import load_scaled_image

class Cloud:
    def __init__(self, x, y, speed, scale=1.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.scale = scale * random.uniform(CLOUD_MIN_SCALE, CLOUD_MAX_SCALE)
        
        # Load one of three cloud variations randomly
        cloud_num = random.randint(1, 3)
        self.image = load_scaled_image(f'cloud{cloud_num}.PNG', (int(100 * self.scale), int(60 * self.scale)))
        
        # Add some transparency to the cloud
        if self.image:
            self.image.set_alpha(220)

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x + 200 < 0:  # Use a larger value to account for cloud width
            self.x = WIDTH + 100

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y)) 