from random import randint
from modele_propgation import SIRD_model
import numpy as np

# Parameters
T = 365  # Total time in days
dt = 0.1  # Time step

# Number of time steps
N = int(T / dt)

class City:
    def __init__(self, population, coord_x, coord_y, name, id, infected=False):
        """
        Initialises a city and fills its parameters.
        """
        self.pop = population
        a = []
        if infected : a = [1/self.pop] 
        else:  a = [0]
        self.infected = a
        self.healthy = [1-self.infected[0]]
        self.dead = [0]
        self.recovered = [0]

        self.x = coord_x
        self.y = coord_y
        self.name = name # string
        self.id = id # int
    
    @classmethod
    def random(cls, max_x, max_y, id):
        """
        initialises a random city given maximum x and y coordinates
        """
        x = randint(0,max_x)
        y = randint(0,max_y)
        name = chr(ord('A') + randint(0,25))
        for i in range(randint(2,8)):
            name += chr(ord('a') + randint(0,25))
        population = randint(50000, 1000000)
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
        return self.infected[-1]>0
    
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
        p = randint(0,self.pop)
        if p<= self.infected[-1]*self.healthy[-1]*self.pop and (not town.is_infected()):
            town.infect()
            return True
        return False
    
    def propagation_tick(self, disease, nb_ticks):
        """
        Implements one time tick of propagation in our model with Euler's method
        """
        for _ in range(nb_ticks):
            h, i, r, d = SIRD_model(self.healthy, self.infected, self.recovered, self.dead, disease)
            self.healthy.append(h), self.infected.append(i), self.recovered.append(r), self.dead.append(d)
        return

def global_propagation(list_cities):
    """
    Function that allows the virus to propagate between cities
    """
    newly_infected_cities_id = []
    for town1 in list_cities:
        for town2 in list_cities:
            if(town1.propagate_to(town2)):
                newly_infected_cities_id.append(town2.id)
    message = f"The virus has arrived to these cities: {[str(list_cities[i].name) for i in newly_infected_cities_id]}"
    return message
