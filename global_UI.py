from PyQt5.QtWidgets import QMainWindow, QTabWidget
from PyQt5.QtCore import Qt
from main_tab import MainTab
from graph_tab import GraphTab
from gamedata import GameData
from history import GameHistory

class Game(QMainWindow): 
    def __init__(self, filename = "royaume_uni", maxturns = 20):
        """
        Constructor that instantly launches the game when called.
        """
        super().__init__()
        self.setWindowTitle("Serious Game: Supervirus")
        self._data = GameData(filename, maxturns)
        self._history = GameHistory(maxturns, self._data)
        self.filename = filename
        self._build_ui()
    
    def _build_ui(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.tab1 = MainTab(self.filename, self._data, self, self._history)
        self.tab2 = GraphTab(self._data)
        self.tabs.addTab(self.tab1, "Main Menu")
        self.tabs.addTab(self.tab2, "Detailed Infographics")
    
    def update(self):
        self.tab1.update_all_views()
        self.tab2.update_plot()
        if self._data.turn == self._data.maxturns:
            self._history.export_file()
            self.close()
        return





