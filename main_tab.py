from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, QMainWindow, QTabWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import parser
from matplotlib import pyplot as plt
from gamedata import GameData

class MainTab(QWidget):
    def __init__(self, filename:str, complete_data:GameData):
        self._game_map = filename
        self._data = complete_data
        super().__init__()
        self._build_ui()
    
    def _add_pixmap(self):
        """
        Adds the map to the QGridLayout. Called in _build_ui().
        """
        n_row = len(self._data.cities)
        n_col = len(self._data.virus.symptoms)

        self.pixmap = QPixmap(str(self._game_map) + "/map.png")  
        self.image_label.setPixmap(self.pixmap)

        self._imheight = self.pixmap.size().height()
        self._imwidth = self.pixmap.size().width()

        self.image_label.setScaledContents(True) #easy rescale
        
        self._grid.addWidget(self.image_label, 0, 0, n_row, n_col) # Add the QLabel to the grid layout
        return

    def _add_button(self, text, row, col, cb):
        """
        Creates a button at (row, col) in the QGridLayout().
        """
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding)  # Make buttons resizable
        self._grid.addWidget(button, row, col)
        button.clicked.connect(cb)
        return

    def _add_button_value(self, text, row, col, cb, index=0):
        """
        Creates a button for a specific city at (row, col) in the QGridLayout().
        """
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding)
        self._grid.addWidget(button, row, col)
        button.customValue = index
        button.clicked.connect(lambda _, obj=button.customValue: cb(obj))
        return
    
    def _add_all_buttons(self):
        """
        Creates all buttons needed for the game. Called in _build_ui().
        """
        n_row = len(self._data.cities)
        n_col = len(self._data.virus.symptoms)
        button_col=0

        for sympt in self._data.virus.symptoms.keys():
            self._add_button_value(f"Symptom: {self._data.virus.symptoms[sympt].name}", n_row, button_col, self._click_symptom, sympt)
            button_col+=1

        # Add buttons for each city on the right
        for i in range(n_row):
            self._add_button_value(self._data.cities[i].name, i, n_col, self._click_city, i)

        self._add_button("Continue Game", n_row, n_col, self._click_time)
        return
    
    def _create_info_boxes(self):
        """
        Creates and displays the info box with labels for game details.
        Stores references to the labels in a dictionary for later updates.
        """
        self._info_labels = {}
        layout = QVBoxLayout()
        town = self._data.cities[self._data.selected_city]
        

        # Create labels and store references
        self._info_labels['upgrade_points'] = QLabel(f"Points available to upgrade virus: {self._data.virus.mutation_points}")
        self._info_labels['virus_name'] = QLabel(f"Virus name: {self._data.virus.name}")
        self._info_labels['virus_name'].setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        self._info_labels['virus_propagation'] = QLabel(f"Virus Propagation factor: {self._data.virus.propagation}")
        self._info_labels['virus_resistance'] = QLabel(f"Virus Infection Duration factor: {self._data.virus.infection_duration}")
        self._info_labels['virus_mortality'] = QLabel(f"Virus Mortality factor: {self._data.virus.mortality_rate}")

        for symptom in self._data.virus.symptoms.keys():
            name = str(self._data.virus.symptoms[symptom].name)
            self._info_labels[f'virus_symptoms_{name}'] = QLabel(f"Virus Symptom {name} factor: {self._data.virus.symptoms[symptom].level}")
        self._info_labels['selected_city'] = QLabel(f"Selected city info:")
        self._info_labels['city_name'] = QLabel(f"{town.name}")
        self._info_labels['selected_city'].setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
        self._info_labels['city_population'] = QLabel(f"Initial Population: {town.pop}")
        self._info_labels['city_infected'] = QLabel(f"Infected: {int(town.infected[-1]*town.pop+0.1)} people, {int(town.infected[-1])*100/town.pop}%")
        self._info_labels['city_dead'] = QLabel(f"Dead: {int(town.dead[-1]*town.pop+0.1)} people, {int(10000*town.dead[-1])/100}%")
        self._info_labels['city_healthy'] = QLabel(f"Healthy: {int(town.healthy[-1]*town.pop+0.1)} people, {int(10000*town.healthy[-1])/100}%")
        self._info_labels['city_recovered'] = QLabel(f"Recovered: {int(town.recovered[-1]*town.pop+0.1)} people, {int(10000*town.recovered[-1])/100}%")
        self._info_labels['turn_number'] = QLabel(f"Turn number: {self._data.turn}")
        
        # Add labels to layout
        for label in self._info_labels.values():
            layout.addWidget(label)
        
        n_row = len(self._data.cities)
        n_col = len(self._data.virus.symptoms)

        container = QWidget()
        container.setLayout(layout)
        self._grid.addWidget(container, 0, n_col+1, n_row, 1)
        return
    
    def _other_messages_box(self):
        """
        Displays error messages for the player.
        """
        self._error_label = QLabel(self._data.messages[self._data.turn][0])
        self._grid.addWidget(self._error_label, len(self._data.cities) + 2, 0, 1, 5)
        self._unexpected_event_label = QLabel("You will be warned of unexpected events here")
        self._grid.addWidget(self._unexpected_event_label, len(self._data.cities) + 3, 0, 1, 5)
        return
    
    def _build_ui(self):
        """
        Creates the Game UI: showing the game map, creating buttons to play, 
        and adding text boxes to display necessary information.
        """
        self
        self.setWindowTitle("Serious Game: Can you end mankind?")
        self._grid = QGridLayout()
        self.setLayout(self._grid)
        self.image_label = QLabel(self)

        # Add all elements to the grid layout
        self._add_pixmap()
        self._add_all_buttons()
        self._create_info_boxes()
        self._other_messages_box()
        return
    
    def update_all_labels(self):
        self._click_city(self._data.selected_city)
        self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._data.virus.mutation_points}")
        self._info_labels['virus_propagation'].setText(f"Virus Propagation factor: {self._data.virus.propagation}")
        self._info_labels['virus_resistance'].setText(f"Virus Infection Duration factor: {self._data.virus.infection_duration}")
        self._info_labels['virus_mortality'].setText(f"Virus Mortality factor: {self._data.virus.mortality_rate}")
        self._info_labels['turn_number'].setText(f"Turn number: {self._data.turn}")
        if self._data.turn < self._data.maxturns + 1:
            self._error_label.setText(self._data.messages[self._data.turn][-1])
        return
    
    def update_city_status(self, city):
        painter = QPainter(self.pixmap)
        x, y = city.coord_x, city.coord_y   
        if city.is_infected() > 0:  # If there are infections
            color = QColor("red")
        else:  # If there are no infections
            color = QColor("green")
        pen = QPen(color, 5, Qt.SolidLine)
        painter.setPen(pen)
        radius = 10  
        painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)
        painter.end()

    def _click_symptom(self, index):
        self._data.click_symptom(index)
        self.update_all_labels()
        return
    
    def _click_city(self, index):
        """
        Updates the info box when a new city is selected.
        """
        self._data.selected_city = index
        town = self._data.cities[index]
        self._info_labels['city_name'].setText(f"{town.name}")
        self._info_labels['city_population'].setText(f"Initial Population: {town.pop}")
        self._info_labels['city_infected'].setText(f"Infected: {int(town.infected[-1]*town.pop+0.1)} people, {int(10000*town.infected[-1])/100}%")
        self._info_labels['city_dead'].setText(f"Dead: {int(town.dead[-1]*town.pop+0.1)} people, {int(10000*town.dead[-1])/100}%")
        self._info_labels['city_healthy'].setText(f"Healthy: {int(town.healthy[-1]*town.pop+0.1)} people, {int(10000*town.healthy[-1])/100}%")
        self._info_labels['city_recovered'].setText(f"Recovered: {int(town.recovered[-1]*town.pop+0.1)} people, {int(10000*town.recovered[-1])/100}%")
        return
    
    def _click_time(self):
        """
        Increments the turn number and updates the corresponding label.
        """
        self._data.click_turn()
        self.update_all_labels()
        for town in self._data.cities:
            self.update_city_status(town)
        if self._data.turn > self._data.maxturns:
            self.parent().close()
        return
