class Ville:
    def __init__(self, population, coord_x, coord_y, name, id):
        self.pop = population
        self.infected = 0  # number between 0 and 1 that gives the proportion of infected ppl
        self.mort = 0
        self.x = coord_x
        self.y = coord_y
        self.name = name # string
        self.id = id # int
