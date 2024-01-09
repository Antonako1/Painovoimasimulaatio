import pygame
import sys, importlib
import variables
from classes import Ball, Secondary_Panel


class Main_Game:
    def __init__(self) -> None:
        # Importtaa oikean datan importlibillä
        try:
            data_name = f"planet_data.{variables.active_planet}" # Datan nimi
            data_dict = importlib.import_module(data_name) # Importtaa datan 
            variables.active_data = data_dict.data.copy() # Tekee siitä kopion ja tallentaa sen
        except ImportError: # Jos importti ei toimi
            # Virhe viesti ja ohjelmasta poistuminen
            print(f"Error: Could not import planet data for {variables.active_planet}")
            pygame.quit()
            sys.exit()

        # Sekunteihin
        self.seconds = 0
        self.start_ticks = pygame.time.get_ticks()
        #
        # deltatime
        self.dt = 0
        self.prev_tick = 0
        self.start_ball()
        #
        # Kakkos paneeli
        variables.secondary_panel = Secondary_Panel()
        #
        pass
    def start_ball(self):
        # Palloille lista
        self.balls = []
        #
        # Alotuspallo
        self.balls.append(Ball(
            variables.screen_dict["width"] / 2, 20, # X, Y
            10, 10, # Radius, mass,
            100, 150, # Vertical-, horizontal velocity
            0.98, 0.8, # Ground friction, elasticity
            (255,0,0))) # Colour
    def run(self):
        # Tausta
        variables.SCREEN.fill((100, 100, 100))
        # Eventit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Peli pois päältä
                if event.key == pygame.K_F8:
                    pygame.quit()
                    sys.exit()
                
                # Active pause
                if event.key == pygame.K_p:
                    variables.active_pause = not(variables.active_pause)
                if event.key == pygame.K_r: # Restarttia
                    self.start_ball()
                    variables.reset_form()
                    variables.current_state = variables.GameStates.INITIALIZE_MAINGAME
                if event.key == pygame.K_h:
                    variables.reset_form()
                    variables.current_state = variables.GameStates.INITIALIZE_MAINMENU
                
                # Tietopaneeli ja pallojen lisäys paneeli
                if event.key == pygame.K_o:
                    variables.active_secondary_panel = not(variables.active_secondary_panel)
                    
                    if variables.active_secondary_panel:
                        variables.screen_dict["width"] += variables.secondary_panel_width
                        variables.secondary_panel = Secondary_Panel()
                    else:
                        variables.screen_dict["width"] -= variables.secondary_panel_width

                    # Näytön kokoa päivitetään
                    variables.SCREEN = pygame.display.set_mode((variables.screen_dict["width"], variables.screen_dict["height"]), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.SRCALPHA)

            # Kakkospaneelin nappien paineluun
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in variables.radio_buttons:
                    if button.rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                        button.active = not(button.active)
                        button.update_variables("in")
                        pass
                    pass
                pass
            #####################################
            #
            # Input kenttä 1
            # 
            # Joutuu loopata kahesti putkeen koska ei äly riitä
            # Aktiivinen kenttä talteen:
            _success = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for input_field in variables.input_fields_1:
                    if input_field.input_field_rect.collidepoint(variables.mouse[0], variables.mouse[1]):

                        # Resetoi muut
                        for input_field_temp in variables.input_fields_1:
                            input_field_temp.active = False
                        # Ja antaa aktiivisen uudelle
                        input_field.active = True
                        _success = True
                        break

            # Jos vaan klikkaa:
            if not _success and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for input_field in variables.input_fields_1:
                    # Resetoi muut
                    for input_field_temp in variables.input_fields_1:
                        input_field_temp.active = False
                        if input_field_temp.info_str == " Air density" and (input_field_temp.text == "" or float(input_field_temp.text) <= 0.000001):
                            # Ilman tiheys ei voi olla nolla
                            input_field_temp.text = "0.00001"
                        elif input_field_temp.text == "":
                            input_field_temp.text = "0"
                
    
            for input_field in variables.input_fields_1:
                # Näppäimien paineluun
                if event.type == pygame.KEYDOWN and input_field.active:
                    if event.key == pygame.K_BACKSPACE:
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
                    # Tallentaa tulokset
                    input_field.update_variables()
                    pass
                pass
            pass
#####################################################################################

        # Kakkosikkunan / Paneelin piirto
        if variables.active_secondary_panel:
            variables.secondary_panel.draw()


        # Jos peli on pausella, se ei mee tästä eteenpäin
        # Paneelia voi silti käyttää ja pallojen tietoja muokata
        if variables.active_pause:
            # Pausessa piirretään pallot silti, mutta ilman liikettä
            for ball in self.balls:
                ball.draw()
            return

        # Nykyinen tikki
        _cur_tick = pygame.time.get_ticks()


        # Sekunnit
        self.seconds = (_cur_tick - self.start_ticks) / 1000.0
        variables.seconds = self.seconds


        # deltatime sekunneissa
        self.dt = (_cur_tick - self.prev_tick) / 1000.0
        variables.deltatime = self.dt
        self.prev_tick = _cur_tick
        
        # Pallojen piirto
        for ball in self.balls:
            ball.draw() # Laskelmat tapahtuu draw funktiossa itestään

        variables.CLOCK.tick(60)
    pass


        

