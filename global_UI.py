from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QMainWindow, QTabWidget
from PyQt5.QtCore import Qt
from main_tab import MainTab
from graph_tab import GraphTab
from gamedata import GameData

class Game(QMainWindow):
    def __init__(self, filename = "royaume_uni", maxturns = 20):
        """
        Constructor that instantly launches the game when called.
        """
        super().__init__()
        self.setWindowTitle("Serious Game: Supervirus")
        self._data = GameData(filename, maxturns)
        self.filename = filename
        self._build_ui()
    
    def _build_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = MainTab(self.filename, self._data)
        self.tab2 = GraphTab(self._data)
        self.tabs.addTab(self.tab1, "Main Menu")
        self.tabs.addTab(self.tab2, "Detailed Infographics")





