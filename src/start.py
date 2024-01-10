import pygame, variables
from main_menu import Main_Menu
from main_game import Main_Game
#
#
# State-machine
#
# START
variables.current_state = variables.GameStates.INITIALIZE_PYGAME

def mainLoop():
    while (True):
        match (variables.current_state):
#                       INIT
#-------------------------------------------------------------
            case variables.GameStates.INITIALIZE_PYGAME:
                # Aloittaa pygamen
                initialize()
                variables.current_state = variables.GameStates.INITIALIZE_MAINMENU
                pass
#
#                       Main menu
#-------------------------------------------------------------
            case variables.GameStates.INITIALIZE_MAINMENU:
                # Jos ei ole main menua, se tekee uuden main menun
                if not isinstance(variables.main_menu, Main_Menu):
                    variables.main_menu = Main_Menu()
                # Vaihtaa staten main menuun
                variables.current_state = variables.GameStates.MAINMENU_WAITINPUT
                pass

            case variables.GameStates.MAINMENU_WAITINPUT:
                # Piirtää main menua
                variables.main_menu.run()
                pass
#
#                       Main game
#-------------------------------------------------------------
            case variables.GameStates.INITIALIZE_MAINGAME:
                # Samat homma kun main menussa
                variables.main_game = None
                variables.main_game = Main_Game()

                variables.current_state = variables.GameStates.PLAY_GAME # Menee peliin
                pass

            case variables.GameStates.PLAY_GAME:
                # Ottaa aktiivisen datan ja
                # Piirtää peliä
                variables.mouse = pygame.mouse.get_pos()
                variables.main_game.run()
                pygame.display.flip()
                pass
        pass
    pass

def initialize():
    pygame.init()
    pygame.display.set_caption("Painovoimasimulaatio")
    # Fontti:               font style,    size
    variables.font = pygame.font.SysFont('monospace', 16)


if __name__ == "__main__":
    mainLoop()