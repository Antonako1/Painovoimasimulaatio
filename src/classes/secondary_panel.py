import pygame, variables
from classes.button import Button
from classes.radio_button import Radio_Button
from classes.text_field import Text_Field
from classes.text_line import Text_Line
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
        _multiply = 1 # Y-akselin kerroin jolla saadaan kaikki hienosti allekkain
        variables.radio_buttons.append(Radio_Button("Zero gravity", self.x + 15, self.y + 10*_multiply)) 
        _multiply += 3
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
        # variables.input_fields_1.append(Text_Field(" Gravity", variables.active_data["gravity"], self.x + 5, self.y+10*_multiply, 100, 25, 9))
        # _multiply += 3
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
        self.text_array.append(Text_Line(" planet mass:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" planet radius:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" paused:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" mouse pos:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" balls:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" fps:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" base gravity:", self.text_line_x, 0))
        self.text_array.append(Text_Line(" base air density:", self.text_line_x, 0))
        self.text_array.append(Text_Line("", self.text_line_x, 0))
        self.text_array.append(Text_Line("-------------------------------", self.text_line_x, 0))
        self.text_array.append(Text_Line("", self.text_line_x, 0))
        self.text_array.append(Text_Line(" current stats:", self.text_line_x, 0))
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
                    # Pitää laittaa koska tää lista sisältää kahta eri luokkaa joilla on eri muuttujia
                    pass
                # Nappi
                try:
                    if item.text == "Add new ball(s)":
                        item.x = self.x +18 + (150)
                        item.y = self.y +10* self.edit_row_3_y
                        is_hovered = item.rect.collidepoint(variables.mouse[0], variables.mouse[1])
                        item.draw(is_hovered)
                except:
                    # Pitää laittaa koska tää lista sisältää kahta eri luokkaa joilla on eri muuttujia
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
