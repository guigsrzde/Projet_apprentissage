import numpy as np
import matplotlib.pyplot as plt

# Parameters
T = 365  # Total time in days
dt = 0.1  # Time step

# Number of time steps
N = int(T / dt)

# Initialization of arrays
t = np.linspace(0, T, N)
S = np.zeros(N)
I = np.zeros(N)
R = np.zeros(N)
D = np.zeros(N)

# Initial conditions
S[0] = 0.99  # Initial proportion of the population susceptible
I[0] = 0.01  # Initial proportion of the population infected
R[0] = 0.0   # Initial proportion of the population recovered
D[0] = 0.0   # Initial proportion of the population deceased
    
def SIRD_model(S, I, R, D, T, dt, virus, n):

    # Updated parameters
    beta = 
    gamma = 
    mu = 

    # Simulation avec la méthode d'Euler
    dS = -beta * S[n-1] * I[n-1] * dt
    dI = (beta * S[n-1] * I[n-1] - gamma * I[n-1] - mu * I[n-1]) * dt
    dR = gamma * I[n-1] * dt
    dD = mu * I[n-1] * dt

    S[n] = S[n-1] + dS
    I[n] = I[n-1] + dI
    R[n] = R[n-1] + dR
    D[n] = D[n-1] + dD
       
    return S[n], I[n], R[n], D[n]



# def plot_SIRD(t, S, I, R, D):
#     """Affiche les résultats du modèle SIRD."""
#     plt.figure(figsize=(10, 6))
#     plt.plot(t, S, label='S (Susceptibles)', color='blue')
#     plt.plot(t, I, label='I (Infectés)', color='red')
#     plt.plot(t, R, label='R (Rétablis)', color='green')
#     plt.plot(t, D, label='D (Décédés)', color='black')
#     plt.xlabel('Temps (jours)')
#     plt.ylabel('Proportion de la population')
#     plt.title('Modèle SIRD - Méthode d\'Euler')
#     plt.legend()
#     plt.grid()
#     plt.show()

# # Exemple d'utilisation
if __name__ == "__main__":
#     # Paramètres initiaux
#     S0 = 0.99  # Population initiale susceptible
#     I0 = 0.01  # Population initiale infectée
#     R0 = 0.0   # Population initiale rétablie
#     D0 = 0.0   # Population initiale décédée

#     # Paramètres du modèle
#     beta = 0.3    # Transmission rate
#     gamma = 0.0   # Healing rate
#     mu = 0.05     # Mortality rate

#     # Paramètres temporels
#     T = 100  # Temps total en jours
#     dt = 0.1  # Pas de temps

#     # Simulation
#     t, S, I, R, D = SIRD_model(S0, I0, R0, D0, beta, gamma, mu, T, dt)
    print(S[1])
    # Affichage des résultats
    plot_SIRD(t, S, I, R, D)

    