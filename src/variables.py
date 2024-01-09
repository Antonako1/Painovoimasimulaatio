import pygame
from enum import Enum, auto
#
# State-machine
class GameStates(Enum):
    INITIALIZE_PYGAME = auto()

    # Menu
    INITIALIZE_MAINMENU = auto()
    MAINMENU_WAITINPUT = auto()

    # Peli
    PLAY_GAME = auto()
    INITIALIZE_MAINGAME = auto()

current_state = None
main_menu = None
main_game = None

################
# Näyttö
screen_dict = {
    "width": 800,
    "height": 600
}
SCREEN = pygame.display.set_mode((screen_dict["width"], screen_dict["height"]), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.SRCALPHA)
################
#
# Kello
CLOCK = pygame.time.Clock()

# fontti
font = None

# Aktiivinen planeetta
active_planet = "earth" # Default

# Aktiivisen planeetan data
active_data = None