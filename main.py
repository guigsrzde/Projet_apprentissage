import affichage_principal
import virus
import sys
from PyQt5.QtWidgets import QApplication

print(sys.version)

print("Hello!")
virus.affiche()
virus()

app = QApplication(sys.argv)
jeu = affichage_principal.Menu()
jeu.show()
sys.exit(app.exec_())
