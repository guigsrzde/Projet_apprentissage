from PyQt5.QtWidgets import QApplication
from global_UI import Game
from sys import exit, argv


app = QApplication(argv)
game = Game(filename="royaume_uni")
game.show()
exit(app.exec_())
