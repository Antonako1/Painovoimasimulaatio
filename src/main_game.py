import pygame
import sys, importlib, random
import variables
from classes import Ball, Secondary_Panel


class Main_Game:
    def __init__(self) -> None:
        # Importtaa oikean datan importlibillä
        try:
            data_name = f"planet_data.{variables.active_planet}" # Datan nimi
            data_dict = importlib.import_module(data_name) # Importtaa datan 
            copy = data_dict.data.copy()
            if variables.active_planet == "custom":
                copy["gravity"] = variables.custom_planet_g
                copy["mass"] = variables.custom_planet_mass
                copy["radius"] = variables.custom_planet_radius # ???
            variables.active_data = copy # Tekee siitä kopion ja tallentaa sen
            variables.original_data = copy # Tekee siitä kopion ja tallentaa sen
        except ImportError: # Jos importti ei toimi
            # Virhe viesti ja ohjelmasta poistuminen
            print(f"Error: Could not import planet data for {variables.active_planet}", ImportError)
            variables.current_state = variables.GameStates.MAINMENU_WAITINPUT
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
        variables.balls = []
        #
        # Alotuspallot
        for i in range(2):
            variables.balls.append(Ball(
                random.randint(variables.screen_dict["middle_x"] - 100, variables.screen_dict["middle_x"] + 100) , random.randint(0, 100), # X, Y
                random.randint(10, 30), 10, # Radius, mass,
                random.randint(10, 300), random.randint(-300, 300), # Vertical-, horizontal velocity
                0.8, 0.7, # elasticity, rigidness
                [255,0,0])) # Colour
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
                    variables.balls.clear()
                    variables.reset_form()
                    variables.active_ball_index = 0
                    variables.current_state = variables.GameStates.INITIALIZE_MAINGAME
                if event.key == pygame.K_h:
                    variables.active_ball_index = 0
                    variables.reset_form()
                    variables.current_state = variables.GameStates.MAINMENU_WAITINPUT
                
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
            
            ####################
            # Aktiivisen pallon muokkaus
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, ball in enumerate(variables.balls):
                    _rect = pygame.Rect(ball.x-ball.radius, ball.y-ball.radius, ball.radius*2, ball.radius*2)
                    if _rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                        variables.active_ball_index = i
            
            #####################################
            #
            # Input kenttä 1
            # 
            # Joutuu loopata kahesti putkeen koska ei äly riitä
            # Köykästä koodia
            #       I
            #       I
            #       V
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
                
                if not _success:
                    for input_field in variables.input_fields_1:
                        # Resetoi muut
                        for input_field_temp in variables.input_fields_1:
                            input_field_temp.active = False
                            if input_field_temp.info_str == " Air density" and (input_field_temp.text == "" or float(input_field_temp.text) <= 0.000001):
                                # Ilman tiheys ei voi olla nolla
                                input_field_temp.text = "0.00001"
                                input_field_temp.update_variables()
                            elif input_field_temp.text == "":
                                input_field_temp.text = "0"   
                                input_field_temp.update_variables()             
    
            for input_field in variables.input_fields_1:
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
            ############################
            # Toggle napit. edit, add
            ############################
            for button in variables.form_button_row_1:
                is_hovered = button.rect.collidepoint(variables.mouse[0], variables.mouse[1])
                if button.text == "Add new ball" and is_hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    variables.active_add_new_ball = True
                    variables.active_edit_current_ball = False
                    pass
                elif button.text == "Edit cur. ball" and is_hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    variables.active_add_new_ball = False
                    variables.active_edit_current_ball = True
                    pass
            
            ############################
            # Input 2, editointi kenttä#
            ############################
            _success = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and variables.active_edit_current_ball:
                for button in variables.button_row_2:
                    if button.rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                        if button.text == "Delete":
                            try:
                                variables.balls.pop(variables.active_ball_index)
                                variables.active_ball_index = 0
                            except:
                                # pop from empty list
                                pass
                        elif button.text == "Freeze":
                            button.active = not(button.active)
                            variables.balls[variables.active_ball_index].freeze = not variables.balls[variables.active_ball_index].freeze
                        elif button.text == "Throw":
                            variables.balls[variables.active_ball_index].vertical_velocity = random.randint(-1500, 1500)
                            variables.balls[variables.active_ball_index].horizontal_velocity = random.randint(-1500, 1500)

                            

                for input_field in variables.input_fields_2:
                    if input_field.input_field_rect.collidepoint(variables.mouse[0], variables.mouse[1]):

                        # Resetoi muut
                        for input_field_temp in variables.input_fields_2:
                            input_field_temp.active = False
                        # Ja antaa aktiivisen uudelle
                        input_field.active = True
                        _success = True
                        break
                
                if not _success:
                    for input_field in variables.input_fields_2:
                        # Resetoi muut
                        for input_field_temp in variables.input_fields_2:
                            input_field_temp.active = False
                            if input_field_temp.text == "":
                                input_field_temp.text = "0"   
                                input_field_temp.update_variables()  
            
            for input_field in variables.input_fields_2:
                # Näppäimien paineluun
                if event.type == pygame.KEYDOWN and input_field.active  and variables.active_edit_current_ball:
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
            
            ###############################
            # Input 3, uudet pallot       #
            ###############################
            _success = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and variables.active_add_new_ball:
                for item in variables.edit_row_3:
                    # click
                    try:
                        if item.rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                            try:
                                if item.text == "Add new ball(s)":
                                    self.add_balls()
                            except:
                                # En muista
                                pass
                    except:
                        # En muista
                        pass

                            
                # Määrä field
                for input_field in variables.edit_row_3:
                    try:
                      if input_field.input_field_rect.collidepoint(variables.mouse[0], variables.mouse[1]):

                        # Resetoi inputin
                            for input_field_temp in variables.edit_row_3:
                                input_field_temp.active = False
                            
                                # Ja antaa aktiivisen uudelle
                                input_field.active = True
                                _success = True
                                break
                    except:
                        # Sisältää eri luokkia
                        pass
                    
                # Määrä field
                if not _success:
                    for input_field in variables.edit_row_3:
                        # Resetoi muut
                        for input_field_temp in variables.edit_row_3:
                            input_field_temp.active = False
                            try:
                                if input_field_temp.text == "" or int(input_field_temp.text) <= 0:
                                    input_field_temp.text = "1"   
                                    input_field_temp.update_variables() 
                            except:
                                # Sisältää eri luokkia
                                pass
                # Muut

                _success = False
                for input_field in variables.input_fields_3:
                    if input_field.input_field_rect.collidepoint(variables.mouse[0], variables.mouse[1]):
                        # Resetoi muut
                        for input_field_temp in variables.input_fields_3:
                            input_field_temp.active = False
                        # Ja antaa aktiivisen uudelle
                        input_field.active = True
                        _success = True
                        break
                # Muut
                if not _success:
                    for input_field in variables.input_fields_3:
                        # Resetoi muut
                        for input_field_temp in variables.input_fields_3:
                            input_field_temp.active = False
                            if input_field_temp.text == "":
                                input_field_temp.text = "0"   
                                input_field_temp.update_variables()  

            for input_field in variables.input_fields_3:
                # Näppäimien paineluun
                if event.type == pygame.KEYDOWN and input_field.active and variables.active_add_new_ball:
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
            for input_field in variables.edit_row_3:
                # Näppäimien paineluun
                try:
                    if input_field.info_str == " Amount":
                        if event.type == pygame.KEYDOWN and input_field.active and variables.active_add_new_ball:
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
                except:
                    # Eri luokkia
                    pass
#####################################################################################

        # Kakkosikkunan / Paneelin piirto
        if variables.active_secondary_panel:
            variables.secondary_panel.draw()


        # Jos peli on pausella, se ei mee tästä eteenpäin
        # Paneelia voi silti käyttää ja pallojen tietoja muokata
        if variables.active_pause:
            # Pausessa piirretään pallot silti, mutta ilman liikettä
            for ball in variables.balls:
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
        for ball in variables.balls:
            ball.draw() # Laskelmat tapahtuu draw funktiossa itestään

        if len(variables.balls) > 1 and variables.active_collision:
            for i, ball1 in enumerate(variables.balls):
                for j, ball2 in enumerate(variables.balls):
                    if i > j:
                        continue
                    
                    # Pallojen vektorit ja säteet
                    v1 = pygame.math.Vector2(ball1.x, ball1.y)
                    v2 = pygame.math.Vector2(ball2.x, ball2.y)
                    r1 = ball1.radius
                    r2 = ball2.radius

                    # Etäisyys pallojen välillä
                    distance = v1.distance_to(v2)
                    if 0 < distance < r1 + r2:
                        # Jos pidempi kuin pallojen säteet niin normalisoi vektori
                        _normalized_vector = (v1 - v2).normalize()

                        # Energian muutokseen, ennen törmäystä
                        v1_initial_x, v1_initial_y = ball1.horizontal_velocity, ball1.vertical_velocity
                        v2_initial_x, v2_initial_y = ball2.horizontal_velocity, ball2.vertical_velocity

                        # Pallojen uudet velocityt
                        ball1_velocity = pygame.math.Vector2(ball1.horizontal_velocity, ball1.vertical_velocity).reflect(_normalized_vector)
                        ball2_velocity = pygame.math.Vector2(ball2.horizontal_velocity, ball2.vertical_velocity).reflect(_normalized_vector)

                        # Energian muutokseen, törmäyksen jälkeen
                        v1_final_x, v1_final_y = ball1.horizontal_velocity, ball1.vertical_velocity
                        v2_final_x, v2_final_y = ball2.horizontal_velocity, ball2.vertical_velocity

                        # Energian jakautuminen
                        # ball1_velocity.x -= self.energy_transfer(ball1.mass, v1_initial_x, v1_final_x, ball2.mass, v2_initial_x, v2_final_x)
                        # ball1_velocity.y -= self.energy_transfer(ball1.mass, v1_initial_y, v1_final_y, ball2.mass, v2_initial_y, v2_final_y)

                        # ball2_velocity.x -= self.energy_transfer(ball2.mass, v2_initial_x, v2_final_x, ball1.mass, v1_initial_x, v1_final_x)
                        # ball2_velocity.y -= self.energy_transfer(ball2.mass, v2_initial_y, v2_final_y, ball1.mass, v1_initial_y, v1_final_y)
                        ball1_velocity.x -= self.energy_transfer(ball2.mass, v2_initial_x, v2_final_x, ball1.mass, v1_initial_x, v1_final_x)
                        ball1_velocity.y -= self.energy_transfer(ball2.mass, v2_initial_y, v2_final_y, ball1.mass, v1_initial_y, v1_final_y)

                        ball2_velocity.x -= self.energy_transfer(ball1.mass, v1_initial_x, v1_final_x, ball2.mass, v2_initial_x, v2_final_x)
                        ball2_velocity.y -= self.energy_transfer(ball1.mass, v1_initial_y, v1_final_y, ball2.mass, v2_initial_y, v2_final_y)


                        # Pallojen suhteellinen vektori
                        relative_velocity = ball2_velocity - ball1_velocity
                        # Suhteelliset luvut kerrotaan normalisoidun vektorin suunnilla
                        if (relative_velocity.x * _normalized_vector.x) + (relative_velocity.y * _normalized_vector.y) > 0:
                            # Kuinka paljon ne on päällekkäi
                            overlap = (r1 + r2) - distance
                            # Kuinka paljon pitää liikkua ettei olis
                            correction = _normalized_vector * overlap
                            # Pitää tällästä säätöö tehä ettei ne lähe leijumaa
                            if (ball1.horizontal_velocity >= 0 and ball2.horizontal_velocity >= 0) and\
                                    ball2.vertical_velocity != -ball2.horizontal_velocity and\
                                        ball1.vertical_velocity != -ball1.horizontal_velocity:
                                        #  Myös jää jumittaa kun x,y nopeudet on esim: -3, 3
                                ball1.y += (correction.y)
                                ball2.y -= (correction.y)
                            # Pitää myös ilmanvastus ottaa huomioo
                            if (ball1.vertical_velocity >= 0 + ball1.air_resistance and\
                                 ball2.vertical_velocity >= 0 + ball2.air_resistance):
                                ball1.x += (correction.x)
                                ball2.x -= (correction.x)
                            pass
                        
                        # Päivittää x,y nopeudet kumpaankin suuntaan
                        _multiply = 1
                        ball1.horizontal_velocity = _multiply * (ball1_velocity.x * ball1.elasticity)
                        ball1.vertical_velocity = _multiply * (ball1_velocity.y * ball1.elasticity)

                        ball2.horizontal_velocity = _multiply * (ball2_velocity.x * ball2.elasticity) 
                        ball2.vertical_velocity = _multiply * (ball2_velocity.y * ball2.elasticity) 
                         

        variables.CLOCK.tick(60)


    # Lisää uusia palloja
    def add_balls(self):
        for i in range(variables.new_ball_default_amount):
            # Jos enemmän kun yks niin joutuu vähän erottelee +- 1 jotta kollisio "räjäyttää" ne irti toisistaa
            if variables.new_ball_default_amount > 1:
                variables.new_ball_default["x"] =\
                random.randint(variables.new_ball_default["x"]-1, variables.new_ball_default["x"]+1)
                pass

            variables.balls.append(
                Ball(
                variables.new_ball_default["x"], variables.new_ball_default["y"], # X, Y
                variables.new_ball_default["radius"], variables.new_ball_default["mass"], # Radius, mass,
                variables.new_ball_default["vertical_velocity"], variables.new_ball_default["horizontal_velocity"], # Vertical-, horizontal velocity
                variables.new_ball_default["elasticity"], variables.new_ball_default["rigidness"], # elasticity
                [
                    variables.new_ball_default["red"],
                    variables.new_ball_default["green"],
                    variables.new_ball_default["blue"]
                ])
                ) # Colour
        pass
    
    def energy_transfer(self, m1, v1_initial, v1_final, m2, v2_initial, v2_final):
        """
        deltaKE = 0.5 * m1 * (v1_initial^2 - v1_final^2) + 0.5 * m2 * (v2_initial^2 - v2_final^2)

        m = Pallon massat
        v_initial = Nopeus ennen törmäystä
        v_final = Nopeus törmäyksen jälkeen
        deltaKE = Kineettisen energian muutos
        """
        deltaKE = 0.5 * m1 * ((v1_initial)**2 - (v1_final)**2) + 0.5 * m2 * ((v2_initial)**2 - (v2_final)**2)
        return deltaKE
    pass


        

