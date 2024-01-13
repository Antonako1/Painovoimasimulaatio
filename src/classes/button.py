import pygame, variables
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
