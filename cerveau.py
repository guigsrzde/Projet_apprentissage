from gamedata import GameData
from history import action
import pickle
import random

class Brain:
    def __init__(self, model, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.model=model
        self.epsilon = epsilon  # Taux d'exploration
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def choose_first_city_idx(self, game):
        """Picks the first city"""
        return self.model.choose_first_city_idx(game)

    def choose_action(self,state):
        """Chooses action based on state"""
        return self.model.predict_action(state)
    
    def learn(self, state, action, reward):
        """"""
        self.model.update(state, action, reward)

    def decay_epsilon(self):
        """Reduces epsilon after each episode"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    

class NoSkill:
    def __init__(self):
        return

    def choose_first_city_idx(self, game):
        return random.randint(0, game.ncities - 1) if game.cities else 0

    def predict_action(self, game):
        symptoms = list(game.virus.symptoms.values())
        actions = {}
        idx = 0
        if game.virus.mutation_points >= symptoms[idx].mutation_cost:
            actions[idx] = symptoms[idx]
        else :
            print("not enough points")
        return actions  
        
    def update(self, state, action, reward):
        return None

class SimpleHeuristic:
    def __init__(self):
        return
    
    def choose_first_city_idx(self, game):
        return random.randint(0, game.ncities - 1) if game.cities else 0
    
    def predict_action(self, game):
        symptoms = game.virus.symptoms
        actions = {}
        idx = 0
        if game.ncities > len(game.infected_cities) and game.virus.mutation_points >= symptoms["Cough"].mutation_cost:
            points = game.virus.mutation_points
            cost = symptoms["Cough"].mutation_cost
            while points >= cost:
                actions[idx] = symptoms["Cough"]
                idx += 1
                points -= cost

        elif game.ncities == len(game.infected_cities) and game.virus.mutation_points >= symptoms["Death"].mutation_cost:
            points = game.virus.mutation_points
            cost = symptoms["Death"].mutation_cost
            while points >= cost:
                actions[idx] = symptoms["Death"]
                idx += 1
                points -= cost
        
        else :
            print("not enough points")

        return actions  

    def update(self, state, action, reward):
        return None


