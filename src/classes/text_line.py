import pygame, variables
class Text_Line:
    def __init__(self, text, x, y) -> None:
        self.text = text
        self.value = ""
        self.x = x
        self.y = y
        self.text_animation = 0 # substring index
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
            case " planet radius:":
                self.value = f" {variables.original_data['radius']} km"
            case " planet mass:":
                self.value = f" {variables.original_data['mass']} kg"
            case " wind experienced:":
                self.value = f" {variables.wind_experienced}"
            case " gravity experienced:":
                self.value = f" {variables.gravity_experienced}"
            case " drag experienced:":
                self.value = f" {variables.drag_experienced}"
            case " Expected g-forces:":
                self.value = f" {variables.custom_planet_g}g"
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
