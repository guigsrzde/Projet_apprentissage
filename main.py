from global_UI import Game
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
game = Game()
game.show()
sys.exit(app.exec_())