#!/usr/bin/env python3
"""
Game launcher script that provides a convenient way to start the game
with various command line options.
"""

import os
import sys
import argparse
import subprocess

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Launch Flappy Bird Style Game')
    parser.add_argument('--show-hitboxes', action='store_true', 
                      help='Show collision hitboxes')
    parser.add_argument('--debug', action='store_true',
                      help='Enable debug mode with additional logging')
    args = parser.parse_args()

    # Get the root directory of the project
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Add the root directory to Python path
    sys.path.insert(0, root_dir)
    
    # Prepare the command to run the game
    cmd = [sys.executable, '-m', 'src.main']
    
    # Add any command line arguments
    if args.show_hitboxes:
        cmd.append('--show-hitboxes')
    
    try:
        # Run the game module
        subprocess.run(cmd, cwd=root_dir, check=True)
    except KeyboardInterrupt:
        print("\nGame terminated by user")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Error running game: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 