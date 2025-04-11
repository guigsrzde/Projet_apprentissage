from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Graphs:
    def __init__(self):
        self.figure = Figure(figsize=(30, 20))
        self.canvas = FigureCanvas(self.figure)

    def update_plot(self, list_cities):
        # Clear previous plots
        self.figure.clear()

        # Filter the list of cities to only include those where town.is_infected() is True
        visible_cities = [town for town in list_cities if town.is_infected()]

        # Check if there are any visible cities
        if not visible_cities:
            # Optionally, display a message or handle the empty case
            self.figure.text(0.5, 0.5, 'No cities to display', ha='center', va='center', fontsize=20)
            self.canvas.draw()
            return

        # Determine the optimal grid size for visible cities
        n = len(visible_cities)
        nrows = int(n ** (1 / 2))
        ncols = nrows
        while nrows * ncols < n:
            nrows += 1

        ax = self.figure.subplots(nrows, ncols, squeeze=False)

        for k in range(n):
            town = visible_cities[k]
            row, col = k // ncols, k % ncols
            ax[row][col].plot(town.healthy, label='healthy')
            ax[row][col].plot(town.infected, label='infected')
            ax[row][col].plot(town.recovered, label='recovered')
            ax[row][col].plot(town.dead, label='dead')

            #### marche pas encore if town.first_infection_turn is not None:
                #### ax[row][col].plot(town.first_infection_turn, 0, 'ro', markersize=20, label='First infection')
             
            ax[row][col].legend()
            ax[row][col].set_title(town.name)
            ax[row][col].grid()

        # Turn off axes for extra subplots
        for k in range(n, nrows * ncols):
            row, col = k // ncols, k % ncols
            ax[row][col].axis('off')

        self.canvas.draw()
