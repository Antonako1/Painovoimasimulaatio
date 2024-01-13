import variables, pygame, math
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
        self.hit = False
        pass
    
    def draw(self):
        # Jos pausella, ei liikuteta
        if not variables.active_pause and not self.freeze:
            self.move()

        _ball_colour = (self.colour[0], self.colour[1], self.colour[2])
        
        # Piirretään pallo tai soikio
        # Jos advanced päällä sekä rigid yli 1
        if variables.active_advanced_ball and self.rigid < 1:
            self.deformation = self.gravitational_deformation()
            if self.deformation > 1: # Jos menee yli yhen niin pallo on korkeempi kun leveempi
                self.deformation = 1
            y_compenstation = self.radius * self.deformation * 2 - self.radius # Paljon y:ssä pitää mennä alaspäin että pallon näyttää olevan maan tasalla

            # Soikio piirretään. x=keskikohta
            pygame.draw.ellipse(variables.SCREEN, _ball_colour, (self.x - self.radius, self.y - y_compenstation, 2 * self.radius, self.radius * self.deformation * 2))
        else:
            # Pelkkä pallo piirretään
            pygame.draw.circle(variables.SCREEN, _ball_colour, (self.x, self.y), self.radius)
        pass

    def move(self) -> None:
        # 3d, pallo
        if variables.active_advanced_ball:
            self.drag_coefficient = 0.47 # Pallon ilmanvastuskerroin
        #2d, ympyrä
        else:
            self.drag_coefficient = 1.17 # Ympyrän ilmanvastuskerroin
        # Pinta-ala
        self.area = (math.pi*self.radius**2)

        # Nopeus lisätään x- ja y-akseleihin        
        self.y += self.vertical_velocity * variables.deltatime
        self.x += self.horizontal_velocity * variables.deltatime

        # Tuulen vaikutus lisätään tai poistetaan
        variables.wind_experienced = 0
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
            Vwind_x = Vwind * math.cos(math.radians(Owind-90)) # Heittää oudosti
            Vwind_y = Vwind * math.sin(math.radians(Owind+90)) # Heittää oudosti

            Vobject_x = self.horizontal_velocity
            Vobject_y = self.vertical_velocity

            v = 1
            try:
                v = math.sqrt((Vobject_x - Vwind_x)**2 + (Vobject_y - Vwind_y)**2)
            except:
                v = 1
                pass

            Fwind = 0.5 * self.drag_coefficient * self.area * variables.active_data["air_density"] * v**2

            Awind = Fwind / (self.mass * 5000)  # Kiloina

            # Tuulen vaikutus
            wind_influence = 0.00001 # Ei toimi ilman tätä.

            ratio_x = (Vobject_x - Vwind_x) / v
            ratio_y = (Vobject_y - Vwind_y) / v
            
            self.horizontal_velocity += ratio_x * Awind * wind_influence
            self.vertical_velocity -= ratio_y * Awind * wind_influence

            # Paljon tuulta pallo saa yhteensä
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
        _velocity_gravitational_effect = 0
        self.gravitational_acceleration = 0
        if not variables.active_zero_g:
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
            self.gravitational_acceleration = gravitational_force / self.mass
            # Lopullinen muuttuja
            _velocity_gravitational_effect = self.gravitational_acceleration

        # Lisätään ilman vastus
        variables.drag_experienced = 0
        self.air_resistance = 0
        if variables.active_air_resistance:
            drag = self.gravitation_drag()
            self.air_resistance = drag
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

        # if self.hit:
        #     self.horizontal_velocity *= self.elasticity
        #     self.vertical_velocity *= self.elasticity
        #     self.hit = False
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
        f_drag = 0
        try:
            f_drag = ((1/2) * variables.active_data["air_density"] * self.drag_coefficient * self.area) * (self.vertical_velocity**2)
        except:
            # Liian iso luku
            f_drag = 1
        # return f_drag / self.mass # ?
        # Painovoiman voima | N
        # f_gravity = (self.mass / 1000) * variables.active_data["gravity"]
        f_gravity = (self.mass / 1000) * self.gravitational_acceleration

        # Netto voima
        f_net = f_gravity - f_drag

        # Painovoiman tuottama kiihtyminen ilmanvastus mukaan lukien
        a = self.mass / f_net
        return a * variables.deltatime
    
    def gravitational_deformation(self)->float:
        _total_mass_on_top = 0
        # Välinen etäisyys
        for ball in variables.balls:
            if not ball == self:
                # Katotaan onko pallo yläällä ja osuuko se
                if (ball.x-ball.radius <= self.x <= ball.x + ball.radius) and (self.y > ball.y or variables.active_zero_g):
                    _total_mass_on_top += ball.mass
        """
        Hooken laki:
            δ = k * m / (g + M)

            δ = Epämuodostuminen
            k = Jäykkyys
            m = Kappaleen massa
            g = Painovoima
            M = Muut massat

        Soikion epämuodostuma leveydellään = (säde * epämuodostuma) * 2
        """
        try:

            other_masses = (_total_mass_on_top * 7)
            if not variables.active_zero_g: # ei painovoimaa, niin se ei voi vaikuttaa 
                other_masses += self.gravitational_acceleration

            delta = (self.rigid * (self.mass * 10 * self.rigid)) / (other_masses)
            
            return delta / self.rigid
        except:
            # Jos painovoima on nolla niin crashaa
            return self.radius
    pass
