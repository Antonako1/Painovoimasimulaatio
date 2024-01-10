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

# Deltatime tikki
deltatime = None

# Sekunnit
seconds = None

# Aktiivinen planeetta
active_planet = "earth" # Default

# Aktiivisen planeetan data
active_data = None

# Onko peli pausella
active_pause = False
#
#
###########################
#
#       Kakkospaneeli
#
# Onko kakkospaneeli päällä
active_secondary_panel = False
secondary_panel = None # Kakkospaneelin luokka
secondary_panel_width = 500 # sen leveys
secondary_panel_text_width = 200 # sen leveys
radio_buttons = None

# Pitää Radio_Button luokkaan lisätä match caseen jos näitä lisää
active_air_resistance = True
active_ground_friction = True
active_wind_resistance = True
active_ceiling = False # Default

# Tekstikentät ja niitten arvot
input_fields_1 = None

# Nappilista
form_button_row_1 = []
form_button_row_2 = []

# Lisäpaneelin napeille
active_add_new_ball = False
active_edit_current_ball = True
active_ball_index = 0 # TODO

# Nappien ja muitten resetointi
def reset_form():
    global active_air_resistance, active_ground_friction, active_wind_resistance, active_ceiling
    active_air_resistance = True
    active_ground_friction = True
    active_wind_resistance = True
    active_ceiling = False