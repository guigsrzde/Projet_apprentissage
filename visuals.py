from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, pyqtSignal
from gamedata import GameData

class GameMap():
    def __init__(self, filename, parent_widget):
        self.layout = QVBoxLayout()
        self.image_label = ClickableLabel(parent_widget)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.pixmap = QPixmap(filename + "/map.png")
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)
        container = QWidget()
        container.setLayout(self.layout)
        self.image = container


        self._imheight = self.pixmap.size().height()
        self._imwidth = self.pixmap.size().width()

    def update_city_status(self, city, id_selected):
        """
        Draws a visual marker on the map to indicate the city's infection status.
        :param city: A city object with coordinates and infection state.
        """
        painter = QPainter(self.pixmap)
        x, y = city.x, city.y
        if city.is_infected() and ((int(city.infected[-1]) * 100 / city.pop) > 0.0):
            color = QColor("red")
        elif not city.is_infected():
            color = QColor("green")
        elif city.is_infected() and ((int(city.infected[-1]) * 100 / city.pop) == 0.0):
            color = QColor("red")        

        radius = 10

        # First, draw a filled black circle
        if city.id == id_selected:
            painter.setBrush(QColor("white"))
        else:
            painter.setBrush(QColor("black"))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)

        # Then draw the colored outline on top
        painter.setBrush(Qt.NoBrush)
        pen = QPen(color, 5, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)

        self.image_label.setPixmap(self.pixmap)
        self.image_label.update()
        painter.end()



class RightColumnInformations:
    def __init__(self, complete_data: GameData):
        self._info_labels = {}
        layout = QVBoxLayout()
        town = complete_data.cities[0]

        # Create labels and store references
        self._info_labels['upgrade_points'] = QLabel(f"Points available to upgrade virus: {complete_data.virus.mutation_points}")
        self._info_labels['virus_name'] = QLabel(f"Virus name: {complete_data.virus.name}")
        self._info_labels['virus_name'].setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        self._info_labels['virus_propagation'] = QLabel(f"Virus Propagation factor: {complete_data.virus.propagation}")
        self._info_labels['virus_resistance'] = QLabel(f"Virus Infection Duration factor: {complete_data.virus.infection_duration}")
        self._info_labels['virus_mortality'] = QLabel(f"Virus Mortality factor: {complete_data.virus.mortality_symptoms}")

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
        self._info_labels['score'] = QLabel(f"Current score : {complete_data.score_function1()}")

        self._info_labels['score'].setStyleSheet("font-weight: bold; font-size: 28px; color: orange;")
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
        self._info_labels['virus_mortality'].setText(f"Virus Mortality factor: {virus.mortality_symptoms}")
        for name in data.virus.symptoms.keys():
            self._info_labels[f'virus_symptoms_{name}'].setText(f"Virus Symptom {name} factor: {data.virus.symptoms[name].level}")

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
        self._info_labels['score'].setText(f"Current score : {data.score_function1()}")

class BottomRowInformations:
    def __init__(self):
        """
        Handles the display of bottom row messages (e.g., errors, warnings).
        """
        self._error_label = QLabel()
        self._unexpected_event_label = QLabel()

    def update_labels(self, data:GameData):
        """
        Updates the displayed messages based on the current turn.
        :param data: GameData object containing overall game state.
        """
        if data.turn < data.maxturns + 1:
            self._error_label.setText(data.messages_err[data.turn][-1])
            self._unexpected_event_label.setText(data.messages_evt[data.turn][-1])

class ClickableLabel(QLabel):
    clicked = pyqtSignal(int,int)

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            x = ev.pos().x()
            y = ev.pos().y()
            self.clicked.emit(x,y)