from numpy import tanh as th

class Virus:
    def __init__(self, name, mutation_points=10):
        self.name = name
        self.symptoms = {}  # Dictionary of active symptoms
        self.mutation_points = mutation_points # evolution points (game currency)

        self.resistance = 0  # recovery value
        self.healing_rate = 0 # SIRD Model coeff

        self.propagation = 0  # propagation value
        self.transmission_rate = 0 # SIRD Model coeff

        self.mortality = 0 # mortality value
        self.mortality_rate = 0 # SIRD Model coeff

        self.length_infection = 1 # length of infection value
        self.infection_duration = 30 # SIRD Model coeff
        
        """
        cough = Symptom("Cough", seriousness=2, mutation_cost=3, propagation_impact=1, mortality_impact=0)
        fever = Symptom("Fever", seriousness=3, mutation_cost=5, propagation_impact=2, mortality_impact=1)
        death = Symptom("Death", seriousness=10, mutation_cost=8, propagation_impact=0, mortality_impact=5)
        
        # Add symptoms
        self.add_symptom(cough)  
        self.add_symptom(fever)  
        self.add_symptom(death)  
        """
    
    def add_symptom(self, symptom):
        """
        Add a symptom to the virus class
        """
        if self.mutation_points >= symptom.mutation_cost:
            self.symptoms[symptom.name] = symptom
            self.mutation_points -= symptom.mutation_cost
            self.update_params()
        else:
            message = f"Not enough mutation points to add {symptom.name}."
            return message

    def upgrade_symptom(self, symptom_name):
        """
        Upgrades a symptom of the Class given its name
        """
        if self.mutation_points >= self.symptoms[symptom_name].mutation_cost:
            new_level = self.symptoms[symptom_name].upgrade()
            return new_level
        error_msg = "Not enough mutation points to upgrade this symptom"
        return error_msg

    def update_params(self):
        """
        Updates the constants for the SIRD model we used
        """
        self.propagation = sum([self.symptoms[name].propagation_impact for name in self.symptoms.keys])
        self.length_infection = sum([self.symptoms[name].recov_rate_impact for name in self.symptoms.keys])
        self.mortality = sum([self.symptoms[name].mortality_impact for name in self.symptoms.keys])

        self.transmission_rate = th(self.transmission_rate)
        self.infection_duration = 30*th(self.length_infection)
        self.mortality_rate = 0.2*th(self.mortality)
        return


    def show_symptoms(self):
        message = [f"Symptoms of the virus {self.name}:"]
        for symptom in self.symptoms:
            message.append(symptom.show_details())
        return message

    def show_stats(self):
        """
        Returns an str that describes the global attributes of the virus. Can be used to show to the user or for debug
        """
        message = f"Virus {self.name}: Propagation={self.propagation}, Resistance={self.resistance}, Mutation points={self.mutation_points}"
        # print(message)
        return message



class Symptom:
    def __init__(self, name, mutation_cost, recov_rate_impact, propagation_impact, mortality_impact):
        """
        Initializes new symptoms to add to the virus
        """
        self.name = name
        self.mutation_cost = mutation_cost
        self.level = 0

        self.recov_rate_impact0 = recov_rate_impact
        self.propagation_impact0 = propagation_impact
        self.mortality_impact0 = mortality_impact

        self.recov_rate_impact = recov_rate_impact
        self.propagation_impact = propagation_impact
        self.mortality_impact = mortality_impact
        

    def show_details(self):
        """
        Information on one of the user's symptoms. Returns an str that can be used to show to the user or debug
        """
        message = f"{self.name} - Seriousness: {self.seriousness}, Cost: {self.mutation_cost}, Propagation: {self.propagation_impact}, Mortality: {self.mortality_impact}"
        # print(message)
        return message

    
    def upgrade(self):
        """
        Upgrades the stats of a symptom by one level
        Returns the new level of the symptom (int)
        """
        self.level +=1
        self.mortality_impact += self.mortality_impact0
        self.propagation_impact += self.propagation_impact0
        self.recov_rate_impact += self.recov_rate_impact0
        return self.level



"""
cough = Symptom("Cough", seriousness=2, mutation_cost=3, propagation_impact=1, mortality_impact=0)
fever = Symptom("Fever", seriousness=3, mutation_cost=5, propagation_impact=2, mortality_impact=1)
death = Symptom("Death", seriousness=10, mutation_cost=8, propagation_impact=0, mortality_impact=5)

# Create a virus
virus = Virus("SuperVirus", propagation=1, resistance=1, mutation_points=10)

# Display initial stats
virus.show_stats()

# Add symptoms
virus.add_symptom(cough)  # Should work
virus.add_symptom(fever)  # Should work if there are enough points
virus.add_symptom(death)  # May fail if points are insufficient

# Display symptoms and stats after evolutions
virus.show_symptoms()
virus.show_stats()
"""
