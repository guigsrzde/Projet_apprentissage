from modele_propagation import SIRD_model
import numpy as np
from numpy.random import randint
from math import sqrt
from numpy import tanh as th

# Parameters
T = 365  # Total time in days
dt = 0.1  # Time step

# Number of time steps
N = int(T / dt)

class City:
    def __init__(self, population, coord_x, coord_y, name, id, healing_factor, propagation_factor, mortality_factor, infected=False):
        """
        Initialises a city and fills its parameters.
        """
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.pop = population
        a = []
        if infected : a = [1/self.pop] 
        else:  a = [0]
        self.infected = a
        self.healthy = [1-self.infected[0]]
        self.dead = [0]
        self.recovered = [0]

        # Factors to compute the parameters
        self.healing_fac = healing_factor
        self.prop_fac = propagation_factor
        self.mortal_fac = mortality_factor

        # Parameters of the city 
        self.healing_rate =  # SIRD Model coeff
        self.propagation_rate = 0
        self.mortality_rate = 0

        self.x = coord_x
        self.y = coord_y
        self.name = name # string
        self.id = id # int

        self.disease_inertia = 1 # determines how fast time should go
    
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
            self.healthy[-1] = 1 - (self.infected[-1] + self.recovered[-1] + self.dead[-1])
        return
    
    def propagate_to(self, town):
        """
        model of propagation to new cities.
        """
        p = randint(0,self.pop)
        if p<= 100*self.infected[-1]*self.pop/self.distance(town) and (not town.is_infected()):
            town.infect()
            return True
        return False
    
    def update_inertia(self, time1=0, time2=0):
        """
        computes the inertia of the virus between two instants of the game
        """
        norm_derivative = sqrt((self.healthy[time2]-self.healthy[time1])**2+(self.infected[time2]-self.infected[time1])**2
                               +(self.dead[time2]-self.dead[time1])**2 + (self.recovered[time2]-self.recovered[time1])**2)
        #we always have at least 2 values in the lists because of the initialisation + 1 loop, value between 0 and 2
        self.disease_inertia = max(min(1000,10*norm_derivative/(0.3-norm_derivative)),1)
        return
    
    def propagation_tick(self, nb_ticks, timeupdate=True):
        """
        Implements one time tick of propagation in our model with Euler's method
        """
        newdt = dt/self.disease_inertia
        for _ in range(nb_ticks):
            h, i, r, d = SIRD_model(self.healthy, self.infected, self.recovered, self.dead, self.healing_rate, self.propagation_rate, self.mortality_rate, dt = newdt)
            self.healthy.append(h), self.infected.append(i), self.recovered.append(r), self.dead.append(d)
            if timeupdate: 
                self.update_inertia(-1,-11)
        return
    
    def update_params(self, virus):
        """
        Updates the constants for the SIRD model we used
        """
        self.transmission_rate = self.prop_fac*th((virus.propagation)/10)
        self.healing_rate = 1/(self.healing_fac*th((virus.length_infection)/10))
        self.mortality_rate = self.mortal_fac*th(virus.mortality_symptoms/10)
        return


def global_propagation(list_cities, nbticks=10):
    """
    Function that allows the virus to propagate between cities
    """
    newly_infected_cities_id = []
    for _ in range(nbticks):
        for town1 in list_cities:
            for town2 in list_cities:
                if(town1.propagate_to(town2)):
                    newly_infected_cities_id.append(town2.id)
    message = f"The virus has arrived to these cities: {[str(list_cities[i].name) for i in newly_infected_cities_id]}"
    return message
