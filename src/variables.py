import pygame, random
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
main_menu_custom_active = False
main_game = None

gravitational_constant = 6.674e-11 # Nm^2/kg^2

################
# Näyttö
screen_dict = {
    "width": 800,
    "height": 600,
    "middle_x": 400,
    "middle_y": 300,
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
original_data = None

# Onko peli pausella
active_pause = False

# Pallolista
balls = []
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
secondary_panel_text_width = 175 # sen leveys
radio_buttons = None

# Pitää Radio_Button luokkaan lisätä match caseen jos näitä lisää
active_air_resistance = True
active_ground_friction = True
active_wind_resistance = True
active_ceiling = True # Default
active_collision = True

active_advanced_ball = False

# Tekstikentät ja niitten arvot
input_fields_1 = None

# Nappilista
form_button_row_1 = []
form_button_row_2 = []

# Lisäpaneelin napeille
active_add_new_ball = False
active_edit_current_ball = True
active_ball_index = 0
active_zero_g = False

# Editointilista
input_fields_2 = []
# Ja napit
button_row_2 = []

#Uusi pallo formi
input_fields_3 = None
# Ja napit
edit_row_3 = [] # Sisältää yhen input fieldin

# Uuden pallon defaultti tiedot
new_ball_default_amount = 1
new_ball_default = {
    "x": screen_dict["width"] / 2,
    "y": 10,
    "radius": 15,
    "mass": 1,
    "vertical_velocity": 100,
    "horizontal_velocity": 50,
    "elasticity": 0.8,
    "rigidness": 0.99,
    "red": 255,
    "green": 255,
    "blue": 0,
}

gravity_experienced = None
wind_experienced = None 
drag_experienced = None 

# Nappien ja muitten resetointi
def reset_form():
    global active_advanced_ball, active_air_resistance, active_ground_friction, active_wind_resistance, active_ceiling
    active_air_resistance = True
    active_ground_friction = True
    active_wind_resistance = True
    active_ceiling = True
    active_advanced_ball = False
    active_zero_g = False