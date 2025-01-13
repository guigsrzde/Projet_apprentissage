from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import parser
import city
import virus
from matplotlib import pyplot as plt
from modele_propgation import SIRD_model

class Menu(QWidget):
    def __init__(self, filename, maxturns=10):
        """
        Constructor that instantly launches the game when called.
        """
        self._cities = parser.get_list_from_file(filename + "/cities.py", "list_cities")
        self._game_map = filename
        self._virus = virus.Virus("SuperVirus")
        self._resize = 0
        self._xmin = 0
        self._ymin = 0
        self._turn = 0
        self._maxturns = maxturns
        super().__init__()
        self._build_ui()
    
    def _add_pixmap(self):
        """
        Adds the map to the QGridLayout. Called in _build_ui().
        """
        n_row = len(self._cities)
        n_col = len(self._virus.symptoms) + 3

        # Load an image using QPixmap
        self.pixmap = QPixmap(str(self._game_map) + "/map.png")  # Replace with your image path

        # Set the image to the QLabel
        self.image_label.setPixmap(self.pixmap)
        self._resize = self.pixmap.size().height() / self.pixmap.size().width()
        self._xmin = 100
        self._ymin = int(self._xmin * self._resize * 3 / 2)

        # Resize the image to fit the label size
        self.image_label.setScaledContents(True)

        # Add the QLabel to the grid layout
        self._grid.addWidget(self.image_label, 0, 0, n_row, n_col)

    def _add_button(self, text, row, col, cb):
        """
        Creates a button at (row, col) in the QGridLayout().
        """
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding)  # Make buttons resizable
        self._grid.addWidget(button, row, col)
        button.clicked.connect(cb)

    def _add_button_value(self, text, row, col, cb, index=0):
        """
        Creates a button for a specific city at (row, col) in the QGridLayout().
        """
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding)
        self._grid.addWidget(button, row, col)
        button.customValue = index
        button.clicked.connect(lambda _, obj=button.customValue: cb(obj))

    def _add_all_buttons(self):
        """
        Creates all buttons needed for the game. Called in _build_ui().
        """
        n_row = len(self._cities)
        n_col = len(self._virus.symptoms) + 3

        # Add buttons at the bottom
        self._add_button("Propagation", n_row, 0, self._click_propagation)
        self._add_button("Resistance", n_row, 1, self._click_resistance)
        for i in range(len(self._virus.symptoms)):
            self._add_button_value(f"Symptom: {self._virus.symptoms[i].name}", n_row, 2 + i, self._click_symptom, i)

        # Add buttons for each city on the right
        for i in range(n_row):
            self._add_button_value(self._cities[i].name, i, n_col, self._click_city, i)

        self._add_button("Continue Game", n_row, n_col, self._click_time)

    def _create_info_boxes(self):
        """
        Creates and displays the info box with labels for game details.
        Stores references to the labels in a dictionary for later updates.
        """
        self._info_labels = {}
        layout = QVBoxLayout()
        town = self._cities[0]

        # Create labels and store references
        self._info_labels['upgrade_points'] = QLabel(f"Points available to upgrade virus: {self._virus.mutation_points}")
        self._info_labels['virus_name'] = QLabel(f"Virus name: {self._virus.name}")
        self._info_labels['virus_propagation'] = QLabel(f"Virus Propagation factor: {self._virus.propagation}")
        self._info_labels['virus_resistance'] = QLabel(f"Virus Resistance factor: {self._virus.resistance}")
        for symptom in self._virus.symptoms:
            name = str(symptom.name)
            self._info_labels[f'virus_symptoms_{name}'] = QLabel(f"Virus Symptom {name} factor: {symptom.level}")
        self._info_labels['selected_city'] = QLabel(f"Selected city: {town.name}")
        self._info_labels['city_population'] = QLabel(f"Initial Population: {town.pop}")
        self._info_labels['city_infected'] = QLabel(f"Infected: {int(town.infected[-1]*town.pop+0.1)} people, {int(10000*town.infected[-1])/100}%")
        self._info_labels['city_dead'] = QLabel(f"Dead: {int(town.dead[-1]*town.pop+0.1)} people, {int(10000*town.dead[-1])/100}%")
        self._info_labels['city_healthy'] = QLabel(f"Healthy: {int(town.healthy[-1]*town.pop+0.1)} people, {int(10000*town.healthy[-1])/100}%")
        self._info_labels['city_recovered'] = QLabel(f"Recovered: {int(town.recovered[-1]*town.pop+0.1)} people, {int(10000*town.recovered[-1])/100}%")
        self._info_labels['turn_number'] = QLabel(f"Turn number: {self._turn}")
        
        # Add labels to layout
        for label in self._info_labels.values():
            layout.addWidget(label)
        
        n_row = len(self._cities)
        n_col = len(self._virus.symptoms) + 3

        container = QWidget()
        container.setLayout(layout)
        self._grid.addWidget(container, 0, n_col+1, n_row, 1)#, 0, 5, len(self._cities) + 1, 1)

    def _other_messages_box(self):
        """
        Displays error messages for the player.
        """
        self._error_label = QLabel("No error message to display")
        self._grid.addWidget(self._error_label, len(self._cities) + 2, 0, 1, 5)
        self._unexpected_event_label = QLabel("You will be warned of unexpected events here")
        self._grid.addWidget(self._unexpected_event_label, len(self._cities) + 3, 0, 1, 5)

    def _build_ui(self):
        """
        Creates the Game UI: showing the game map, creating buttons to play, 
        and adding text boxes to display necessary information.
        """
        self.setWindowTitle("Serious Game: Can you end mankind?")
        self._grid = QGridLayout()
        self.setLayout(self._grid)
        self.image_label = QLabel(self)

        # Add all elements to the grid layout
        self._add_pixmap()
        self._add_all_buttons()
        self._create_info_boxes()
        self._other_messages_box()

    def _click_propagation(self):
        if self._virus.mutation_points > 0:
            self._virus.propagation += 1
            self._virus.transmission_rate = 1 - 1/self._virus.propagation
            self._virus.mutation_points -= 1
            self._info_labels['virus_propagation'].setText(f"Virus Propagation factor: {self._virus.propagation}")
            self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._virus.mutation_points}")
        else:
            self._error_label.setText("Not enough points available to upgrade the propagation of the virus.")

    def _click_resistance(self):
        if self._virus.mutation_points > 0:
            self._virus.resistance += 1
            self._virus.healing_rate = 1/resistance
            self._virus.mutation_points -= 1
            self._info_labels['virus_resistance'].setText(f"Virus Resistance factor: {self._virus.resistance}")
            self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._virus.mutation_points}")
        else:
            self._error_label.setText("Not enough points available to upgrade the resistance of the virus.")

    def _click_symptom(self, index):
        if self._virus.mutation_points > 0:
            symptom = self._virus.symptoms[index]
            self._virus.symptoms[index].upgrade()
            self._virus.mutation_points -= 1
            self._info_labels[f'virus_symptoms_{str(symptom.name)}'].setText(f"Virus Symptom {str(symptom.name)} factor: {symptom.level}")
            self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._virus.mutation_points}")
        else:
            self._error_label.setText(f"Not enough points available to upgrade the symptom {self._virus.symptoms[index].name} of the virus.")

    def _click_city(self, index):
        """
        Updates the info box when a new city is selected.
        """
        city = self._cities[index]
        self._info_labels['selected_city'].setText(f"Selected city: {city.name}")
        self._info_labels['city_population'].setText(f"Initial Population: {city.pop}")
        self._info_labels['city_infected'].setText(f"Infected: {city.infected}")
        self._info_labels['city_dead'].setText(f"Dead: {city.dead}")

    def _click_time(self):
        """
        Increments the turn number and updates the corresponding label.
        """
        self._turn += 1
        if self._turn == self._maxturns:
            self._error_label.setText("This is your last turn!")
        elif self._turn > self._maxturns:
            self.close()
            n = len(self._cities)
            n = int(n**(1/2))
            fig, ax = plt.subplots(n, n, figsize = (30,20))
            fig.suptitle("Global Evolution of your virus", fontsize = 28)
            for k in range(len(self._cities)):
                town = self._cities[k]
                row,col=k//n,k%n
                ax[row][col].plot(town.healthy,label = 'healthy')
                ax[row][col].plot(town.infected, label = 'infected')
                ax[row][col].plot(town.recovered, label = 'recovered')
                ax[row][col].plot(town.dead, label = 'dead')
                ax[row][col].set_title(town.name)
                ax[row][col].grid()
            plt.show()
        else:
            self._info_labels['turn_number'].setText(f"Turn number: {self._turn}")
        

    def resizeEvent(self, event):
        """
        Rescales the image based on window size.
        """
        width = event.size().width()
        height = event.size().height()

        new_width = int(min(width, max(self._xmin, width * 0.8)))
        new_height = int(min(height, max(self._ymin, height * 0.8)))

        scaled_pixmap = self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)

        super().resizeEvent(event)
