# Flappy Bird Style Game

A modern implementation of the classic Flappy Bird game, built with Python and Pygame. This version features enhanced graphics, smooth animations, and progressive difficulty scaling.

## Features

- 🎮 Smooth, physics-based gameplay
- 🎨 Beautiful animated sprites and backgrounds
- 🌈 Dynamic motion trails and particle effects
- 📈 Progressive difficulty scaling
- 🖼️ Resizable game window with maintained aspect ratio
- 💫 Precise elliptical hitboxes for accurate collisions
- 🎵 Layered parallax backgrounds with clouds
- 🌱 Decorative ground with grass and flowers

## Requirements

- Python 3.x
- Pygame 2.x

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required dependencies:
```bash
pip install pygame
```

## Running the Game

From the project root directory, run:
```bash
python -m src.main
```

### Command Line Options

- `--show-hitboxes`: Display collision hitboxes (useful for debugging)
```bash
python -m src.main --show-hitboxes
```

## How to Play

- Press SPACE to start the game
- Press SPACE to make the bird flap
- Navigate through the pipes without touching them
- Avoid hitting the ground or ceiling
- Try to achieve the highest score possible!

## Game Mechanics

- The bird maintains a consistent jump height throughout the game
- Game speed increases progressively with score:
  - Score 0: Normal speed (1.0x)
  - Score 5: 1.5x speed
  - Score 10+: 2.0x speed (maximum)
- Obstacles and background scroll faster as speed increases
- Precise collision detection using elliptical hitboxes

## Project Structure

```
src/
├── __init__.py
├── main.py
├── entities/
│   ├── bird.py
│   ├── obstacle.py
│   └── background.py
└── utils/
    ├── constants.py
    └── helpers.py
```

## Controls

- SPACE: Flap/Jump
- SPACE: Start game (when in start screen)
- SPACE: Restart game (when in game over screen)
- Window can be freely resized while maintaining aspect ratio

## Credits

- Game assets from [source of your assets]
- Built with Python and Pygame
- Inspired by the original Flappy Bird game

## License

[Your chosen license]