import game_UI
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
game = game_UI.Menu("royaume_uni")
game.show()
sys.exit(app.exec_())
