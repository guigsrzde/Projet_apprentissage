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
    newI = town.infected * (town.healthy * disease.incidence - 1/disease.infection_duration - disease.virulence) * dt + town.infected
    town.recovered = newR
    town.healthy = newS
    town.infected = newI


R = np.array([0])
S = np.array([0.9])
I = np.array([1-S[0]])
L = 30
B = 1
M = 0.1

for i in range(1000):
    R,S,I = update_eq(R,S,I,L,B,M)

plt.plot(R, label='rétablis')
plt.plot(S, label='sains')
plt.plot(I, label='infectés')
plt.plot(R+S+I, label='Population totale')
plt.plot
plt.grid()
plt.legend()
plt.show()
