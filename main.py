import affichage_principal
import virus
import sys
from PyQt5.QtWidgets import QApplication

toux = virus.Symptom("Toux", gravite=2, cout_mutation=3, impact_propagation=1, impact_mortalite=0)
fievre = virus.Symptom("Fièvre", gravite=3, cout_mutation=5, impact_propagation=2, impact_mortalite=1)
mort = virus.Symptom("Mort", gravite=10, cout_mutation=8, impact_propagation=0, impact_mortalite=5)

# Créer un virus
virus = virus.Virus("SuperVirus", propagation=1, resistance=1, points_mutation=10)

# Afficher les stats initiales
virus.afficher_stats()

# Ajouter des symptômes
virus.ajouter_symptome(toux)  # Devrait fonctionner
virus.ajouter_symptome(fievre)  # Devrait fonctionner si les points suffisent
virus.ajouter_symptome(mort)  # Peut échouer si les points sont insuffisants

# Afficher les symptômes et stats après les évolutions
virus.afficher_symptomes()
virus.afficher_stats()


app = QApplication(sys.argv)
jeu = affichage_principal.Menu("royaume_uni")
jeu.show()
sys.exit(app.exec_())
