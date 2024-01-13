import pygame, sys, variables, random, main_game
from classes.secondary_panel import Secondary_Panel
# Eventit
def handle_events(self):
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