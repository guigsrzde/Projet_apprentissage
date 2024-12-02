class Ville:
    def __init__(self, population, coord_x, coord_y):
        self.pop = population
        self.infected = 0  # number between 0 and 1 that gives the proportion of infected ppl
        self.x = coord_x
        self.y = coord_y