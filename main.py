from affichage_principal import *
from virus import *

print(sys.version)

print("Hello!")
affiche()
virus()

app = QApplication(sys.argv)
jeu = Menu()
jeu.show()
sys.exit(app.exec_())