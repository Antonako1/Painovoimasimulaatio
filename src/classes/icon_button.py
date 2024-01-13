import pygame, variables
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
