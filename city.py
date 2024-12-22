import random

class City:
    def __init__(self, population, coord_x, coord_y, name, id):
        self.pop = population
        self.healthy = 1-1/population # number between 0 and 1 that gives the proportion of healthy ppl
        self.infected = 1 - self.healthy  
        self.dead = 0
        self.recovered = 0
        self.x = coord_x
        self.y = coord_y
        self.name = name # string
        self.id = id # int
        #params for the propagation model
        self.L = 10 #average infection length
        self.M = 0.1 #mortality rate
        self.B = 1 #propagation factor
    
    @classmethod
    def random(cls, max_x, max_y, id):
        x = random.randint(0,max_x)
        y = random.randint(0,max_y)
        name = chr(ord('A') + random.randint(0,25))
        for i in range(random.randint(2,8)):
            name += chr(ord('a') + random.randint(0,25))
        population = random.randint(50000, 1000000)
        return cls(population, x, y, name, id)
    
    def maj_param_propagation(self, disease):
        #update B,L and M in function of how the disease has evolved
        return
    
    def propagation_tick(self):
        #implementation of euler's method
        return
