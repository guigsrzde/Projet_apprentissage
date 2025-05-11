import pandas as pd
from datetime import datetime
from gamedata import GameData

def action(symptom_key):
    return f"clicl symptom {symptom_key}"

class GameHistory:
    def __init__(self, nb_turns, allgamedata:GameData):
        self.turn_actions = {i:[] for i in range(nb_turns)}
        self.alldata = allgamedata

    def add_action(self, turn_nb, symptom_key):
        self.turn_actions[turn_nb].append(action(symptom_key))
    
    def add_arrays(self):
        arrays = []
        for i in range(self.alldata.ncities):
            for time in range(len(self.alldata.cities[0].infected)):
                arrays.append({
                    "City id": self.alldata.cities[i].id,
                    "time": time,
                    "Infected": self.alldata.cities[i].infected,
                    "Healthy": self.alldata.cities[i].healthy,
                    "Dead": self.alldata.cities[i].dead,
                    "Recovered": self.alldata.cities[i].recovered
                })
        self.values = arrays
    
    def export_file(self):
        self.add_arrays()
        data = pd.DataFrame(self.values)
        data.to_csv(f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}', index=False, encoding='utf-8')
