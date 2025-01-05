import numpy as np
import matplotlib.pyplot as plt


# Nombre de pas de temps
N = int(T / dt)

# Initialisation des tableaux                       
t = np.linspace(0, T, N)
S = np.zeros(N)
I = np.zeros(N)
R = np.zeros(N)
D = np.zeros(N)


def SIRD_model(S0, I0, R0, D0, beta, gamma, mu, T, dt, instant):

    # Conditions initiales
    S[instant] = S0
    I[instant] = I0
    R[instant] = R0
    D[instant] = D0

    # Simulation avec la méthode d'Euler
    for n in range(N - 1):
        dS = -beta * S[n] * I[n] * dt
        dI = (beta * S[n] * I[n] - gamma * I[n] - mu * I[n]) * dt
        dR = gamma * I[n] * dt
        dD = mu * I[n] * dt

        S[n+1] = S[n] + dS
        I[n+1] = I[n] + dI
        R[n+1] = R[n] + dR
        D[n+1] = D[n] + dD

    return t, S, I, R, D

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

# Exemple d'utilisation
if __name__ == "__main__":
    # Paramètres initiaux
    S0 = 0.99  # Population initiale susceptible
    I0 = 0.01  # Population initiale infectée
    R0 = 0.0   # Population initiale rétablie
    D0 = 0.0   # Population initiale décédée

    # Paramètres du modèle
    beta = 0.3    # Taux de transmission
    gamma = 0.0   # Taux de récupération
    mu = 0.05     # Taux de mortalité

    # Paramètres temporels
    T = 100  # Temps total en jours
    dt = 0.1  # Pas de temps

    # Simulation
    t, S, I, R, D = SIRD_model(S0, I0, R0, D0, beta, gamma, mu, T, dt)

    # Affichage des résultats
    plot_SIRD(t, S, I, R, D)

    