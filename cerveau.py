from gamedata import GameData
from history import action
import pickle
import random

class Brain:
    def __init__(self, model):
        self.model=model

    def choose_first_city_idx(self, game):
        return self.model.choose_first_city_idx(game)

    def choose_action(self,state):
        return self.model.predict_action(state)
    
    def learn(self, state, action, reward):
        self.model.update(state, action, reward)

class NoSkill:
    def __init__self():
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



