from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt
from gamedata import GameData
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphTab(QWidget):
    def __init__(self, complete_data: GameData):
        super().__init__()
        self._grid = QGridLayout()
        self.setLayout(self._grid)
        
        # Add Update Button
        self.update_button = QPushButton("Update Graphs")
        self.update_button.clicked.connect(self.update_plot)
        self._grid.addWidget(self.update_button, 1, 0, 1, 1)
        
        # Initialize the figure and canvas
        self.figure = Figure(figsize=(30, 20))
        self.canvas = FigureCanvas(self.figure)
        self._grid.addWidget(self.canvas, 0, 0, 1, 1)
        
        # Store the data
        self._data = complete_data
        
        # Initial plot
        self.update_plot()

    def update_plot(self):
        # Clear previous plots
        self.figure.clear()
        
        n = self._data.ncities
        nrows = int(n ** (1 / 2))
        ncols = nrows
        while nrows * ncols < n:
            nrows += 1
        
        # Create subplots within the existing figure
        ax = self.figure.subplots(nrows, ncols)
        
        # Plot data for each city
        for k in range(n):
            town = self._data.cities[k]
            row, col = k // ncols, k % ncols
            
            # Plot the data
            ax[row][col].plot(town.healthy, label='healthy')
            ax[row][col].plot(town.infected, label='infected')
            ax[row][col].plot(town.recovered, label='recovered')
            ax[row][col].plot(town.dead, label='dead')
            ax[row][col].legend()
            ax[row][col].set_title(town.name)
            ax[row][col].grid()

        # Turn off axes for extra subplots if necessary
        for k in range(n, nrows * ncols):
            row, col = k // ncols, k % ncols
            ax[row][col].axis('off')
        
        # Redraw the canvas
        self.canvas.draw()
