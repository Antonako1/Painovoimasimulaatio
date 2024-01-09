import pygame
import sys, importlib
import variables
from classes import Ball


class Main_Game:
    def __init__(self) -> None:
        # Importtaa oikean datan importlibillä
        try:
            data_name = f"planet_data.{variables.active_planet}" # Datan nimi
            data_dict = importlib.import_module(data_name) # Importtaa datan 
            self.planet_data = data_dict.data.copy() # Tekee siitä kopion
        except ImportError: # Jos importti ei toimi
            # Virhe viesti ja ohjelmasta poistuminen
            print(f"Error: Could not import planet data for {variables.active_planet}")
            pygame.quit()
            sys.exit()

        print(self.planet_data["gravity"])
        # Sekunteihin
        self.seconds = 0
        self.start_ticks = pygame.time.get_ticks()

        # deltatime
        self.dt = 0
        self.prev_tick = 0

        # Palloille lista
        self.balls = []
        
        # Alotuspallo
        self.balls.append(Ball(
            variables.screen_dict["width"] / 2, 0,
              25, 500, 10, # Radius, mass, velocity
                (255,0,0)))
        pass
    def run(self):
        #
        # Nykyinen tikki
        _cur_tick = pygame.time.get_ticks()
        #
        # Sekunnit
        self.seconds = (_cur_tick - self.start_ticks) / 1000.0
        #
        # deltatime sekunneissa
        self.dt = (_cur_tick - self.prev_tick) / 1000.0
        self.prev_tick = _cur_tick
        #
        # Tausta
        variables.SCREEN.fill((100, 100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Pallojen piirto
        for ball in self.balls:
            ball.draw() # Laskelmat tapahtuu draw funktiossa itestään

        # Näytön päivitys
        pygame.display.flip()
        variables.CLOCK.tick(60)



        

