import pandas as pd
from datetime import datetime
from city import City

def action(symptom_key):
    return f"{symptom_key}"

class GameHistory:
    def __init__(self, nb_turns, export=False):
        self.turn_actions = {i:[] for i in range(nb_turns+1)}
        self.nbturns = nb_turns
        self.do = export

    def add_action(self, turn_nb, symptom_key):
        if self.do:
            self.turn_actions[turn_nb].append(action(symptom_key))
    
    def add_arrays(self, cities):
        if self.do:
            arrays = []
            mult_factor = len(cities[0].infected)//self.nbturns
            for i in range(len(cities)):
                for time in range(self.nbturns):
                    adjusted_time = time * mult_factor
                    arrays.append({
                        "City id": cities[i].id,
                        "City Name": cities[i].name,
                        "turn": time,
                        "Infected": cities[i].infected[adjusted_time],
                        "Healthy": cities[i].healthy[adjusted_time],
                        "Dead": cities[i].dead[adjusted_time],
                        "Recovered": cities[i].recovered[adjusted_time],
                        "Actions": self.turn_actions[time]
                    })
            self.values = arrays
    
    def export_file(self, cities):
        if self.do:
            self.add_arrays(cities)
            data = pd.DataFrame(self.values)
            data.to_csv(f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}', index=False, encoding='utf-8')
