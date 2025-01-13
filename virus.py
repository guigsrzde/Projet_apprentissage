
class Virus:
    def __init__(self, name, propagation=1, resistance=1, mutation_points=100):
        self.name = name
        self.symptoms = []  # List of active symptoms

        self.propagation = propagation  # base level of propagation
        self.transmission_rate = 1 - 1/propagation # Increases with the propagation

        self.resistance = resistance  # base level of resistance
        self.healing_rate = 1/resistance # Decreases when the virus' resistance increases

        self.mortality_rate = 0.1 # value that determines how harmful the virus is 

        self.mutation_points = mutation_points # evolution points (game currency)

        self.infection_duration = 30 # average number of turns that a person stays infected before dying or recovering
        self.incidence = 1 # value that determines how fast the virus propagates
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
        if self.mutation_points >= symptom.mutation_cost:
            self.symptoms.append(symptom)
            self.propagation += symptom.propagation_impact
            # self.mortality_rate += symptom.mortality_impact
            self.mutation_points -= symptom.mutation_cost
            print(f"{symptom.name} added ! Propagation level : {self.propagation}, Resistance level : {self.resistance}. Leftover points : {self.mutation_points}")
        else:
            print(f"Not enough mutation points to add {symptom.name}.")

    def intensify(self, caracteristic, value):
        if self.mutation_points >= value:
            setattr(self, caracteristic, getattr(self, caracteristic) + value)
            self.mutation_points -= value
            print(f"{caracteristic.capitalize()} upgraded to {getattr(self, caracteristic)}. Leftover points : {self.mutation_points}")
        else:
            print("Not enough mutation points")

    def show_symptoms(self):
        print(f"Symptoms of the virus {self.name}:")
        for symptom in self.symptoms:
            symptom.show_details()

    def show_stats(self):
        print(f"Virus {self.name}: Propagation={self.propagation}, Resistance={self.resistance}, Mutation points={self.mutation_points}")




class Symptom:
    def __init__(self, name, seriousness, mutation_cost, propagation_impact, mortality_impact):
        self.name = name
        self.seriousness = seriousness
        self.mutation_cost = mutation_cost
        self.propagation_impact = propagation_impact
        self.mortality_impact = mortality_impact
        self.level = 0

    def show_details(self):
        print(f"{self.name} - Seriousness: {self.seriousness}, Cost: {self.mutation_cost}, Propagation: {self.propagation_impact}, Mortality: {self.mortality_impact}")
    
    def upgrade(self):
        #A faire
        self.level +=1

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
