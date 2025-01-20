import virus
import city
import matplotlib.pyplot as plt
import numpy as np


test_city = city.City.random(1,1,1)
disease = virus.Virus("Supervirus")
test_city.infect()

def propagate_virus(town, disease, dt=0.1):
    newR = town.infected[-1]/disease.infection_duration * dt + town.recovered[-1]
    newS = -disease.incidence * town.infected[-1] * town.healthy[-1] *dt + town.healthy[-1]
    newI = town.infected[-1] * (town.healthy[-1] * disease.incidence - 1/disease.infection_duration - disease.mortality) * dt + town.infected[-1]
    town.add_values(newR,newS,newI)

for i in range(1000):
    propagate_virus(test_city, disease)

X = range(1001)
plt.plot(X,test_city.recovered, label='recovered')
plt.plot(X,test_city.healthy, label='healthy')
plt.plot(X,test_city.infected, label='infected')
plt.plot(X,test_city.dead, label = 'dead')
plt.plot(X,test_city.recovered+test_city.infected+test_city.healthy, label='total population')
plt.grid()
plt.legend()
plt.show()
