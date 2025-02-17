from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout
from gamedata import GameData
from visuals_graphs import Graphs

class GraphTab(QWidget):
    def __init__(self, complete_data: GameData):
        super().__init__()
        self._grid = QGridLayout()
        self.setLayout(self._grid)
        
        
        # Initialize the figure and canvas
        self.graphs = Graphs()
        self._grid.addWidget(self.graphs.canvas, 0, 0, 1, 1)
        
        # Store the data
        self._data = complete_data
        
        # Initial plot
        self.update_plot()

    def update_plot(self):
        self.graphs.update_plot(self._data.cities)
        return
