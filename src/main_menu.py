import pygame
import sys
import variables
from classes import Button, Icon_Button


class Main_Menu:
    def __init__(self) -> None:
        self.buttons = [] # Napeille lista, alotus nappi erikseen
        # Rivi 1 ja y akseli
        _cur_y = 50 # Aloituskohta
        self.buttons.append(Icon_Button("mercury", pygame.image.load("images/icons/icon_mercury.png"), _cur_y))
        self.buttons.append(Icon_Button("venus", pygame.image.load("images/icons/icon_venus.png"), _cur_y))
        self.buttons.append(Icon_Button("themoon", pygame.image.load("images/icons/icon_the_moon.png"), _cur_y))
        _cur_y += 125 # Rivin vaihto
        self.buttons.append(Icon_Button("earth", pygame.image.load("images/icons/icon_earth.png"), _cur_y))
        self.buttons.append(Icon_Button("mars", pygame.image.load("images/icons/icon_mars.png"), _cur_y))
        self.buttons.append(Icon_Button("jupiter", pygame.image.load("images/icons/icon_jupiter.png"), _cur_y))
        _cur_y += 125 # Rivin vaihto
        self.buttons.append(Icon_Button("saturn", pygame.image.load("images/icons/icon_saturn.png"), _cur_y))
        self.buttons.append(Icon_Button("uranus", pygame.image.load("images/icons/icon_uranus.png"), _cur_y))
        self.buttons.append(Icon_Button("neptune", pygame.image.load("images/icons/icon_neptune.png"), _cur_y))
        _cur_y += 125 # Rivin vaihto
        self.buttons.append(Icon_Button("pluto", pygame.image.load("images/icons/icon_pluto.png"), _cur_y))
        self.buttons.append(Icon_Button("thesun", pygame.image.load("images/icons/icon_the_sun.png"), _cur_y))
        self.buttons.append(Icon_Button("custom", pygame.image.load("images/icons/icon_custom.png"), _cur_y))

        # Alotus nappi joka laitetaan keskelle
        self.start_button = Button("Start simulation", (40,40,40), (100,100,100), (0, 255, 102))
        self.start_button.x = variables.screen_dict["width"] / 2 - self.start_button.width / 2
        self.start_button.y = variables.screen_dict["height"] / 2
        pass
    def run(self):
        # Hiiren tiedot
        _mouse = pygame.mouse.get_pos()

        # Tausta
        variables.SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Jos hiirellä klikataan ja sen päällä hoverataan
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons: # Iconinappi
                    if button.rect.collidepoint(_mouse[0], _mouse[1]):
                        self.check_clicks(button.target) # Katsotaan mitä klikattiin
                # Starttinappi
                if self.start_button.rect.collidepoint(_mouse[0], _mouse[1]):
                    self.check_clicks(self.start_button.text) # Katsotaan mitä klikattiin
                

        # Piirtää iconi napit
        for i, button in enumerate(self.buttons):
            # y-akseli ilmoitetaan aiemmin
            if i >= 3 and i <= 5:
                # Rivi 2
                i -= 3
            elif i >= 6 and i <= 8:
                # Rivi 3
                i -= 6
            elif i >= 9 and i <= 11:
                i -= 9
            # else: Rivi 1
            button.x = (10) + i + (button.width*i)
            is_hovered = button.rect.collidepoint(_mouse[0], _mouse[1])

            # Aktiivisen planeetan maalaus
            if variables.active_planet == button.target:
                is_hovered = True

            button.draw(is_hovered)
        #
        # Alotusnappi
        is_hovered = self.start_button.rect.collidepoint(_mouse[0], _mouse[1])
        self.start_button.draw(is_hovered)
        # Näytön päivitys
        pygame.display.flip()
        variables.CLOCK.tick(60)

    def check_clicks(self, target):
        # Aktiivisen planeetan nimi
        if target != "Start simulation":
            variables.active_planet = target

        
        match target:
            case "Start simulation": # Aloittaa simulaation
                variables.current_state = variables.GameStates.INITIALIZE_MAINGAME
                pass
            #
            # Planeettaa klikatessa se laittaa uudet arvot variables.py
            # tiedostoon talteen simulaatiota varten

        pass
        


        

