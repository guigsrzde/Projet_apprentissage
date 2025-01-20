import numpy as np
import matplotlib.pyplot as plt
import virus

# Parameters
T = 365  # Total time in days
dt = 0.1  # Time step

# Number of time steps
N = int(T / dt)

# Initialization of arrays
t = np.linspace(0, T, N)

# # Initial conditions
# healthy[0] = 0.99  # Initial proportion of the population susceptible
# infected[0] = 0.01  # Initial proportion of the population infected
# recovered[0] = 0.0   # Initial proportion of the population recovered
# deceased[0] = 0.0   # Initial proportion of the population deceased
    
# def SIRD_model(S, I, R, D, virus, n):

#     # Updated parameters
#     beta = virus.transmission_rate
#     gamma = virus.healing_rate
#     mu = virus.mortality_rate

#     # Simulation avec la méthode d'Euler
#     dS = -beta * S[n-1] * I[n-1] * dt
#     dI = (beta * S[n-1] * I[n-1] - gamma * I[n-1] - mu * I[n-1]) * dt
#     dR = gamma * I[n-1] * dt
#     dD = mu * I[n-1] * dt

#     S[n] = S[n-1] + dS
#     I[n] = I[n-1] + dI
#     R[n] = R[n-1] + dR
#     D[n] = D[n-1] + dD
       
#     return S[n], I[n], R[n], D[n]

def SIRD_model(S, I, R, D, virus):

    # Updated parameters
    beta = virus.transmission_rate
    gamma = virus.healing_rate
    mu = virus.mortality_rate

    # Simulation avec la méthode d'Euler
    dS = -beta * S[-1] * I[-1] * dt
    dI = (beta * S[-1] * I[-1] - gamma * I[-1] - mu * I[-1]) * dt
    dR = gamma * I[-1] * dt
    dD = mu * I[-1] * dt

    S.append(S[-1] + dS)
    I.append(I[-1] + dI)
    R.append(R[-1] + dR)
    D.append(D[-1] + dD)
       
    return S[-1], I[-1], R[-1], D[-1]



def plot_SIRD(t, S, I, R, D):
    """Affiche les résultats du modèle SIRD."""
    plt.figure(figsize=(10, 6))
    plt.plot(t, S, label='S (Susceptibles)', color='blue')
    plt.plot(t, I, label='I (Infectés)', color='red')
    plt.plot(t, R, label='R (Rétablis)', color='green')
    plt.plot(t, D, label='D (Décédés)', color='black')
    plt.xlabel('Temps (jours)')
    plt.ylabel('Proportion de la population')
    plt.title('Modèle SIRD - Méthode d\'Euler')
    plt.legend()
    plt.grid()
    plt.show()

"""# Exemple d'utilisation
if __name__ == "__main__":

    # Simulation
    S_, I_, R_, D_ = SIRD_model(S, I, R, D, virus, 1)
    print(S_, I_, R_, D_)
    # Affichage des résultats
    plot_SIRD(t, S_, I_, R_, D_)
"""
    