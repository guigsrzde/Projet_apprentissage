from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Graphs():
    def __init__(self):
        self.figure = Figure(figsize=(30, 20))
        self.canvas = FigureCanvas(self.figure)
        return
    
    def update_plot(self, list_cities):
        # Clear previous plots
        self.figure.clear()
        
        #Determine the optimal grid size
        n = len(list_cities)
        nrows = int(n ** (1 / 2))
        ncols = nrows
        while nrows * ncols < n:
            nrows += 1

        ax = self.figure.subplots(nrows, ncols)
        for k in range(n):
            town = list_cities[k]
            row, col = k // ncols, k % ncols
            ax[row][col].plot(town.healthy, label='healthy')
            ax[row][col].plot(town.infected, label='infected')
            ax[row][col].plot(town.recovered, label='recovered')
            ax[row][col].plot(town.dead, label='dead')
            ax[row][col].legend()
            ax[row][col].set_title(town.name)
            ax[row][col].grid()
        # Turn off axes for extra subplots
        for k in range(n, nrows * ncols):
            row, col = k // ncols, k % ncols
            ax[row][col].axis('off')

        self.canvas.draw()
        return