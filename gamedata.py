from parser import get_list_from_file
from virus import Virus
from city import global_propagation
import random 

class GameData():
    def __init__(self, filename, maxturns):
        self.cities = get_list_from_file(filename + "/cities.py", "list_cities")
        self.ncities = len(self.cities)
        self.virus = Virus("SuperVirus")
        self.resize = 0
        self.xmin = 0
        self.ymin = 0
        self.turn = 0
        self.maxturns = maxturns
        self.selected_city = 0
        self.messages = [[""] for _ in range(self.maxturns+1)]
        self.messages[0].append("Game starts now.")
        self.vaccination_time = random.randint(5,18)
        self.vaccination_prop = 0.2

    def click_turn(self):
        self.turn += 1
        vaccine_msg = self.vaccine()
        propag_msg = global_propagation(self.cities) 
        self.virus.mutation_points += 2

        for i in range (self.ncities):
            town = self.cities[i]
            town.propagation_tick(self.virus, nb_ticks=100)

        if self.turn < self.maxturns:
            self.messages[self.turn].append(propag_msg + " ; " + vaccine_msg)

        if self.turn == self.maxturns:
            self.messages[-1].append("This is your last turn! Clicking next turn will end the game and close the app")
    
        return
    
    def click_symptom(self, index):
            if self.virus.mutation_points >= self.virus.symptoms[index].mutation_cost:
                self.virus.upgrade_symptom(index)
                self.virus.propagation += self.virus.symptoms[index].propagation_impact
                self.virus.infection_duration += self.virus.symptoms[index].duration_impact
            else:
                self.messages[self.turn].append(f"Not enough points available to upgrade the symptom {self.virus.symptoms[index].name}. Points required : {self.virus.symptoms[index].mutation_cost}")
            return

    def vaccine(self):
        if self.turn == self.vaccination_time:
            for town in self.cities:
                prop_vaccinated = min(self.vaccination_prop, town.healthy[-1])
                town.recovered[-1] += prop_vaccinated
                town.healthy[-1] -= prop_vaccinated
            message = f"The UK has developped a vaccine !"
            return message
        else:
            return ""
                

