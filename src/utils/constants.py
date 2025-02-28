import math

# Game window dimensions
WIDTH = 800
HEIGHT = 600

# Game physics
GRAVITY = 600  # Reduced from 1000 to make the game feel better
FLAP_STRENGTH = 250  # Reduced slightly to match new gravity
BASE_OBSTACLE_SPEED = 200  # Base speed that will be scaled with score
MAX_OBSTACLE_SPEED = 400   # Maximum speed cap
SPEED_INCREASE_FACTOR = 0.1  # How much to increase speed per score point
MAX_FALL_SPEED = 400  # New constant to limit maximum fall speed

# Speed scaling function
def get_speed_multiplier(score):
    return min(1 + score * SPEED_INCREASE_FACTOR, MAX_OBSTACLE_SPEED / BASE_OBSTACLE_SPEED)

# Game objects
SPACING = 300  # Horizontal distance between pipes
GAP_HEIGHT = 200  # Increased from 150 to 200 for more vertical space between pipes
GROUND_HEIGHT = 100
BIRD_SIZE = 50
OBSTACLE_WIDTH = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
BIRD_YELLOW = (255, 255, 0)
TREE_GREEN = (34, 139, 34)

# Cloud configuration
CLOUD_LAYERS = 3  # Number of background parallax layers
NUM_CLOUDS_PER_LAYER = 4  # Number of clouds in each layer
CLOUD_MIN_SCALE = 0.7
CLOUD_MAX_SCALE = 1.3 