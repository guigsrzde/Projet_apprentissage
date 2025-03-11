from parser import get_list_from_file
from virus import Virus
from city import global_propagation
from city import City
import random 

class GameData():
    def __init__(self, filename, maxturns):
        self.cities = get_list_from_file(filename + "/cities.py", "list_cities")
        self.start_city = None
        self.ncities = len(self.cities)
        self.virus = Virus("SuperVirus")
        self.resize = 0
        self.xmin = 0
        self.ymin = 0
        self.turn = 0
        self.maxturns = maxturns
        self.selected_city = 0
        self.messages_err = [[""] for _ in range(self.maxturns+1)]
        self.messages_evt = [[""] for _ in range(self.maxturns+1)]
        self.messages_err[0].append("Game starts now. Click on the City you want to start your virus in.")
        self.messages_evt[0].append("You will be warned of unexpected events here.")
        self.vaccination_time = random.randint(5,18)
        self.vaccination_prop = 0.2

    def click_turn(self):
        if self.start_city is None:
            return
        self.turn += 1
        vaccine_msg = self.vaccine()
        propag_msg = global_propagation(self.cities) 
        self.virus.mutation_points += 2
        

        for i in range (self.ncities):
            town = self.cities[i]
            town.propagation_tick(nb_ticks=100,timeupdate=(self.turn!=1))

        if self.turn < self.maxturns:
            self.messages_err[self.turn].append(propag_msg)
            self.messages_evt[self.turn].append(vaccine_msg)

        if self.turn == self.maxturns:
            self.messages_err[-1].append("This is your last turn! Clicking next turn will end the game and close the app")
    
        return
    
    def click_symptom(self, index):
            if self.virus.mutation_points >= self.virus.symptoms[index].mutation_cost:
                self.virus.upgrade_symptom(index)
                self.virus.propagation += self.virus.symptoms[index].propagation_impact
                self.virus.infection_duration += self.virus.symptoms[index].duration_impact
                for i in range(self.ncities):
                    self.cities[i].update_params(self.virus)
            else:
                self.messages_err[self.turn].append(f"Not enough points available to upgrade the symptom {self.virus.symptoms[index].name}. Points required : {self.virus.symptoms[index].mutation_cost}")
            return
    
    def first_city_choice(self):
        if self.start_city is None:
            self.start_city = self.cities[self.selected_city]
            self.start_city.infect()
            self.messages_err.append(f"You have selected {self.start_city.name} to start your virus.")
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
                

