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
    def __init__(self, population, coord_x, coord_y, name, id, healing_factor, propagation_factor, mortality_factor, vaccination_prop, infected=False):
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

        self.first_infection_turn = None

        # Factors to compute the parameters
        self.healing_fac = healing_factor
        self.prop_fac = propagation_factor
        self.mortal_fac = mortality_factor

        # Parameters of the city 
        self.healing_rate = 0 # SIRD Model coeff
        self.propagation_rate = 0
        self.mortality_rate = 0

        self.vaccination_prop = vaccination_prop
        self.lockdown = False
        self.lockdown_threshold = 0.5  
        self.lockdown_effectiveness = 0.7  # Reduces 70% of the propagation inside the city
        self.lockdown_history = [False]

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
        return cls(population, x, y, name, id, randint(50,70), randint(40,60)/100, randint(10,30)/100, randint(40,70)/100)
    
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
    
    def infect(self, turn):
        """
        infects a citizen of a city if the city has not yet been infected
        """
        if self.first_infection_turn is None and self.is_infected():
            self.first_infection_turn = turn
        if self.is_infected()==False:
            self.infected[-1] = 1/self.pop
            self.healthy[-1] = 1 - (self.infected[-1] + self.recovered[-1] + self.dead[-1])
        return
    
    def check_lockdown_status(self):
        """
        Checks if a lockdown should be put in place or raised
        """
        # Starts a lockdown if the threshold is reached
        if self.infected[-1] >= self.lockdown_threshold and not self.lockdown:
            self.lockdown = True
            print(f"ALERTE: La ville {self.name} entre en confinement avec {self.infected[-1]*100:.1f}% de population infectée")
        
        # Raise the lockdown if the infected level returns under threshold 
        elif self.infected[-1] < self.lockdown_threshold and self.lockdown:
            self.lockdown = False
            print(f"INFO: La ville {self.name} sort du confinement avec {self.infected[-1]*100:.1f}% de population infectée")
        
        # Enregistrer l'état de confinement
        self.lockdown_history.append(self.lockdown)
        
        return self.lockdown
    
    def propagate_to(self, town, turn=0):
        """
        model of propagation to new cities.
        """
        if self.distance(town) != 0 and not self.lockdown and not town.lockdown:
            return (170/self.distance(town))**2 * self.infected[-1]  #170 is the avg distance between 2 points on the pixmap
        return 0
    
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
        ####print(f"[DEBUG] {self.name} tick: healthy={self.healthy[-1]:.2f}, infected={self.infected[-1]:.2f}, rate={self.propagation_rate}")

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
        ####print(f"[DEBUG] {self.name} reçoit propagation={virus.propagation}, mortality={virus.mortality_symptoms}")
        self.propagation_rate = self.prop_fac*th((virus.propagation)/10)
        self.healing_rate = 1/(self.healing_fac*th((virus.length_infection)/10))
        self.mortality_rate = self.mortal_fac*th(virus.mortality_symptoms/10)
    
        if self.lockdown:
            self.propagation_rate *= (1 - self.lockdown_effectiveness)

        return


def global_propagation(list_cities, turn, nbticks=10):
    """
    Function that allows the virus to propagate between cities
    """
    newly_infected_cities_id = []

    for town in list_cities:
        town.check_lockdown_status()

    M = np.array([[town1.propagate_to(town2) for town2 in list_cities] for town1 in list_cities])
    prop_values = M.sum(axis=0)
    randval = np.random.rand(len(list_cities))
    
    for i in range(len(list_cities)):
        if randval[i] < prop_values[i] and (not list_cities[i].is_infected()):
            list_cities[i].infect(turn)
            newly_infected_cities_id.append(list_cities[i].id)
    if len(newly_infected_cities_id) != 0:
        message = f"The virus has arrived to these cities: {[str(list_cities[i].name) for i in newly_infected_cities_id]}"
    else:
        message = f"Currently, {len([town for town in list_cities if town.is_infected()])}/{len(list_cities)} cities have been infected with your virus."
    return message
