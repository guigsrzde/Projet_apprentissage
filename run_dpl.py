from gamedata import GameData
import numpy as np
from discrete_policy_learning import QLearningBrain
import matplotlib.pyplot as plt
import pickle

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

def plot_results(event_time, score):
    unique_events = np.unique(event_time)
    n_events = len(unique_events)
    means=[]
    
    ncols = 4
    nrows = max((n_events + 1) // ncols,1)

    fig, axs = plt.subplots(nrows, ncols, figsize=(12, 3 * nrows))
    axs = np.array(axs).reshape(-1)  # Flatten in case of single row

    for i, evt in enumerate(unique_events):
        indices = np.where(event_time == evt)[0]
        x = indices
        score = np.array(score)
        y = score[indices]
        means.append(sum(y)/len(y))

        axs[i].plot(x, y)
        axs[i].set_title(f"Event Time = {evt}", fontsize=12)
        if i ==0:
            axs[i].set_ylabel("Score")
    
    axs[-1].plot(range(8,8+n_events), means, marker='o')
    axs[-1].set_title("score moyen en fonction de la vaccination")
    
    
    plt.subplots_adjust(hspace=0.4)
    plt.show()

def constant_reward_fn(game:GameData, actions):
    return game.score_function1()  # récompense constante

def train_q_agent(num_episodes=100, brain=None):
    brain = brain
    scores = []
    v_times = []

    for episode in range(num_episodes):
        game = GameData("random", 20)
        symptom_dict = game.virus.symptoms

        if brain is None:
            brain = QLearningBrain(symptom_dict)
        else:
            brain.symptom_dict = symptom_dict
            brain.symptom_list = list(symptom_dict.values())
        
        run_q_game(brain, game)
        scores.append(game.score)
        v_times.append(game.vaccination_time)
        if episode%10==0:
            print(f"train game number {episode}")
        #print(f"Épisode {episode+1}/{num_episodes} terminé — epsilon = {brain.epsilon:.4f}")
    #plot_results(v_times, scores)
    #smooth_histogram(scores)
    #print(f"score_mean :{np.mean(scores)}, epsilon = {brain.epsilon}")
    return brain
    
def run_q_game(brain, game):
    game.selected_city = brain.choose_first_city_idx(game)
    game.first_city_choice()
    #print(f"Ville de départ : {game.start_city.name}")

    while game.turn <= game.maxturns:
        actions = brain.choose_action(game)

        if actions:
            apply_action(game, actions)
            brain.learn(game, actions)
        else:
            brain.learn(game, actions={})

        game.click_turn()
    return 

def apply_action(game:GameData, actions):
    if actions:
        for symptom in actions.values():
            game.click_symptom(symptom.name)
            #game.history.add_action(game.turn, symptom.name)
    else:
        game.click_turn()

def validate_brain(brain, n_iter):
    scores = []
    v_times = []
    for n in range (n_iter):
        game = GameData("random", 20)
        brain.symptom_dict = game.virus.symptoms
        brain.symptom_list = list(brain.symptom_dict.values())
        run_q_game(brain, game)
        scores.append(game.score)
        v_times.append(game.vaccination_time)
        if n%10==0:
            print(f"validation game number {n}")

    #plot_results(v_times, scores)
    #smooth_histogram(scores)
    return v_times, scores


if __name__ == "__main__":
    data = []
    for i in range(10):
        print(f"interation {i}")
        brain = train_q_agent(num_episodes=100)
        data.append(brain)
    with open('brains.pkl', 'wb') as f:
        pickle.dump(data, f)
