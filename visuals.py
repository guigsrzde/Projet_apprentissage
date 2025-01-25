from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt
from gamedata import GameData

class GameMap:
    def __init__(self, filename, parent_widget):
        self.image_label = QLabel(parent_widget)
        self.pixmap = QPixmap((filename) + "/map.png")
        self.image_label.setPixmap(self.pixmap)

        self._imheight = self.pixmap.size().height()
        self._imwidth = self.pixmap.size().width()

        self.image_label.setScaledContents(True)  # Easy rescale

    # def attach_to_label(self, label: QLabel):
    #     """
    #     Attaches the map pixmap to a QLabel for display.
    #     :param label: QLabel instance where the map will be rendered.
    #     """
    #     label.setPixmap(self.pixmap)
    #     label.setScaledContents(True)  # Allow scaling based on widget size.

    def update_city_status(self, city):
        """
        Draws a visual marker on the map to indicate the city's infection status.
        :param city: A city object with coordinates and infection state.
        """
        painter = QPainter(self.pixmap)
        x, y = city.coord_x, city.coord_y
        color = QColor("red") if city.is_infected() else QColor("green")
        pen = QPen(color, 5, Qt.SolidLine)
        painter.setPen(pen)
        radius = 10
        painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)
        painter.end()

class RightColumnInformations:
    def __init__(self, complete_data: GameData):
        self._info_labels = {}
        layout = QVBoxLayout()
        town = complete_data.cities[complete_data.selected_city]

        # Create labels and store references
        self._info_labels['upgrade_points'] = QLabel(f"Points available to upgrade virus: {complete_data.virus.mutation_points}")
        self._info_labels['virus_name'] = QLabel(f"Virus name: {complete_data.virus.name}")
        self._info_labels['virus_name'].setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        self._info_labels['virus_propagation'] = QLabel(f"Virus Propagation factor: {complete_data.virus.propagation}")
        self._info_labels['virus_resistance'] = QLabel(f"Virus Infection Duration factor: {complete_data.virus.infection_duration}")
        self._info_labels['virus_mortality'] = QLabel(f"Virus Mortality factor: {complete_data.virus.mortality_rate}")

        for symptom in complete_data.virus.symptoms.keys():
            name = str(complete_data.virus.symptoms[symptom].name)
            self._info_labels[f'virus_symptoms_{name}'] = QLabel(f"Virus Symptom {name} factor: {complete_data.virus.symptoms[symptom].level}")
        self._info_labels['selected_city'] = QLabel(f"Selected city info:")
        self._info_labels['city_name'] = QLabel(f"{town.name}")
        self._info_labels['selected_city'].setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
        self._info_labels['city_population'] = QLabel(f"Initial Population: {town.pop}")
        self._info_labels['city_infected'] = QLabel(f"Infected: {int(town.infected[-1]*town.pop+0.1)} people, {int(town.infected[-1])*100/town.pop}%")
        self._info_labels['city_dead'] = QLabel(f"Dead: {int(town.dead[-1]*town.pop+0.1)} people, {int(10000*town.dead[-1])/100}%")
        self._info_labels['city_healthy'] = QLabel(f"Healthy: {int(town.healthy[-1]*town.pop+0.1)} people, {int(10000*town.healthy[-1])/100}%")
        self._info_labels['city_recovered'] = QLabel(f"Recovered: {int(town.recovered[-1]*town.pop+0.1)} people, {int(10000*town.recovered[-1])/100}%")
        self._info_labels['turn_number'] = QLabel(f"Turn number: {complete_data.turn}")
        
        # Add labels to layout
        for label in self._info_labels.values():
            layout.addWidget(label)
        
        container = QWidget()
        container.setLayout(layout)
        self.box = container

    def update_labels(self, data:GameData):
        """
        Updates the displayed information based on the current game state.
        :param data: GameData object containing overall game state.
        :param selected_city: The currently selected city object.
        """
        virus = data.virus
        self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {virus.mutation_points}")
        self._info_labels['virus_name'].setText(f"Virus name: {virus.name}")
        self._info_labels['virus_propagation'].setText(f"Virus Propagation factor: {virus.propagation}")
        self._info_labels['virus_resistance'].setText(f"Virus Infection Duration factor: {virus.infection_duration}")
        self._info_labels['virus_mortality'].setText(f"Virus Mortality factor: {virus.mortality_rate}")

        selected_city = data.cities[data.selected_city]
        # Update city-specific information.
        self._info_labels['city_name'].setText(f"{selected_city.name}")
        self._info_labels['city_population'].setText(f"Initial Population: {selected_city.pop}")
        self._info_labels['city_infected'].setText(
            f"Infected: {int(selected_city.infected[-1]*selected_city.pop+0.1)} people, {int(10000*selected_city.infected[-1])/100}%")
        self._info_labels['city_dead'].setText(
            f"Dead: {int(selected_city.dead[-1]*selected_city.pop+0.1)} people, {int(10000*selected_city.dead[-1])/100}%")
        self._info_labels['city_healthy'].setText(
            f"Healthy: {int(selected_city.healthy[-1]*selected_city.pop+0.1)} people, {int(10000*selected_city.healthy[-1])/100}%")
        self._info_labels['city_recovered'].setText(
            f"Recovered: {int(selected_city.recovered[-1]*selected_city.pop+0.1)} people, {int(10000*selected_city.recovered[-1])/100}%")
        self._info_labels['turn_number'].setText(f"Turn number: {data.turn}")

class BottomRowInformations:
    def __init__(self):
        """
        Handles the display of bottom row messages (e.g., errors, warnings).
        """
        self._error_label = QLabel()
        self._unexpected_event_label = QLabel("You will be warned of unexpected events here.")

    def update_labels(self, data):
        """
        Updates the displayed messages based on the current turn.
        :param data: GameData object containing overall game state.
        """
        if data.turn < data.maxturns + 1:
            self._error_label.setText(data.messages[data.turn][-1])