import virus
import city
import matplotlib.pyplot as plt
import numpy as np


test_city = city.City.random(1,1,1)
disease = virus.Virus("Supervirus")
#I + R + S = P
#P: total population
#R: individuals that recovered (they are immunised)
#S: healthy indivisuals
#I: infected individuals

#equations : 
#I'(t) = B*I(t)*S(t) - I(t)/L - M*I(t)
#S'(t) = -B*I(t)*S(t)
#R'(t) = I(t)/L
#L: average length of infection before recovery or death
#B: value that characterises how infectious a virus is
#M: virus death rate

def update_eq(R,S,I,L,B,M,dt=0.1):
    newR = I[-1]/L * dt + R[-1]
    newS = -B*I[-1] * S[-1]*dt + S[-1]
    newI = I[-1]*(S[-1]*B-1/L-M) * dt + I[-1]
    R = np.append(R,newR)
    S = np.append(S,newS)
    I = np.append(I,newI)
    return R,S,I

def propagate_virus(town, disease, dt=0.1):
    newR = town.infected/disease.infection_duration * dt + town.recovered
    newS = -disease.incidence * town.infected * town.healthy *dt + town.healthy
    newI = town.infected * (town.healthy * disease.incidence - 1/disease.infection_duration - disease.mortality) * dt + town.infected
    town.recovered = newR
    town.healthy = newS
    town.infected = newI


R = np.array([0])
S = np.array([test_city.healthy])
I = np.array([test_city.infected])
L = 30
B = 1
M = 0.1

Rtest = np.array([0])
Stest = np.array([test_city.healthy])
Itest = np.array([test_city.infected])

for i in range(1000):
    R,S,I = update_eq(R,S,I,L,B,M)
    propagate_virus(test_city, disease)
    Rtest = np.append(Rtest, test_city.recovered)
    Stest = np.append(Stest, test_city.healthy)
    Itest = np.append(Itest, test_city.infected)

plt.plot(Rtest, label='recovered')
plt.plot(Stest, label='healthy')
plt.plot(Itest, label='infected')
plt.plot(Rtest+Itest+Stest, label='total population')
plt.plot
plt.grid()
plt.legend()
plt.show()
