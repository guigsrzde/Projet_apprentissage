import pandas as pd
from datetime import datetime

ACTIONS = {"S1":"Click symptom 1", "S2":"Click Symtom 2", "S3":"Click Symtom 3", "S4":"Click Symtom 4"}

class GameHistory:
    def __init__(self, nb_turns):
        self.turn_actions = {i:None for i in range(nb_turns)}

    def add_action(self, turn_nb, symptom_number):
        if (self.turn_actions[turn_nb] is not None):
            self.turn_actions[turn_nb].append(ACTIONS[f"S{symptom_number}"])
        else:
            self.turn_actions[turn_nb] = ACTIONS[f"S{symptom_number}"]
    
    def export_file(self):
        data = pd.DataFrame(self.nb_turns)
        data.to_excel(f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx', index=False)
