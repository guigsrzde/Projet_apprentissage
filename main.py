from affichage_principal import *
from virus import *

print("Hello!")
affiche()
virus()

app = widgets.QApplication(sys.argv)
jeu = Menu()
jeu.show()
sys.exit(app.exec_())