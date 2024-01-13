import pygame, variables
class Radio_Button:
    def __init__(self, text, x, y) -> None:
        # Ulkoympyrä
        self.radius_out = 10 # Fontin ko'on mukaan
        self.colour_out = (150,150,150)
        # Sisäympyrä
        self.radius_in = self.radius_out -2
        # self.colour_in = (100,100,255)
        self.colour_in = (255,0,0)
        self.colour_in_hover = (155,0,0)
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
        if self.active:
            pygame.draw.circle(variables.SCREEN,(self.colour_in), (self.x, self.y), self.radius_in)
            pygame.draw.circle(variables.SCREEN,(self.colour_out), (self.x, self.y), self.radius_in_2)
        elif is_hovered:
            pygame.draw.circle(variables.SCREEN,(self.colour_in_hover), (self.x, self.y), self.radius_in)
            pygame.draw.circle(variables.SCREEN,(self.colour_out), (self.x, self.y), self.radius_in_2)


        # Teksti
        _text_surface = variables.font.render(self.text, True, self.text_colour)
        variables.SCREEN.blit(_text_surface, (self.x + 16, self.y - self.radius_out))

        pass
    def make_rect(self):
        self.rect = pygame.Rect(self.x - self.radius_out, self.y - self.radius_out, self.radius_out * 2, self.radius_out * 2)
        pass
    def update_variables(self, case):
        # Tuleeko variablesista "ulos" tai sinne "sisään"
        if case == "out":
            match self.text:
                case "Zero gravity":
                    self.active = variables.active_zero_g
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
                case "Zero gravity":
                    variables.active_zero_g = self.active
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
