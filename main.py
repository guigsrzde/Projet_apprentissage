import affichage_principal
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
jeu = affichage_principal.Menu("royaume_uni")
jeu.show()
sys.exit(app.exec_())
