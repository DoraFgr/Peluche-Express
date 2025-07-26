import arcade
import argparse
import logging
from src.game import PelucheGame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 840
SCREEN_TITLE = "Peluche Express"

def main():
    parser = argparse.ArgumentParser(description='Peluche Express Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    
    # Configure logging
    if args.debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logging.debug("Debug mode enabled")
    else:
        logging.basicConfig(level=logging.WARNING)
    
    game = PelucheGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main() 