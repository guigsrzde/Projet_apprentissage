from numpy import tanh as th

class Virus:
    def __init__(self, name, mutation_points=30):
        self.name = name
        self.symptoms = {}  # Dictionary of active symptoms
        self.mutation_points = mutation_points # evolution points (game currency)

        
        #self.healing_rate = 0 # SIRD Model coeff

        self.propagation = 0 # propagation value (virus only)
        #self.transmission_rate = 0 # SIRD Model coeff

        self.mortality_symptoms = 0 # mortality value (symptoms only)
        #self.mortality_rate = 0 # SIRD Model coeff

        self.infection_duration = 40 # SIRD Model coeff
        
        
        cough = Symptom("Cough", duration_impact=-1, mutation_cost=3, propagation_impact=3, mortality_impact=0)
        fatigue = Symptom("Fatigue", duration_impact=-1, mutation_cost=5, propagation_impact=-3, mortality_impact=2)
        death = Symptom("Death", duration_impact=-3, mutation_cost=8, propagation_impact=0, mortality_impact=5)
        
        # Add symptoms
        self.add_symptom(cough)  
        self.add_symptom(fatigue)  
        self.add_symptom(death)  
        
    
    def add_symptom(self, symptom):
        """
        Add a symptom to the virus class
        """
        if self.mutation_points >= symptom.mutation_cost:
            self.symptoms[symptom.name] = symptom
            self.mutation_points -= symptom.mutation_cost
            self.update_values()
        else:
            message = f"Not enough mutation points to add {symptom.name}."
            return message

    def upgrade_symptom(self, symptom_name):
        """
        Upgrades a symptom of the Class given its name
        """
        if self.mutation_points >= self.symptoms[symptom_name].mutation_cost:
            new_level = self.symptoms[symptom_name].upgrade()
            self.update_values()
            self.mutation_points -= self.symptoms[symptom_name].mutation_cost
            return new_level
        error_msg = "Not enough mutation points to upgrade this symptom"
        return error_msg
    

    def update_values(self):
        """
        Updates the constants for the SIRD model we used
        """
        self.propagation = sum([self.symptoms[name].propagation_impact for name in self.symptoms.keys()])
        self.length_infection = self.infection_duration + sum([self.symptoms[name].duration_impact for name in self.symptoms.keys()])
        self.mortality_symptoms = sum([self.symptoms[name].mortality_impact for name in self.symptoms.keys()])

        self.transmission_rate = 0.3*th((self.propagation)/10)
        self.healing_rate = 1/(50*th((self.length_infection)/10))
        self.mortality_rate = 0.1*th(self.mortality_symptoms/10)
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
        message = f"Virus {self.name}: Propagation={self.propagation}, Infection Duration={self.infection_duration}, Mutation points={self.mutation_points}"
        # print(message)
        return message



class Symptom:
    def __init__(self, name, mutation_cost, duration_impact, propagation_impact, mortality_impact):
        """
        Initializes new symptoms to add to the virus
        """
        self.name = name
        self.mutation_cost = mutation_cost
        self.level = 0

        self.duration_impact0 = duration_impact
        self.propagation_impact0 = propagation_impact
        self.mortality_impact0 = mortality_impact

        self.duration_impact = 0
        self.propagation_impact = 0
        self.mortality_impact = 0
        

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
        if self.duration_impact > self.duration_impact0 :
            self.duration_impact += self.duration_impact0
        return self.level


