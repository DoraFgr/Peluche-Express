import arcade
from src.game import PelucheExpress
# Constants
SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 840
SCREEN_TITLE = "Platformer"

def main():
    window = PelucheExpress(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()