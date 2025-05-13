from gamedata import GameData
from history import action

class Brain:
    def __init__(self, model):
        self.model=model

    def choose_action(self,state):
        return self.model.predict_action(state)
    
    def learn(self, state, action, reward):
        self.model.update(state, action, reward)

class NoSkill:
    def __init__self():
        return

    def predict_action(self, state:GameData):
        if state.virus.mutation_points >= list(state.virus.symptoms.keys())[0].mutation_cost:
            return action(list(state.virus.symptoms.keys())[0])  #list(state.virus.symptoms.keys())[0] corresponds to the name of the symptom
        else:
            return None
    def update(self, state, action, reward):
        return None



try:
    cerveau_basique
except NameError:
    cerveau_basique = Brain(NoSkill())


