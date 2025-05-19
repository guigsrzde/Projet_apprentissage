from cerveau import Brain, NoSkill, SimpleHeuristic
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
        
        # Demander à l'agent de choisir des actions
        chosen_actions = brain.choose_action(game)
        
        print(f"Tour actuel: {current_turn}/{max_turns}")

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
    reward = 0 ###############
    
    for symptom in actions.values():
        game.click_symptom(symptom.name)
        game.history.add_action(game.turn, symptom.name)

    reward = 10  ####################
    
    return reward

def get_game_result(game):
    """Retourne un résumé des résultats du jeu."""
    total_infected_percentage = 0
    world_pop = sum([town.pop for town in game.cities])
    for town in game.cities:
        total_infected_percentage += (1-(town.healthy[-1] + town.vaccination_prop*town.healthy[game.vaccination_time-1]))*town.pop/world_pop
    return {
        "World population": world_pop,
        "Total percentage of people that got contaminated": total_infected_percentage*100,
        "Total number of deaths by virus": sum([town.dead[-1]*town.pop for town in game.cities]),
        "Total number of people still infected": sum([town.infected[-1]*town.pop for town in game.cities]),
        "Total nunmber of people still healthy (neither vaccined nor ever infected)": sum([town.healthy[-1]*town.pop for town in game.cities]),
        "Total number of recovered people": sum([town.recovered[-1]*town.pop for town in game.cities]),
        "Total number of people who received the vaccine": sum([town.vaccination_prop*town.healthy[game.vaccination_time-1]*town.pop for town in game.cities]),
        "mutation_points left": game.virus.mutation_points,
    }

game_instance = GameData("random", 20)
basic_brain = Brain(SimpleHeuristic())
run_game_with_agent(basic_brain, game_instance)