from gamedata import GameData
import numpy as np
from discrete_policy_learning import QLearningBrain
import matplotlib.pyplot as plt

def smooth_histogram(data, bins=30, kernel_width=3):
    # Histogramme simple
    counts, bin_edges = np.histogram(data, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Création d'un noyau gaussien simple
    kernel_size = kernel_width
    kernel_x = np.linspace(-3, 3, kernel_size)
    kernel = np.exp(-0.5 * kernel_x**2)
    kernel /= kernel.sum()  # normaliser le kernel

    # Convolution pour lisser l'histogramme
    smooth_counts = np.convolve(counts, kernel, mode='same')

    # Plot
    plt.figure(figsize=(8,5))
    plt.bar(bin_centers, counts, width=bin_edges[1]-bin_edges[0], alpha=0.4, label='Histogramme')
    plt.plot(bin_centers, smooth_counts, color='red', label='Histogramme lissé')
    plt.xlabel('Valeurs')
    plt.ylabel('Densité estimée')
    plt.title('Estimation de densité (histogramme lissé)')
    plt.legend()
    plt.grid(True)
    plt.show()


def constant_reward_fn(game, actions):
    return game.score  # récompense constante

def train_q_agent(num_episodes=100):
    brain = None
    scores = []

    for episode in range(num_episodes):
        game = GameData("random", 20)
        symptom_dict = game.virus.symptoms

        if brain is None:
            brain = QLearningBrain(symptom_dict, reward_fn=constant_reward_fn)
        else:
            brain.symptom_dict = symptom_dict
            brain.symptom_list = list(symptom_dict.values())

        scores.append(run_q_game(brain, game))
        brain.epsilon = max(0.01, brain.epsilon-0.01)
        print(f"Épisode {episode+1}/{num_episodes} terminé — epsilon = {brain.epsilon:.4f}")
    smooth_histogram(scores)
    plt.plot(scores)
    

def run_q_game(brain, game):
    game.selected_city = brain.choose_first_city_idx(game)
    game.first_city_choice()
    print(f"Ville de départ : {game.start_city.name}")

    while game.turn < game.maxturns:
        actions = brain.choose_action(game)

        if actions:
            apply_action(game, actions)
            brain.learn(game, actions)
        else:
            brain.learn(game, actions={})

        game.vaccine()
        game.click_turn()
    print(game.score)
    return game.score

def apply_action(game, actions):
    for symptom in actions.values():
        game.click_symptom(symptom.name)
        game.history.add_action(game.turn, symptom.name)




if __name__ == "__main__":
    train_q_agent(num_episodes=100)
