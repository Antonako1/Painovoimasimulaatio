import pygame
import sys
import variables
from classes import Button, Icon_Button, Text_Field, Text_Line
from planet_data import custom

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

        # Customikenttä
        self.custom_fields = []
        self.custom_data = custom.data.copy()
        self.custom_x = variables.screen_dict["width"] - 200
        self.custom_y = 300
        self.custom_fields.append(Text_Field(" Planet's mass (kg)", self.custom_data["mass"], self.custom_x, self.custom_y, 100, 25, 10))
        self.custom_fields.append(Text_Field(" Planet's radius (km)", self.custom_data["radius"], self.custom_x, self.custom_y+50, 100, 25, 10))
        variables.custom_planet_mass = self.custom_data["mass"]
        variables.custom_planet_radius = self.custom_data["radius"]
        self.text_line = Text_Line(" Excepted g-forces:", self.custom_x - 14, self.custom_y + 75)
        # Sekunteihin
        self.seconds = 0
        self.start_ticks = pygame.time.get_ticks()
        pass
    def run(self):
        # Nykyinen tikki
        _cur_tick = pygame.time.get_ticks()
        # Sekunnit
        self.seconds = (_cur_tick - self.start_ticks) / 1000.0
        variables.seconds = self.seconds
        # Hiiren tiedot
        variables.mouse = pygame.mouse.get_pos()

        # Tausta
        variables.SCREEN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F8):
                pygame.quit()
                sys.exit()

            # Jos hiirellä klikataan ja sen päällä hoverataan
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons: # Iconinappi
                    if button.rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                        self.check_clicks(button.target) # Katsotaan mitä klikattiin
                # Starttinappi
                if self.start_button.rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                    self.check_clicks(self.start_button.text) # Katsotaan mitä klikattiin
                pass  
            
            _success = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for input_field in self.custom_fields:
                    if input_field.input_field_rect.collidepoint(variables.mouse[0], variables.mouse[1]):

                        # Resetoi muut
                        for input_field_temp in self.custom_fields:
                            input_field_temp.active = False
                        # Ja antaa aktiivisen uudelle
                        input_field.active = True
                        _success = True
                        break
                
                if not _success:
                    for input_field in self.custom_fields:
                        # Resetoi muut
                        for input_field_temp in self.custom_fields:
                            input_field_temp.active = False
                            if input_field_temp.text == "":
                                input_field_temp.text = "0"   
                                input_field_temp.update_variables()             
    
            for input_field in self.custom_fields:
                # Näppäimien paineluun
                if event.type == pygame.KEYDOWN and input_field.active:
                    # Tallentaa tulokset
                    if event.key == pygame.K_RETURN:
                        input_field.update_variables()
                    elif event.key == pygame.K_BACKSPACE:
                        # Poistaa kirjaimen
                        input_field.text = input_field.text[:-1]
                        input_field.color_input = input_field.color_active_input
                    else:
                        if len(input_field.text) >= input_field.max_input_length:
                            input_field.input_error_time = variables.seconds
                        else:
                            # Lisää kirjaimen
                            input_field.text += event.unicode
                            input_field.color_input = input_field.color_active_input
                            pass
                        pass
                    pass
                pass  

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
            is_hovered = button.rect.collidepoint(variables.mouse[0], variables.mouse[1])

            # Aktiivisen planeetan maalaus
            if variables.active_planet == button.target:
                is_hovered = True

            button.draw(is_hovered)
        

        if variables.main_menu_custom_active:
            pygame.draw.rect(variables.SCREEN, (100,100,100), (self.custom_x - 15, self.custom_y - 15, 400, 110))
            for text_field in self.custom_fields:
                _text_main_rect = variables.font.render("Stats for custom planet", True, (0, 255, 102))
                variables.SCREEN.blit(_text_main_rect, (self.custom_x - 12, self.custom_y - 15, 400, 110))
                text_field.draw()
                mass_celestial_body = variables.custom_planet_mass
                # Painovoiman vetovoima
                gravitational_force = variables.gravitational_constant * 70 * mass_celestial_body / variables.custom_planet_radius**2
                # Painovoiman kiihtyvyys vauhti
                gravitational_acceleration = gravitational_force / 70
                variables.custom_planet_g = round(gravitational_acceleration, 3)

                self.text_line.draw()
            pass
        #
        # Alotusnappi
        is_hovered = self.start_button.rect.collidepoint(variables.mouse[0], variables.mouse[1])
        self.start_button.draw(is_hovered)
        # Näytön päivitys
        pygame.display.flip()
        variables.CLOCK.tick(60)

    def check_clicks(self, target):
        # Aktiivisen planeetan nimi
        if target != "Start simulation":
            variables.active_planet = target
            if target == "custom":
                variables.main_menu_custom_active = True
            else:
                variables.main_menu_custom_active = False

        
        match target:
            case "Start simulation": # Aloittaa simulaation
                variables.current_state = variables.GameStates.INITIALIZE_MAINGAME
                pass
        pass
        


        

