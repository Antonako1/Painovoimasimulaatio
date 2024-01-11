import pygame, variables, math, random
#
#
# Perus tekstinappi
#
class Button:
    def __init__(self, text:str, background_colour:tuple, background_colour_hover:tuple, text_colour:tuple) -> None:
        self.text = text
        self.x = 0
        self.y = 0
        # Leveys on tekstin leveys + 5
        self.width = variables.font.render(self.text, True, (0,0,0)).get_width() + 5
        self.height = 40

        self.background_colour = background_colour
        self.background_colour_hover = background_colour_hover
        self.text_colour = text_colour

        self.active = False # ! Temp

        self.make_rect() # Tekee rectin valmiiksi
        pass
    def draw(self, is_hovered):
        self.make_rect()
        # Piirtää teksin taustan
        _active_colour = self.background_colour
        if is_hovered:
            _active_colour = self.background_colour_hover
        pygame.draw.rect(variables.SCREEN, _active_colour, self.rect)

        _text_surface = variables.font.render(self.text, True, self.text_colour)
        variables.SCREEN.blit(_text_surface, (self.x +1, self.y + (self.height / 4)))
        pass

    def make_rect(self): # Tekee rectin
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    pass
#
#
#
# Iconikuva nappi
#
class Icon_Button:
    def __init__(self, target:str, icon_img:pygame.image, y) -> None:
        self.target = target
        # y-akseli ilmoitetaan muista erikseen rivien tekemisen takia 
        self.background_colour = (40,40,40) # Normiväri
        self.background_colour_hover = (100,100,100) # Active ja hoveri väri
        self.x = 0
        self.y = y
        self.width = 100
        self.height = 100
        # Jos planeetta on saturnus, sen leveys on 2 kertaa isompi
        self.image = pygame.transform.scale(icon_img, (self.width, self.height)) # Skaalaus kokoon

        # Tekee rectin
        self.make_rect()
        pass
    def draw(self, is_hovered):
        self.make_rect()
        # Jos hoveri tai active
        _active_colour = self.background_colour
        if is_hovered:
            _active_colour = self.background_colour_hover

        # Rectin piirto
        pygame.draw.rect(variables.SCREEN, _active_colour, self.rect)

        # Kuva samaan kohtaan
        variables.SCREEN.blit(self.image, (self.x, self.y))
        pass
    def make_rect(self):# Taustalle recti
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pass
#
#
# Tekstikenttä kirjottamiseen
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
        self.info_animation = 0
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
                case " Gravity":
                    # tallennetaan
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
            else:
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
                    case " hor. vel":
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
#
#
# Tekstikohta paneeliin
class Text_Line:
    def __init__(self, text, x, y) -> None:
        self.text = text
        self.value = ""
        self.x = x
        self.y = y
        self.text_animation = 0
        self.text_timer = 0
        self.text_colour = (0, 255, 102)
        pass
    def draw(self):
        self.update_values()
        _text_str = self.text + self.value
        # Teksti viereen 
        # Animaatio mukana
        _txt_x = self.x + 3
        _txt_surface = variables.font.render(_text_str, True, self.text_colour)
        # Jos teksti menee yli 
        if _txt_surface.get_width() + _txt_x >= variables.screen_dict["width"] - 10:
            # Tekee uuden stringin joka kirjoitetaan
            _txt_str_substr = self.construct_new_string(_text_str, self.text_animation, 999)
            _txt_surface = variables.font.render(_txt_str_substr, True, self.text_colour)

            # Joka 0.25 sekuntia animaatiota liikutetaan
            if variables.seconds - self.text_timer >= 0.25:
                # Lisätään substringin alku
                self.text_animation += 1
                # Nykyinen aika
                self.text_timer = variables.seconds
                # Jos menee yli pituuden
                if (self.text_animation) == len(_text_str):
                    self.text_animation = 0
                    pass
                pass
            pass

        variables.SCREEN.blit(_txt_surface, (_txt_x, self.y + 1))
        pass
    def update_values(self):
        match self.text:
            case " mouse pos:":
                self.value = f" {variables.mouse[0]}x, {variables.mouse[1]}y"
            case " balls:":
                self.value = f" {len(variables.balls)}"
            case " paused:":
                self.value = f" {variables.active_pause}"
            case " fps:":
                self.value = f" {int(variables.CLOCK.get_fps())}"
            case " base gravity:":
                self.value = f" {variables.original_data['gravity']}"
            case " base air density:":
                self.value = f" {variables.original_data['air_density']}"
            case " planet:":
                self.value = f" {variables.active_planet}"
            case " wind experienced:":
                self.value = f" {variables.wind_experienced}"
            case " gravity experienced:":
                self.value = f" {variables.gravity_experienced}"
            case " drag experienced:":
                self.value = f" {variables.drag_experienced}"
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

#
#
# Radio nappi, On-Off
class Radio_Button:
    def __init__(self, text, x, y) -> None:
        # Ulkoympyrä
        self.radius_out = 10 # Fontin ko'on mukaan
        self.colour_out = (150,150,150)
        # Sisäympyrä
        self.radius_in = self.radius_out -2
        # self.colour_in = (100,100,255)
        self.colour_in = (255,0,0)
        # Sisäympyrä 2
        self.radius_in_2 = self.radius_in -4

        self.x = x
        self.y = y

        self.text = text
        self.text_colour = (0, 255, 102)

        self.make_rect()

        self.active = False
        pass
    def draw(self, is_hovered):
        self.update_variables("out")
        # Ulkoympyrä
        pygame.draw.circle(variables.SCREEN,(self.colour_out), (self.x, self.y), self.radius_out)

        # Sisäympyrä
        # Jos hoverattu tai aktiivinen
        if is_hovered:
            pygame.draw.circle(variables.SCREEN,(self.colour_in), (self.x, self.y), self.radius_in)
            pygame.draw.circle(variables.SCREEN,(self.colour_out), (self.x, self.y), self.radius_in_2)


        # Teksti
        _text_surface = variables.font.render(self.text, True, self.text_colour)
        variables.SCREEN.blit(_text_surface, (self.x + 16, self.y - self.radius_out))

        pass
    def make_rect(self):
        self.rect = pygame.Rect(self.x - self.radius_out, self.y - self.radius_out, self.radius_out * 2, self.radius_out * 2)
        pass
    def update_variables(self, case):
        if case == "out":
            match self.text:
                case "Air resistance":
                    self.active = variables.active_air_resistance
                case "Ground friction":
                    self.active = variables.active_ground_friction
                case "Wind speed":
                    self.active = variables.active_wind_resistance
                case "Active ceiling":
                    self.active = variables.active_ceiling
                case "Ball collisions":
                    self.active = variables.active_collision
                case "Advanced Ball physics":
                    self.active = variables.active_advanced_ball
        elif case == "in":
            match self.text:
                case "Air resistance":
                    variables.active_air_resistance = self.active
                case "Ground friction":
                    variables.active_ground_friction = self.active
                case "Wind speed":
                    variables.active_wind_resistance = self.active
                case "Active ceiling":
                    variables.active_ceiling = self.active
                case "Ball collisions":
                    variables.active_collision = self.active
                case "Advanced Ball physics":
                    variables.active_advanced_ball = self.active
        
        
        pass
    pass
#
#
#
# Pelin pallo joka pomppii
class Ball:
    # X
    # Y
    # Säde
    # Massa
    # Vertikaalinen Nopeus
    # Horisonttaali Nopeus
    # Joustavuus
    # Jäykkyys
    # Pallon väri
    def __init__(self, x:int, y:int, radius:int, mass:int, vertical_velocity:int, horizontal_velocity:int, elasticity:float, rigid:float, colour:list) -> None:
        self.radius = radius
        self.x = x
        self.y = y + radius # Yläkulmaan
        self.colour = colour
        self.mass = mass
        self.vertical_velocity = vertical_velocity
        self.horizontal_velocity = horizontal_velocity
        self.elasticity = elasticity
        self.freeze = False
        self.rigid = rigid
        pass
    def draw(self):
        # Jos pausella, ei liikuteta
        if not variables.active_pause and not self.freeze:
            self.move()


        _ball_colour = (self.colour[0], self.colour[1], self.colour[2])
        # Piirretään pallo tai soikio
        if variables.active_advanced_ball and variables.active_data["gravity"] >= 4.5 and self.rigid < 1:
            deformation = self.gravitational_deformation()
            y_compenstation = 0
            if deformation * 2 > 1.090:
                deformation = 1.090

            pygame.draw.ellipse(variables.SCREEN, _ball_colour, (self.x, self.y - y_compenstation, 2 * self.radius, deformation * 2))
        else:
            pygame.draw.circle(variables.SCREEN, _ball_colour, (self.x, self.y), self.radius)

        pass
    def move(self) -> None:
        # 3d
        if variables.active_advanced_ball:
            self.drag_coefficient = 0.47 # Pallon ilmanvastuskerroin
        #2d
        else:
            self.drag_coefficient = 1.17 # Ympyrän ilmanvastuskerroin
        # Pinta-ala
        self.area = (math.pi*self.radius**2)


        # Nopeus lisätään x- ja y-akseleihin        
        self.y += self.vertical_velocity * variables.deltatime
        self.x += self.horizontal_velocity * variables.deltatime

        # Tuulen vaikutus lisätään tai poistetaan
        if variables.active_wind_resistance:
            """
            Vwind_x = Vwind * cos(θwind) ! Kulma radiaaneina
            Vwind_y = Vwind * sin(θwind) ! Kulma radiaaneina

            v = sqrt((Vobject_x - Vwind_x)^2 + (Vobject_y - Wvind_y)^2)

            Fwind=0.5*Cd*A*ρ*v^2

            Awind = Fwind / m



            ratio = (Aoriginal - Vwind) / v

            Atotal = ratio * Awind

            Cd = Ilmanvastuskerroin
            A = Pinta-ala
            ρ = Ilman tiheys
            v = Nopeus objektin ja tuulen välillä
            m = Massa
            Vobject_x = Objektin nopeus
            Vobject_y = Objektin nopeus
            Vwind_x = Tuulen nopeus
            Vwind_y = Tuulen nopeus
            θwind = Tuulen kulma
            Fwind = Tuulen voima
            Awind = Tuulen kiihdyntä
            Atotal = Lopullinen nopeus
            Aoriginal = Alkuperäinen nopeus
            """
            Owind = variables.active_data["wind_direction"]
            Vwind = variables.active_data["wind_speed"] * 25 # Toimii jostai syystä vaan kun on * 10-100
            Vwind_x = Vwind * math.cos(math.radians(Owind - 90))
            Vwind_y = Vwind * math.sin(math.radians(Owind - 90))

            Vobject_x = self.horizontal_velocity
            Vobject_y = self.vertical_velocity

            v = 1
            try:
                v = math.sqrt((Vobject_x - Vwind_x)**2 + (Vobject_y - Vwind_y)**2)
            except:
                pass

            Fwind = 0.5 * self.drag_coefficient * self.area * variables.active_data["air_density"] * v**2

            Awind = Fwind / (self.mass * 1000)  # Kiloina

            # Tuulen vaikutus
            wind_influence = 0.00001 # Ei toimi muute

            ratio_x = (Vobject_x - Vwind_x) / v
            ratio_y = (Vobject_y - Vwind_y) / v
            
            self.horizontal_velocity += ratio_x * Awind * wind_influence
            self.vertical_velocity += ratio_y * Awind * wind_influence

            variables.wind_experienced = (ratio_x * Awind * wind_influence) + (ratio_y * Awind * wind_influence)
            pass

        # Y-akseli pomppaus, alas ja ylös
        if self.y >= variables.screen_dict["height"] - self.radius \
        or variables.active_ceiling and self.y <= 0 + self.radius:
            # Pallo menee ylös, se jää sinne.
            # Oli väärte päin, sen takii "not"
            self.y = variables.screen_dict["height"] - self.radius if not self.y <= 0 + self.radius else 0 + self.radius
            # Nopeus kääntyy ja se kerrotaan pallon joustavuudella
            self.vertical_velocity = -(self.vertical_velocity * self.elasticity)
            pass
        # X-akseli pomppaus, oikea ja vasen
        # Paneeli päällä, oikea
        # Paneeli pois päältä, oikea
        # Vasen
        if (variables.active_secondary_panel and self.x >= variables.screen_dict["width"] - self.radius - variables.secondary_panel_width) \
        or (not(variables.active_secondary_panel) and self.x >= variables.screen_dict["width"] - self.radius) \
        or (self.x <= 0 + self.radius):
            # Jos kimpoaa vasemmalle, se siirretääm vasempaan reunaan. Sama oikealla
            # Vasen
            # Oikea, paneeli pois päältä
            # Oikea, paneeli päällä
            self.x = 0 + self.radius if self.x < 0 + self.radius else \
                variables.screen_dict["width"] - self.radius if not variables.active_secondary_panel else \
                variables.screen_dict["width"] - self.radius - variables.secondary_panel_width
            # Nopeus kääntyy ja se kerrotaan joustavuudella
            self.horizontal_velocity = -(self.horizontal_velocity * self.elasticity)
            pass
            
        # Lisätään painovoiman ja ilmanvastuksen vaikutus
        """
        newtonin painovoimalaki
        F = (G * m1 * m2) / (r^2)

        g = F/m1

        F = voima
        G = Pysyvä painovoima
        g = painovoima jonka kappale kokee
        m1, m2 = kappaleen massa, kappaleen massa joka vetää puoleensa
        r = Välinen etäisyys

        https://en.wikipedia.org/wiki/Gravity_of_Earth#Conventional_value

        Calculating the gravity at Earth's surface using the average radius of Earth (6,371 kilometres (3,959 mi)),
        [10] the experimentally determined value of the gravitational constant, and the Earth mass of 5.9722 ×1024 
        kg gives an acceleration of 9.8203 m/s2,[11] slightly greater than the standard gravity of 9.80665 m/s2

        TULOS: 9.819860885194819 ≈ 9.8203 (melkeen sama)
        """
        # Planeetan massa
        mass_celestial_body = variables.active_data["mass"]
        # Painovoiman vetovoima
        gravitational_force = variables.gravitational_constant * self.mass * mass_celestial_body / variables.active_data["radius"]**2
        # Painovoiman kiihtyvyys vauhti
        gravitational_acceleration = gravitational_force / self.mass
        # Lopullinen muuttuja
        _velocity_gravitational_effect = gravitational_acceleration

        # Lisätään ilman vastus
        variables.drag_experienced = 0
        if variables.active_air_resistance:
            drag = self.gravitation_drag()
            variables.drag_experienced += drag
            _velocity_gravitational_effect -= drag
            # _velocity_gravitational_effect *= variables.deltatime
        self.vertical_velocity += (_velocity_gravitational_effect)
        variables.gravity_experienced = (_velocity_gravitational_effect)

        # Lisätään maan kitka jos se koskettaa maan pintaa ja toggle on päällä
        if self.y >= variables.screen_dict["height"] - self.radius and variables.active_ground_friction:
            self.horizontal_velocity *= variables.active_data["ground_friction"]
            variables.drag_experienced += variables.active_data["ground_friction"]
            pass
        pass

    def gravitation_drag(self) -> float:
        """
        Laskee painovoiman vastuksen

        Termit:
            ρ = Ilman tiheys
            Cd = Ilmanvastuskerroin
            A = Pinta-ala
            v = Nopeus
            F_gravity = Painovoiman aiheuttama voima
            F_drag = Voiman vastus liikkeen vastakkaiseen suuntaan
            F_net = F_gravityn ja F_dragin netto
            a = Kiihtyvyys
        Kaava:
            F_drag=1/2ρCdAv^2

            F_gravity=m⋅g

            F_net=F_gravity-F_drag

            a=m/F_net
        """
        # Voiman vastus
        f_drag = ((1/2) * variables.active_data["air_density"] * self.drag_coefficient * self.area) * (self.vertical_velocity**2)
        # return f_drag / self.mass # ?
        # Painovoiman voima | N
        f_gravity = (self.mass / 1000) * variables.active_data["gravity"]

        # Netto voima
        f_net = f_gravity - f_drag

        # Painovoiman tuottama kiihtyminen ilmanvastus mukaan lukien
        a = self.mass / f_net
        return a * variables.deltatime
    #TODO
    def gravitational_deformation(self)->float:
        _total_mass_on_top = 0
        v1 = pygame.math.Vector2(self.x, self.y)
        # Säteet
        r1 = self.radius

        # Välinen etäisyys
        for ball in variables.balls:
            if not ball.x == self.x and not ball.y == self.y:
                # Jos ei sama pallo niin jatkaa
                continue
            # Katotaan onko pallo yläällä ja osuuko se
            v2 = pygame.math.Vector2(ball.x, ball.y)
            r2 = ball.radius
            distance = v1.distance_to(v2)
            if ball.x-ball.radius <= self.x <= ball.x + ball.radius\
            and distance < r1 + r2 and distance > 0:
                _total_mass_on_top += ball.mass
        """
        Hooken laki:
            δ=km/(g+M)

            δ = Epämuodostuminen
            k = Jäykkyys
            m = Kappaleen massa
            g = Painovoima
            M = Muut massat

        Soikion epämuodostuma leveydellään = (säde * epämuodostuma) * 2
        """
        try:
            delta = (self.rigid * self.mass) / (variables.active_data["gravity"] + _total_mass_on_top)
            print(f'{self.rigid} * {self.mass} / {variables.active_data["gravity"] } = {delta} * {self.radius} | {delta*self.rigid * 2}')
            
            return delta * self.rigid
        except:
            # Jos painovoima on nolla niin crashaa
            return self.radius
    pass
#
#
#
# O-paneeli näytön oikeessa laidassa
class Secondary_Panel:
    def __init__(self) -> None:
        #
        # Leveys, korkes, x ja y
        # 300xKorkeus oikeassa nurkassa
        self.width = variables.secondary_panel_width - variables.secondary_panel_text_width
        self.height = variables.screen_dict["height"]
        self.x = variables.screen_dict["width"] - variables.secondary_panel_width
        self.y = 0
        self.panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.background_colour = (30,30,30)

        # Radionapit
        variables.radio_buttons = []
        _multiply = 1
        variables.radio_buttons.append(Radio_Button("Air resistance", self.x + 15, self.y + 10*_multiply)) 
        _multiply += 3
        variables.radio_buttons.append(Radio_Button("Ground friction", self.x + 15, self.y + 10*_multiply))
        _multiply += 3
        variables.radio_buttons.append(Radio_Button("Wind speed", self.x + 15, self.y + 10*_multiply))
        _multiply += 3
        variables.radio_buttons.append(Radio_Button("Active ceiling", self.x + 15, self.y + 10*_multiply))
        _multiply += 3
        variables.radio_buttons.append(Radio_Button("Ball collisions", self.x + 15, self.y + 10*_multiply))
        _multiply += 3
        variables.radio_buttons.append(Radio_Button("Advanced Ball physics", self.x + 15, self.y + 10*_multiply))
        _multiply += 2
        self.line_1_y_pos = _multiply # 1. viivan y

        # Inputti kentät
        variables.input_fields_1 = []
        _multiply += 1
        variables.input_fields_1.append(Text_Field(" Gravity", variables.active_data["gravity"], self.x + 5, self.y+10*_multiply, 100, 25, 9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Air density",variables.active_data["air_density"], self.x + 5, self.y+10*_multiply, 100, 25, 9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Ground friction",variables.active_data["ground_friction"], self.x + 5, self.y+10*_multiply, 100, 25,9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Wind speed (m/s)", variables.active_data["wind_speed"], self.x + 5, self.y+10*_multiply, 100, 25,9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Wind direction (degrees from middle)", variables.active_data["wind_direction"], self.x + 5, self.y+10*_multiply, 100, 25,9))
        _multiply += 3
        self.line_2_y_pos = _multiply # 2. viivan y

        # Napit lisää pallo, muokkaa palloa

        variables.form_button_row_1 = []
        _multiply += 1
        self.button_row_1_y = _multiply
        variables.form_button_row_1.append(Button("Add new ball", (150,150,150), (100,100,100), (0, 255, 102)))
        variables.form_button_row_1.append(Button("Edit cur. ball", (150,150,150), (100,100,100), (0, 255, 102)))
        _multiply_middle = _multiply # Editointikentille
        _multiply_middle_2 = _multiply # Lisäyskentille
        # Muokkaa nykyistä palloa
        # Editoi entisen pallon tietoja
        variables.input_fields_2 = []
        _multiply_middle += 5
        variables.input_fields_2.append(Text_Field("x-pos.", round(variables.balls[variables.active_ball_index].x, 1), self.x + 5, self.y+10*_multiply_middle,95,25,9))
        variables.input_fields_2.append(Text_Field(" y-pos.", round(variables.balls[variables.active_ball_index].y, 1), self.x + 10 + 100 + 75, self.y+10*_multiply_middle,100,25,9))
        _multiply_middle += 3
        variables.input_fields_2.append(Text_Field("radius", round(variables.balls[variables.active_ball_index].radius, 1), self.x + 5, self.y+10*_multiply_middle,95,25,9))
        variables.input_fields_2.append(Text_Field(" mass (kg)", round(variables.balls[variables.active_ball_index].mass, 1), self.x + 10 + 100 + 75, self.y+10*_multiply_middle,100,25,9))
        _multiply_middle += 3
        variables.input_fields_2.append(Text_Field("ver. vel.", round(variables.balls[variables.active_ball_index].vertical_velocity, 1), self.x + 5, self.y+10*_multiply_middle,95,25,9))
        variables.input_fields_2.append(Text_Field(" hor. vel.", round(variables.balls[variables.active_ball_index].horizontal_velocity, 1), self.x + 10 + 100 + 75, self.y+10*_multiply_middle,100,25,9))

        _multiply_middle += 3
        variables.input_fields_2.append(Text_Field("rigidness", round(variables.balls[variables.active_ball_index].rigid, 2), self.x + 5, self.y+10*_multiply_middle,95,25,9))
        variables.input_fields_2.append(Text_Field(" elasticity", round(variables.balls[variables.active_ball_index].elasticity, 2), self.x + 10 + 100 + 75, self.y+10*_multiply_middle,95,25,9))
                                                    
        _multiply_middle += 3
        variables.input_fields_2.append(Text_Field("Red", round(variables.balls[variables.active_ball_index].colour[0], 1), self.x + 5, self.y+10*_multiply_middle,50,25,4))
        variables.input_fields_2.append(Text_Field("Green", round(variables.balls[variables.active_ball_index].colour[1], 1), self.x + 5 + 10 + 50*2, self.y+10*_multiply_middle,50,25,4))
        variables.input_fields_2.append(Text_Field(" Blue", round(variables.balls[variables.active_ball_index].colour[2], 1), self.x + 5 + 50*4 + 25, self.y+10*_multiply_middle,50,25,4))

        # Poistonappi
        _multiply_middle += 3
        self.button_row_2_y = _multiply_middle
        variables.button_row_2 = []
        variables.button_row_2.append(Button("Delete", (150,150,150), (100,100,100), (0,255,102)))
        # variables.button_row_2.append(Button("Freeze", (150,150,150), (100,100,100), (0,255,102)))
        variables.button_row_2.append(Radio_Button("Freeze", 0, 0))
        variables.button_row_2.append(Button("Throw", (150,150,150), (100,100,100), (0,255,102)))

##############################################
        # Lisää uusi pallo
        # Editoi entisen pallon tietoja
        variables.input_fields_3 = []
        _multiply_middle_2 += 5
        variables.input_fields_3.append(Text_Field("x-pos.", round(variables.balls[variables.active_ball_index].x, 1), self.x + 5, self.y+10*_multiply_middle_2,95,25,9))
        variables.input_fields_3.append(Text_Field(" y-pos.", round(variables.balls[variables.active_ball_index].y, 1), self.x + 10 + 100 + 75, self.y+10*_multiply_middle_2,100,25,9))
        _multiply_middle_2 += 3
        variables.input_fields_3.append(Text_Field("radius", round(variables.balls[variables.active_ball_index].radius, 1), self.x + 5, self.y+10*_multiply_middle_2,95,25,9))
        variables.input_fields_3.append(Text_Field(" mass (kg)", round(variables.balls[variables.active_ball_index].mass, 1), self.x + 10 + 100 + 75, self.y+10*_multiply_middle_2,100,25,9))
        _multiply_middle_2 += 3
        variables.input_fields_3.append(Text_Field("ver. vel.", round(variables.balls[variables.active_ball_index].radius, 1), self.x + 5, self.y+10*_multiply_middle_2,95,25,9))
        variables.input_fields_3.append(Text_Field(" hor. vel.", round(variables.balls[variables.active_ball_index].mass, 1), self.x + 10 + 100 + 75, self.y+10*_multiply_middle_2,100,25,9))

        _multiply_middle_2 += 3
        variables.input_fields_3.append(Text_Field("rigidness", round(variables.balls[variables.active_ball_index].rigid, 2), self.x + 5, self.y+10*_multiply_middle_2,95,25,9))
        variables.input_fields_3.append(Text_Field(" elasticity", round(variables.balls[variables.active_ball_index].elasticity, 2), self.x + 10 + 100 + 75, self.y+10*_multiply_middle_2,95,25,9))
                                                         
        _multiply_middle_2 += 3
        variables.input_fields_3.append(Text_Field("Red", round(variables.balls[variables.active_ball_index].colour[0], 1), self.x + 5, self.y+10*_multiply_middle_2,50,25,4))
        variables.input_fields_3.append(Text_Field("Green", round(variables.balls[variables.active_ball_index].colour[1], 1), self.x + 5 + 10 + 50*2, self.y+10*_multiply_middle_2,50,25,4))
        variables.input_fields_3.append(Text_Field(" Blue", round(variables.balls[variables.active_ball_index].colour[2], 1), self.x + 5 + 50*4 + 25, self.y+10*_multiply_middle_2,50,25,4))

        # Lisöysnappi
        _multiply_middle_2 += 3
        self.edit_row_3_y = _multiply_middle_2
        variables.edit_row_3 = []
        variables.edit_row_3.append(Text_Field(" Amount", variables.new_ball_default_amount, self.x + 18, self.y +10*(_multiply_middle_2 + 1), 50,25,4))
        variables.edit_row_3.append(Button("Add new ball(s)", (150,150,150), (100,100,100), (0,255,102)))



        # Tekstipaneeli
        self.text_panel_rect = pygame.Rect(variables.screen_dict["width"]-variables.secondary_panel_text_width,0,variables.secondary_panel_text_width,variables.screen_dict["height"])
        # tekstit
        self.text_array = []
        self.text_line_x = variables.screen_dict["width"] - variables.secondary_panel_text_width
        self.text_array.append(Text_Line(" planet:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" paused:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" mouse pos:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" balls:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" fps:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" base gravity:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" base air density:", self.text_line_x, 0))
        self.text_array.append(Text_Line("", self.text_line_x, 0))
        self.text_array.append(Text_Line("-------------------------------", self.text_line_x, 0))
        self.text_array.append(Text_Line("", self.text_line_x, 0))
        self.text_array.append(Text_Line(" current ball stats:", self.text_line_x, 0))
        self.text_array.append(Text_Line("", self.text_line_x, 0))
        self.text_array.append(Text_Line(" gravity experienced:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" wind experienced:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" drag experienced:", self.text_line_x, 0))

        pass
    def draw(self):
        #
        # Taustan piirto
        pygame.draw.rect(variables.SCREEN, self.background_colour, self.panel_rect)
        #
        # Omat eventit omille napeille sun muille tekstikentille


        # Radionapit
        for button in variables.radio_buttons:
            is_hovered = button.rect.collidepoint(variables.mouse[0], variables.mouse[1])
            if button.active:
                is_hovered = True
            button.draw(is_hovered)
            pass
        # Viiva alle
        pygame.draw.line(variables.SCREEN, (150,150,150), (self.x, self.y + 10*self.line_1_y_pos), (variables.screen_dict["width"], self.y + 10*self.line_1_y_pos), 2)
        # Tekstikentät
        for textfield in variables.input_fields_1:
            textfield.draw()
        # Viiva alle
        pygame.draw.line(variables.SCREEN, (150,150,150), (self.x, self.y + 10*self.line_2_y_pos), (variables.screen_dict["width"], self.y + 10*self.line_2_y_pos), 2)
        # Valinta napit:
        # Lisää uusi pallo, muokkaa olemassa olevaa palloa.
        for i, button in enumerate(variables.form_button_row_1):
            button.y = self.y + (10 * self.button_row_1_y)
            button.x = (self.x + 5) + (100 + 75) * i
            is_hovered = button.rect.collidepoint(variables.mouse[0], variables.mouse[1])

            # Aktivointiväri ja reuna vihreeksi
            #0, 255, 102
            if variables.active_add_new_ball and button.text == "Add new ball":
                pygame.draw.rect(variables.SCREEN, (0, 255, 102), button.rect, 2)
                is_hovered = True
            elif variables.active_edit_current_ball and button.text == "Edit cur. ball":
                pygame.draw.rect(variables.SCREEN, (0, 255, 102), button.rect, 2)
                is_hovered = True
            button.draw(is_hovered)
            if variables.active_add_new_ball and button.text == "Add new ball":
                pygame.draw.rect(variables.SCREEN, (0, 255, 102), button.rect, 1)
            elif variables.active_edit_current_ball and button.text == "Edit cur. ball":
                pygame.draw.rect(variables.SCREEN, (0, 255, 102), button.rect, 1)
            pass
        pass
        
        # Piirtää sen paneelin alle, joka on napeilla päällä
        if variables.active_add_new_ball:
            # Uusi pallo
            # Input
            for input_field in variables.input_fields_3:
                if not input_field.active:
                    input_field.text = self.update_edit_fields_new_ball(input_field)
                input_field.draw()

            # Lisää ja määrä
            for item in variables.edit_row_3:
                # Inputti
                try:
                    if item.info_str == " Amount":
                        item.draw()
                except:
                    pass
                # Nappi
                try:
                    if item.text == "Add new ball(s)":
                        item.x = self.x +18 + (150)
                        item.y = self.y +10* self.edit_row_3_y
                        is_hovered = item.rect.collidepoint(variables.mouse[0], variables.mouse[1])
                        item.draw(is_hovered)
                except:
                    pass
            pass
        elif variables.active_edit_current_ball:
            for textfield in variables.input_fields_2:
                if not textfield.active:
                    textfield.text = self.update_edit_fields(textfield)
                textfield.draw()


            # Piirtää napit 
            for i, button in enumerate(variables.button_row_2):
                # Radionapille eri korkeus
                if button.text == "Freeze":
                    # Bugaa muuten, ei päivity active
                    try:
                        button.active = variables.balls[variables.active_ball_index].freeze
                    except:
                        # out of range
                        pass
                    button.y = self.y + 10 * (self.button_row_2_y + 2)
                else:
                    button.y = self.y + 10 * self.button_row_2_y
                button.x = self.x + 5 + (100 * i) 
                button.make_rect()
                is_hovered = button.rect.collidepoint(variables.mouse[0], variables.mouse[1])
                if button.active:
                    is_hovered = True
                button.draw(is_hovered)
            pass
        

        # Tekstipaneelin pohja
        pygame.draw.rect(variables.SCREEN, self.background_colour, self.text_panel_rect)
        # Viiva
        pygame.draw.line(variables.SCREEN, (150,150,150), (self.text_panel_rect.x, 0), (self.text_panel_rect.x, variables.screen_dict["height"]))

        # Teksti
        for i, line in enumerate(self.text_array):
            line.y = self.y + 3 + (i * 16)
            line.draw()
        pass

    # Päivittää pallonmuokkaajan tietoja reaaliaikaan
    def update_edit_fields(self, sender):
        _return_var = None
        try:
            match sender.info_str:
                case "x-pos.":
                    _return_var = int(round(variables.balls[variables.active_ball_index].x,0))
                    pass
                case " y-pos.":
                    _return_var = int(round(variables.balls[variables.active_ball_index].y,0))
                    pass
                case "radius":
                    _return_var = int(round(variables.balls[variables.active_ball_index].radius,0))
                    pass
                case " mass (kg)":
                    _return_var = float(round(variables.balls[variables.active_ball_index].mass,2))
                    pass
                case "ver. vel.":
                    _return_var = int(round(variables.balls[variables.active_ball_index].vertical_velocity,0))
                    pass
                case " hor. vel.":
                    _return_var = int(round(variables.balls[variables.active_ball_index].horizontal_velocity,0))
                case "rigidness":
                    _return_var = float(round(variables.balls[variables.active_ball_index].rigid,2))
                case " elasticity":
                    _return_var = float(round(variables.balls[variables.active_ball_index].elasticity,2))
                case "Red":
                    _return_var = int(round(variables.balls[variables.active_ball_index].colour[0],0))
                case "Green":
                    _return_var = int(round(variables.balls[variables.active_ball_index].colour[1],0))
                case " Blue":
                    _return_var = int(round(variables.balls[variables.active_ball_index].colour[2],0))
                    pass
        except:
            # print("list index out of range:", IndexError)
            pass
        return str(_return_var)
    
    # Päivittää pallonlisääjän tiedot
    def update_edit_fields_new_ball(self, sender) -> str:
        _return_var = None
        try:
            match sender.info_str:
                case "x-pos.":
                    _return_var = int(round(variables.new_ball_default["x"],0))
                    pass
                case " y-pos.":
                    _return_var = int(round(variables.new_ball_default["y"],0))
                    pass
                case "radius":
                    _return_var = int(round(variables.new_ball_default["radius"],0))
                    pass
                case " mass (kg)":
                    _return_var = float(round(variables.new_ball_default["mass"],2))
                    pass
                case "ver. vel.":
                    _return_var = int(round(variables.new_ball_default["vertical_velocity"],0))
                    pass
                case " hor. vel.":
                    _return_var = int(round(variables.new_ball_default["horizontal_velocity"],0))
                case "rigidness":
                    _return_var = float(round(variables.new_ball_default["rigidness"],2))
                case " elasticity":
                    _return_var = float(round(variables.new_ball_default["elasticity"],2))
                case "Red":
                    _return_var = int(round(variables.new_ball_default["red"],0))
                case "Green":
                    _return_var = int(round(variables.new_ball_default["green"],0))
                case " Blue":
                    _return_var = int(round(variables.new_ball_default["blue"],0))
                    pass
        except IndexError:
            # print("list index out of range:", IndexError)
            pass
        return str(_return_var)
    pass