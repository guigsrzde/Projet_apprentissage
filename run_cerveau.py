from cerveau import Brain, NoSkill
import gamedata
from PyQt5.QtWidgets import QApplication
from global_UI import Game
from sys import argv


def run_game_with_agent(brain, game):
    
    game_data = game._data
    max_turns = game_data.maxturns   
    current_turn = game_data.turn

    while current_turn < max_turns:
        # Récupérer l'état actuel du jeu
        current_state = game_data.cities
        
        # Demander à l'agent de choisir des actions
        chosen_actions = brain.choose_action(game_data)#current_state)
        
        reward = 0
        if chosen_actions is not None:
            reward = execute_action_in_game(game, chosen_actions)
            
            brain.learn(current_state, chosen_actions, reward)
        
        game_data.click_turn()     
        current_turn = game_data.turn
        
        if current_turn == max_turns:
            break
    
    # Afficher les résultats
    print(f"Partie terminée au tour {current_turn}")
    #print(f"Résultat: {game._history}")


def execute_action_in_game(game, actions):
    """Exécute l'action fournie par l'agent dans le jeu."""
    reward = 0
    game_data = game._data
    
    for symptom in actions:
        game_data.click_symptom(symptom)
        game._history.add_action(symptom)

    reward = 10  ####################
    
    return reward

def get_game_result(game):
    """Retourne un résumé des résultats du jeu."""
    data = game._data
    return {
        "infection_totale": data.world.total_infected_percentage(),
        "morts": data.world.total_deaths(),
        "mutation_points": data.virus.mutation_points,
        "symptomes_acquis": sum(1 for s in data.virus.symptoms.values() if s.is_acquired),
        "transmissions_acquises": sum(1 for t in data.virus.transmissions.values() if t.is_acquired)
    }

app = QApplication(argv)
game_instance = Game()
basic_brain = Brain(NoSkill())
run_game_with_agent(basic_brain, game_instance)