import pygame, variables, math, random
#
#
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
        variables.SCREEN.blit(_text_surface, (self.x, self.y + (self.height / 4)))
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

        _info_x = self.x + self.input_field_rect.width + 10
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

        variables.SCREEN.blit(_info_txt_surface, (_info_x, self.y))
        pass
    def update_variables(self):
        try:
            # Tallentaa tiedot
            match self.info_str:
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
                case " Wind resistance":
                    if float(self.text) <= 0.00001:
                        self.text = "0"
                    variables.active_data["wind_resistance"] = float(self.text)
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
        self.colour_in = (100,100,255)
        # Sisäympyrä 2
        self.radius_in_2 = self.radius_in -4

        self.x = x
        self.y = y

        self.text = text
        self.text_colour = (0, 255, 102)

        self.make_rect()
        self.update_variables("out")
        pass
    def draw(self, is_hovered):
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
                case "Wind resistance":
                    self.active = variables.active_wind_resistance
                case "Active ceiling":
                    self.active = variables.active_ceiling
        elif case == "in":
            match self.text:
                case "Air resistance":
                    variables.active_air_resistance = self.active
                case "Ground friction":
                    variables.active_ground_friction = self.active
                case "Wind resistance":
                    variables.active_wind_resistance = self.active
                case "Active ceiling":
                    variables.active_ceiling = self.active
        
        
        pass
    pass
# Pelin pallo joka pomppii
# TODO Wind resistance
class Ball:
    # X
    # Y
    # Säde
    # Massa
    # Vertikaalinen kiihtyvyys
    # Horisonttaali kiihtyvyys
    # Maan kitka
    # Joustavuus
    # Pallon väri
    def __init__(self, x:int, y:int, radius:int, mass:int, vertical_velocity:int, horizontal_velocity:int, elasticity:float , colour:tuple) -> None:
        self.radius = radius
        self.x = x
        self.y = y + radius # Yläkulmaan
        self.colour = colour
        self.mass = mass
        self.vertical_velocity = vertical_velocity
        self.horizontal_velocity = horizontal_velocity
        self.elasticity = elasticity
        pass
    def draw(self):
        # Jos pausella, ei liikuteta
        if not variables.active_pause:
            self.move()
        pygame.draw.circle(variables.SCREEN, self.colour, (self.x, self.y), self.radius)
        pass
    def move(self) -> None:
        # Kiihtyvyys lisätään x- ja y-akseleihin        
        self.y += self.vertical_velocity * variables.deltatime
        self.x += self.horizontal_velocity * variables.deltatime

        # Y-akseli pomppaus, alas ja ylös
        if self.y >= variables.screen_dict["height"] - self.radius \
        or variables.active_ceiling and self.y <= 0 + self.radius:
            # Pallo menee ylös, se jää sinne.
            # Oli väärte päin, sen takii "not"
            self.y = variables.screen_dict["height"] - self.radius if not self.y <= 0 + self.radius else 0 + self.radius
            # Kiihtyvyys kääntyy ja se kerrotaan pallon joustavuudella
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
            # Kiihtyvyys kääntyy ja se kerrotaan joustavuudella
            self.horizontal_velocity = -(self.horizontal_velocity * self.elasticity)
            pass

        # Lisätään painovoiman ja ilmanvastuksen vaikutus
        _velocity_gravitational_effect = variables.active_data["gravity"]
        # Lisätään ilman vastus
        if variables.active_air_resistance:
            _velocity_gravitational_effect -= self.gravitation_drag()
        self.vertical_velocity += _velocity_gravitational_effect

        # Tuulen vastus

        # Lisätään maan kitka jos se koskettaa maan pintaa ja toggle on päällä
        if self.y >= variables.screen_dict["height"] - self.radius and variables.active_ground_friction:
            self.horizontal_velocity *= variables.active_data["ground_friction"]
            pass

        pass

    def gravitation_drag(self) -> float:
        """
        Laskee painovoiman vastuksen

        Termit:
            ρ = Ilman tiheys
            Cd = Ilmanvastuskerroin
            A = Pinta-ala
            v = Kiihtyvyys
            F_gravity = Painovoiman aiheuttama voima
            F_drag = Voiman vastus liikkeen vastakkaiseen suuntaan
            F_net = F_gravityn ja F_dragin netto

        Kaava:
        F_drag=1/2ρCdAv^2

        F_gravity=m⋅g

        F_net=F_gravity-F_drag

        a=m/F_net
        """

        # Pinta-ala
        area = (math.pi*self.radius**2)
        drag_coefficient = 0.47 # Pallon ilmanvastuskerroin
        # Voiman vastus
        f_drag = (1/2) * variables.active_data["air_density"] * drag_coefficient * area * self.vertical_velocity

        # Painovoiman voima | N
        f_gravity = self.mass * variables.active_data["gravity"]

        # Netto voima
        f_net = f_gravity - f_drag
        # print(f'{f_gravity} - {f_drag} = {f_net}')

        # Painovoiman tuottama kiihtyminen ilmanvastus mukaan lukien
        a = self.mass / f_net
        # print(f'{self.mass} / {f_net} = {a} \n')
        return a * variables.deltatime
    pass
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
        variables.radio_buttons.append(Radio_Button("Wind resistance", self.x + 15, self.y + 10*_multiply))
        _multiply += 3
        variables.radio_buttons.append(Radio_Button("Active ceiling", self.x + 15, self.y + 10*_multiply))
        _multiply += 2
        self.line_1_y_pos = _multiply # 1. viivan y

        # Inputti kentät
        variables.input_fields_1 = []
        _multiply += 1
        variables.input_fields_1.append(Text_Field(" Gravity asdsadsdaasdasdasdsadsad", variables.active_data["gravity"], self.x + 15, self.y+10*_multiply, 100, 25, 9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Air density",variables.active_data["air_density"], self.x + 15, self.y+10*_multiply, 100, 25, 9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Ground friction",variables.active_data["ground_friction"], self.x + 15, self.y+10*_multiply, 100, 25,9))
        _multiply += 3
        variables.input_fields_1.append(Text_Field(" Wind resistance", variables.active_data["wind_resistance"], self.x + 15, self.y+10*_multiply, 100, 25,9))
        _multiply += 3
        self.line_2_y_pos = _multiply # 2. viivan y

        # Napit lisää pallo, muokkaa palloa
        variables.form_button_row_1 = []
        _multiply += 2
        self.button_row_1_y = _multiply
        variables.form_button_row_1.append(Button("Add new ball", (150,150,150), (100,100,100), (0, 255, 102)))
        variables.form_button_row_1.append(Button("Edit cur. ball", (150,150,150), (100,100,100), (0, 255, 102)))

        # Editoi entisen pallon tietoja
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
            button.x = (self.x + 10) + (140 * i)
            is_hovered = button.rect.collidepoint(variables.mouse[0], variables.mouse[1])
            button.draw(is_hovered)
            pass
        pass
    pass