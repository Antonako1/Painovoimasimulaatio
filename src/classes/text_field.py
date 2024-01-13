import pygame, variables, random
class Text_Field:
    def __init__(self, info_str:str, text:str, x:int, y:int, width:int, height:int, max_length:int) -> None:
        self.info_str = info_str
        self.text = str(text)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text_colour = (0, 255, 102)

        # Tekstin taustan palikka ja reuna väri
        # Harmaa normiväri
        self.color_inactive_input = (150,150,150)
        # solarized light active väri
        self.color_active_input = (238,232,213)
        self.input_field_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Väri
        self.color_input = self.color_inactive_input
        # Onko se päällä
        self.active = False

        # Inputin _ animaatioon
        self.start_ticks = pygame.time.get_ticks()
        self.input_error_time = -1# Millon errori

        # Pituus animaatio
        self.info_animation = 0 # Animaation substring indexi
        self.info_timer = 0

        self.max_input_length = max_length # Tekstikentän maksimi pituus

        self.input_done = False
        pass
    def draw(self):
        # Input tekstin piirto
        txt_surface = variables.font.render(self.text, True, self.text_colour)
        
        # Taustapalikan väri
        if self.active:
            self.color_input = self.color_active_input
        else: 
            self.color_input = self.color_inactive_input

        x_y_plus = (5, 5) 
        # Piirtää tekstin
        variables.SCREEN.blit(txt_surface, (self.input_field_rect.x+x_y_plus[0], self.input_field_rect.y+x_y_plus[1]))
        
        _memory_rect = self.input_field_rect.copy()
        # Jos errori niin tärisee
        if variables.seconds - self.input_error_time <= 0.25:
            # Tärisee input
            shake_offset = (random.randint(-1, 1), random.randint(-1, 1))
            _memory_rect.x += shake_offset[0]
            _memory_rect.y += shake_offset[1]
            self.color_input = (235, 71, 52) # Punanen reunaväri
        # Joka sekunti jos aktiivinen, piirretään "_"
        elif round(variables.seconds, 1) % 1 == 0 and self.active and not len(self.text) >= self.max_input_length:
                # Piirtää sen vilkkuvan viivan: _
                _line = variables.font.render("_", True, self.text_colour)
                variables.SCREEN.blit(_line, (self.input_field_rect.x +5 +txt_surface.get_width(), self.input_field_rect.y+5))
                pass
        
        # Piirtää laatikon
        pygame.draw.rect(variables.SCREEN, self.color_input, _memory_rect, 2)   

        _info_x = self.x + self.input_field_rect.width + 3
        #
        #
        # Teksti viereen 
        # Animaatio mukana
        _info_txt_surface = variables.font.render(self.info_str, True, self.text_colour)
        # Jos teksti menee yli 
        if _info_txt_surface.get_width() + _info_x >= variables.screen_dict["width"] - variables.secondary_panel_text_width - 10:
            # Tekee uuden stringin joka kirjoitetaan
            _info_str_substr = self.construct_new_string(self.info_str, self.info_animation, 999)
            _info_txt_surface = variables.font.render(_info_str_substr, True, self.text_colour)

            # Joka 0.25 sekuntia animaatiota liikutetaan
            if variables.seconds - self.info_timer >= 0.25:
                # Lisätään substringin alku
                self.info_animation += 1
                # Nykyinen aika
                self.info_timer = variables.seconds
                # Jos menee yli pituuden
                if (self.info_animation) == len(self.info_str):
                    self.info_animation = 0
                    pass
                pass
            pass

        variables.SCREEN.blit(_info_txt_surface, (_info_x, self.y + 1))
        pass
    def update_variables(self):
        try:
            # Tallentaa tiedot
            match self.info_str:
            #################################
            #           input 1             #
            #################################
                # tallennetaan
                case " Gravity":
                    variables.active_data["gravity"] = float(self.text)
                    pass
                case " Air density":
                    if float(self.text) <= 0.000001:
                        # Ilman tiheys ei voi olla nolla
                        self.text = "0.00001"
                    variables.active_data["air_density"] = float(self.text)
                    pass
                case " Ground friction":
                    variables.active_data["ground_friction"] = float(self.text)
                    pass
                case " Wind speed (m/s)":
                    if float(self.text) <= 0.000001:
                        # Tuulen nopeus ei voi olla nolla
                        self.text = "0.00001"
                    variables.active_data["wind_speed"] = float(self.text)
                    pass
                case " Wind direction (degrees from middle)":
                    variables.active_data["wind_direction"] = float(self.text)

            #################################
            #           input 2             #
            #################################
            # Edit #
            if variables.active_edit_current_ball:
                match self.info_str:
                    case "x-pos.":
                        variables.balls[variables.active_ball_index].x = float(self.text)
                        pass
                    case " y-pos.":
                        variables.balls[variables.active_ball_index].y = float(self.text)
                        pass
                    case "radius":
                        variables.balls[variables.active_ball_index].radius = float(self.text)
                        pass
                    case " mass (kg)":
                        variables.balls[variables.active_ball_index].mass = float(self.text)
                    case "ver. vel.":
                        variables.balls[variables.active_ball_index].vertical_velocity = float(self.text)
                        pass
                    case " hor. vel.":
                        variables.balls[variables.active_ball_index].horizontal_velocity = float(self.text)
                        pass
                    case "rigidness":
                        variables.balls[variables.active_ball_index].rigid = float(self.text)
                    case " elasticity":
                        variables.balls[variables.active_ball_index].elasticity = float(self.text)
                    case "Red":
                        if float(self.text) <= 255:
                            variables.balls[variables.active_ball_index].colour[0] = float(self.text)
                    case "Green":
                        if float(self.text) <= 255:
                            variables.balls[variables.active_ball_index].colour[1] = float(self.text)
                    case " Blue":
                        if float(self.text) <= 255:
                            variables.balls[variables.active_ball_index].colour[2] = float(self.text)
                        pass
            elif variables.active_add_new_ball:
                ###########
                # INPUT 3 #
                ###########
                # Uusi pallo
                match self.info_str:
                    case "x-pos.":
                        variables.new_ball_default["x"] = float(self.text)
                        pass
                    case " y-pos.":
                        variables.new_ball_default["y"] = float(self.text)
                        pass
                    case "radius":
                        variables.new_ball_default["radius"] = float(self.text)
                        pass
                    case " mass (kg)":
                        variables.new_ball_default["mass"] = float(self.text)
                    case "ver. vel.":
                        variables.new_ball_default["vertical_velocity"] = float(self.text)
                        pass
                    case " hor. vel.":
                        variables.new_ball_default["horizontal_velocity"] = float(self.text)
                        pass
                    case "rigidness":
                        variables.new_ball_default["rigidness"] = float(self.text)
                    case " elasticity":
                        variables.new_ball_default["elasticity"] = float(self.text)
                    case "Red":
                        if float(self.text) <= 255:
                            variables.new_ball_default["red"] = float(self.text)
                        else:
                            variables.new_ball_default["red"] = 0
                    case "Green":
                        if float(self.text) <= 255:
                            variables.new_ball_default["green"] = float(self.text)
                        else:
                            variables.new_ball_default["green"] = 0
                    case " Blue":
                        if float(self.text) <= 255:
                            variables.new_ball_default["blue"] = float(self.text)
                        else:
                            variables.new_ball_default["blue"] = 0
                        pass
                    case " Amount":
                        variables.new_ball_default_amount = int(self.text)
            # Kattoo eriksee
            if variables.main_menu_custom_active:
                match self.info_str:
                    case " Planet's mass (kg)":
                        variables.custom_planet_mass = float(self.text)
                    case " Planet's radius (km)":
                        variables.custom_planet_radius = float(self.text)

                pass
        except:
            print("Invalid value")
        pass
    def construct_new_string(self, text:str, index:int, max=int):
        _final_text = ""

        # Looppaa indexistä eteenpäin kaikki kirjaimet tekstiin
        for jindex, letter in enumerate(text):
            if jindex >= index and len(_final_text) != max:
                _final_text += letter
            pass
        # Looppaa indexistä taaksepäin kaikki kirjaimet tekstiin
        for jindex, letter in enumerate(text):
            if jindex < index and len(_final_text) != max:
                _final_text += letter
            pass
        return _final_text
    pass
