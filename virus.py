def virus():
    print("ok virus")
    return 0


class Virus:
    def __init__(self, nom, propagation=1, resistance=1, points_mutation=10):
        self.nom = nom
        self.symptomes = []  # Liste des symptômes actifs
        self.propagation = propagation  # Propagation de base
        self.resistance = resistance  # Résistance de base
        self.points_mutation = points_mutation  # Points pour évoluer

    def ajouter_symptome(self, symptome):
        if self.points_mutation >= symptome.cout_mutation:
            self.symptomes.append(symptome)
            self.propagation += symptome.impact_propagation
            self.resistance += symptome.impact_mortalite
            self.points_mutation -= symptome.cout_mutation
            print(f"{symptome.nom} ajouté ! Propagation : {self.propagation}, Résistance : {self.resistance}. Points restants : {self.points_mutation}")
        else:
            print(f"Pas assez de points pour ajouter {symptome.nom}.")

    def intensifier(self, caracteristique, valeur):
        if self.points_mutation >= valeur:
            setattr(self, caracteristique, getattr(self, caracteristique) + valeur)
            self.points_mutation -= valeur
            print(f"{caracteristique.capitalize()} augmenté à {getattr(self, caracteristique)}. Points restants : {self.points_mutation}")
        else:
            print("Pas assez de points de mutation.")

    def afficher_symptomes(self):
        print(f"Symptômes du virus {self.nom}:")
        for symptome in self.symptomes:
            symptome.afficher_details()

    def afficher_stats(self):
        print(f"Virus {self.nom}: Propagation={self.propagation}, Résistance={self.resistance}, Points mutation={self.points_mutation}")




class Symptom:
    def __init__(self, nom, gravite, cout_mutation, impact_propagation, impact_mortalite):
        self.nom = nom
        self.gravite = gravite
        self.cout_mutation = cout_mutation
        self.impact_propagation = impact_propagation
        self.impact_mortalite = impact_mortalite

    def afficher_details(self):
        print(f"{self.nom} - Gravité: {self.gravite}, Coût: {self.cout_mutation}, Propagation: {self.impact_propagation}, Mortalité: {self.impact_mortalite}")
