import random
import numpy as np

class City:
    def __init__(self, population, coord_x, coord_y, name, id, infected=False):
        """
        Initialises a city and fills its parameters.
        """
        self.pop = population
        if infected:
            self.healthy = np.array([1-1/population])
        else:
            self.healthy = np.array([1.0])
        self.infected = np.array([float(1 - self.healthy[0])])
        self.dead = np.array([float(0)])
        self.recovered = np.array([float(0)])
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
        """
        initialises a random city given maximum x and y coordinates
        """
        x = random.randint(0,max_x)
        y = random.randint(0,max_y)
        name = chr(ord('A') + random.randint(0,25))
        for i in range(random.randint(2,8)):
            name += chr(ord('a') + random.randint(0,25))
        population = random.randint(50000, 1000000)
        return cls(population, x, y, name, id)
    
    def add_values(self, new_recovered, new_healthy, new_infected):
        """
        updates the current status of the population in the city with new values
        """
        new_dead=1-new_recovered-new_healthy-new_infected
        self.recovered = np.append(self.recovered, new_recovered)
        self.healthy = np.append(self.healthy, new_healthy)
        self.infected = np.append(self.infected, new_infected)
        self.dead = np.append(self.dead, new_dead)
    
    def distance(self, town):
        """
        returns the distance between two cities
        """
        return max(1,int(((self.x-town.x)**2+(self.y-town.y)**2)**(1/2)))

    def is_infected(self):
        """
        returns a bool that tells us if someone has the virus in the city
        """
        return self.infected>0
    
    def infect(self):
        """
        infects a citizen of a city if the city has not yet been infected
        """
        if self.is_infected()==False:
            self.infected[-1] = 1/self.pop
            self.healthy[-1] = 1 - self.infected[-1]
        return
    
    def propagate_to(self, town):
        """
        model of propagation to new cities.
        """
        p = 100/self.distance(town)*random.randint(0,self.pop)/self.pop
        if p<= self.infected[-1]*self.pop and (not town.is_infected()):
            town.infect()
            return True
        return False
    
    def maj_param_propagation(self, disease):
        """
        update the model parameters in function of how the disease has evolved
        """
        #TODO
        return
    
    def propagation_tick(self, disease):
        """
        Implements one time tick of propagation in our model with Euler's method
        """
        #TODO
        return
