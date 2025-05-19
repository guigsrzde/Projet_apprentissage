from cerveau import Brain, NoSkill
from gamedata import GameData
from PyQt5.QtWidgets import QApplication
from sys import argv


def run_game_with_agent(brain, game):
    
    game.selected_city = brain.choose_first_city_idx(game)
    game.first_city_choice()
    print(f"Ville de départ sélectionnée: {game.start_city.name}")
    max_turns = game.maxturns   
    current_turn = game.turn
    print(f"Tour initial: {current_turn}, Tours maximum: {max_turns}")

    iteration_count = 0
    max_iterations = 1000

    while current_turn < max_turns:
        # Récupérer l'état actuel du jeu
        ####current_state = game.cities
        
        # Demander à l'agent de choisir des actions
        chosen_actions = brain.choose_action(game)#current_state)
        
        iteration_count += 1
        print(f"Itération {iteration_count}, Tour actuel: {current_turn}/{max_turns}")
        
        if iteration_count > max_iterations:
            print("ALERTE: Boucle infinie détectée - arrêt forcé")
            break

        reward = 0
        if chosen_actions is not None:
            reward = execute_action_in_game(game, chosen_actions)
            
            brain.learn(game, chosen_actions, reward)
        
        game.vaccine()   
        game.click_turn() 
        current_turn = game.turn
        
        if current_turn == max_turns:
            break
    
    # Afficher les résultats
    print(f"Partie terminée au tour {current_turn}")
    print(f"Résultats: " )
    for key, value in get_game_result(game).items():
        print(f"{key}: {round(value)}")
        # if isinstance(value, (float)):
        #     print(f"{key}: {value:.4f}")
        # else:
        #     print(f"{key}: {value}")
    

def execute_action_in_game(game, actions):
    """Exécute l'action fournie par l'agent dans le jeu."""
    reward = 0
    
    for symptom in actions.values():
        game.click_symptom(symptom.name)
        game.history.add_action(game.turn, symptom.name)

    reward = 10  ####################
    
    return reward

def get_game_result(game):
    """Retourne un résumé des résultats du jeu."""
    total_infected_percentage = 0
    total_deaths = 0
    total_recovered = 0
    for town in game.cities:
        total_infected_percentage += town.infected[-1] + town.recovered[-1] - town.vaccination_prop * town.healthy[game.vaccination_time]
        total_deaths += town.dead[-1]*town.pop
        total_recovered += town.recovered[-1]*town.pop
    return {
        "Total number of people that got contaminated": total_infected_percentage,
        "Total number of deaths by virus": total_deaths,
        "mutation_points left": game.virus.mutation_points,
        "Total number of recovered people": total_recovered,
    }

game_instance = GameData("royaume_uni", 20)
basic_brain = Brain(NoSkill())
run_game_with_agent(basic_brain, game_instance)