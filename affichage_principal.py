from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import parser
import virus


class Menu(QWidget):
    def __init__(self, filename):
        """
        Constructor that instantly launches the game when called
        """
        self._cities = parser.get_list_from_file(filename + "/cities.py", "list_cities")
        self._game_map = filename
        self._virus = virus.Virus("SuperVirus")
        self._resize = 0
        self._xmin = 0
        self._ymin = 0
        self._tour = 0
        super().__init__()
        self._build_ui()
        #self.resize(500, 256)
    
    def _add_pixmap(self):
        """
        This method adds the map to the QGridLayout. It is called in _build_ui().
        """
        n_cities = len(self._cities)

        # Load an image using QPixmap
        self.pixmap = QPixmap(str(self._game_map) + "/map.png")  # Replace with your image path

        # Set the image to the QLabel
        self.image_label.setPixmap(self.pixmap)
        self._resize = self.pixmap.size().height() / self.pixmap.size().width()
        self._xmin = 100
        self._ymin = int(self._xmin*self._resize*3/2)

        # Resize the image to fit the label size
        self.image_label.setScaledContents(True)  # Makes sure the image scales to fit the label

        # Add the QLabel to the grid layout (position 0, 0)
        self._grid.addWidget(self.image_label, 0, 0, n_cities, 3)

    def _add_button(self, text, row, col, cb):
        """
        Function that creates a text box in (row, col) of the QGridLayout()
        """
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding) # Make buttons resizable
        self._grid.addWidget(button, row, col)  # Add the button to the grid
        button.clicked.connect(cb)
    
    def _add_button_city(self, text, row, col, cb, index=0):
        """
        Function that creates a text box in (row, col) of the QGridLayout()
        """
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding) # Make buttons resizable
        self._grid.addWidget(button, row, col)  # Add the button to the grid
        button.customValue = index
        button.clicked.connect(lambda _, obj=button.customValue: cb(obj))
    
    def _add_all_buttons(self):
        """
        This method creates all buttons needed for the game. It is called in _build_ui()
        """

        n_cities = len(self._cities)

        # Add buttons on the bottom
        self._add_button("Propagation", n_cities, 0, self._click_propagation)
        self._add_button("Resistance", n_cities, 1, self._click_resistance)
        self._add_button("Symptome", n_cities, 2, self._click_symptome)

        # Add buttons on the right side
        for i in range(n_cities):
            self._add_button_city(self._cities[i].name, i, 4, self._click_ville, i)
        
        self._add_button("Continue Game", n_cities, 4, self._click_time)
    
    def _create_info_boxes(self):
        """
        Create and display the info box with labels for game details.
        Stores references to the labels in a dictionary for later updates.
        """
        self._info_labels = {}  # Dictionary to store references to labels
        layout = QVBoxLayout()
        ville = self._cities[0]

        # Create labels and store them in the dictionary
        self._info_labels['upgrade_points'] = QLabel(f"Points available to upgrade virus: {self._virus.points_mutation}")
        self._info_labels['virus_name'] = QLabel(f"Virus name: {self._virus.nom}")
        self._info_labels['virus_propagation'] = QLabel(f"Virus Propagation factor: {self._virus.propagation}")
        self._info_labels['virus_resistance'] = QLabel(f"Virus Resistance factor: {self._virus.resistance}")
        self._info_labels['virus_symptoms'] = QLabel(f"Virus Symptom factor: {self._virus.symptomes}")
        self._info_labels['selected_city'] = QLabel(f"Selected city : {ville.name}")
        self._info_labels['city_population'] = QLabel(f"Initial Population : {ville.pop}")
        self._info_labels['city_infected'] = QLabel(f"Infected : {ville.infected}")
        self._info_labels['city_dead'] = QLabel(f"Dead : {ville.mort}")
        self._info_labels['turn_number'] = QLabel(f"Turn number : {self._tour}")

        # Add labels to the layout
        for label in self._info_labels.values():
            layout.addWidget(label)

        # Create a container and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Add the container to the grid
        self._grid.addWidget(container, 0, 5, len(self._cities) + 1, 1)

    def _other_messages_box(self):
        self._error_label = QLabel("No error message to display")
        self._grid.addWidget(self._error_label, len(self._cities)+2, 0, 1, 5)
        self._unexpected_event_label = QLabel("You will be warned of unexpected events here")
        self._grid.addWidget(self._unexpected_event_label, len(self._cities)+3, 0, 1, 5)

    def _build_ui(self):
        """
        Creates the Game UI: showing the game map and creating buttons to play the game,
        and add text boxes to display the needed information.
        """
        n_cities = len(self._cities)
        self.setWindowTitle("Serious Game: Réussiras-tu à faire disparaître l'humanité")
        self._grid = QGridLayout()  # Create a QGridLayout
        self.setLayout(self._grid)  # Set the QGridLayout as the main layout of the window
        self.image_label = QLabel(self)

        # Add all elements needed to the gridlayout
        self._add_pixmap()
        self._add_all_buttons()
        self._create_info_boxes()
        self._other_messages_box()

    def _click_propagation(self):
        if (self._virus.points_mutation > 0):
            self._virus.propagation += 1
            self._virus.points_mutation -= 1
            if hasattr(self, '_info_labels'):
                self._info_labels['virus_propagation'].setText(f"Virus Propagation factor: {self._virus.propagation}")
                self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._virus.points_mutation}")
            else:
                print("Info labels are not initialized!")
        else:
            self._error_label.setText("Not enough points available to upgrade the propagation on the virus")

    def _click_resistance(self):
        
        if (self._virus.points_mutation > 0):
            self._virus.resistance += 1
            self._virus.points_mutation -= 1
            if hasattr(self, '_info_labels'):
                self._info_labels['virus_resistance'].setText(f"Virus Resistance factor: {self._virus.resistance}")
                self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._virus.points_mutation}")
            else:
                print("Info labels are not initialized!")
        else:
            self._error_label.setText("Not enough points available to upgrade the resistance on the virus")

    def _click_symptome(self):
        if (self._virus.points_mutation > 0):
            self._virus.symptomes += 1
            self._virus.points_mutation -= 1
            if hasattr(self, '_info_labels'):
                self._info_labels['virus_symptoms'].setText(f"Virus Symptom factor: {self._virus.symptomes}")
                self._info_labels['upgrade_points'].setText(f"Points available to upgrade virus: {self._virus.points_mutation}")
            else:
                print("Info labels are not initialized!")
        else:
            self._error_label.setText("Not enough points available to upgrade the symptoms on the virus")

    def _click_ville(self, index):
        """
        Update the info box when a new city is selected.
        """
        ville = self._cities[index]
        print(index)
        if hasattr(self, '_info_labels'):
            self._info_labels['selected_city'].setText(f"Selected city : {ville.name}")
            self._info_labels['city_population'].setText(f"Initial Population : {ville.pop}")
            self._info_labels['city_infected'].setText(f"Infected : {ville.infected}")
            self._info_labels['city_dead'].setText(f"Dead : {ville.mort}")
        else:
            print("Info labels are not initialized!")
    
    def _click_time(self):
        """
        Increment the turn number and update the corresponding label.
        """
        self._tour += 1
        if hasattr(self, '_info_labels'):
            self._info_labels['turn_number'].setText(f"Turn number : {self._tour}")
        else:
            print("Info labels are not initialized!")

    def resizeEvent(self, event):
        """
        Rescale the image appropriately based on the window size.
        """
        width = event.size().width()
        height = event.size().height()
        
        # Respect minimum and maximum sizes for the image
        new_width = int(min(width, max(self._xmin, width * 0.8)))
        new_height = int(min(height, max(self._ymin, height * 0.8)))

        # Scale the pixmap while keeping the aspect ratio
        scaled_pixmap = self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)

        # Set the scaled pixmap to the QLabel
        self.image_label.setPixmap(scaled_pixmap)

        super().resizeEvent(event)  # Call the parent class method
