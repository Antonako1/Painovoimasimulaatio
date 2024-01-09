import pygame, variables
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
# Pelin pallo joka pomppii
#
class Ball:
    def __init__(self, x:int, y:int, radius:int, mass:int, velocity:int, colour:tuple) -> None:
        self.radius = radius
        self.x = x
        self.y = y + radius # Yläkulmaan
        self.colour = colour
        self.mass = mass
        self.velocity = velocity
        pass
    def move(self) -> None:

        pass
    def draw(self):
        self.move()
        pygame.draw.circle(variables.SCREEN, self.colour, (self.x, self.y), self.radius)
        pass