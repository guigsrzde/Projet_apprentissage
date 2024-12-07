from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import parser
import virus


class Menu(QWidget):
    def __init__(self, filename):
        self._cities = parser.get_list_from_file(filename + "/cities.py", "list_cities")
        print(self._cities[0].name)
        self._game_map = filename
        self._virus = virus.Virus("SuperVirus")
        self._resize = 0
        self._xmin = 0
        self._ymin = 0
        super().__init__()
        self._build_ui()
        self.resize(500, 256)

    def _add_button(self, text, row, col, cb, object = None):
        button = QPushButton(text)
        button.setSizePolicy(button.sizePolicy().Expanding, button.sizePolicy().Expanding) # Make buttons resizable
        self._grid.addWidget(button, row, col)  # Add the button to the grid
        button.customValue = object
        button.clicked.connect(lambda: cb(button.customValue))

    def _build_ui(self):
        self.setWindowTitle("Serious Game: Réussiras-tu à faire disparaître l'humanité")
        self._grid = QGridLayout()  # Create a QGridLayout
        self.setLayout(self._grid)  # Set the QGridLayout as the main layout of the window
        self.image_label = QLabel(self)

        # Load an image using QPixmap
        self.pixmap = QPixmap(str(self._game_map) + "/map.png")  # Replace with your image path

        # Set the image to the QLabel
        self.image_label.setPixmap(self.pixmap)

        self._resize = self.pixmap.size().height() / self.pixmap.size().width()
        self._xmin = 100
        self._ymin = int(self._xmin*self._resize*3/2)

        # Optional: Resize the image to fit the label size
        self.image_label.setScaledContents(True)  # Makes sure the image scales to fit the label

        # Add the QLabel to the grid layout (position 0, 0)
        
        self._grid.addWidget(self.image_label, 0, 0, 4, len(self._cities))

        # Add buttons on the right side (column 3)
        self._add_button("Infos Virus", 0, len(self._cities), self._click_virus, self._virus)
        self._add_button("Resistance", 1, len(self._cities), self._click_resistance, self._virus)
        self._add_button("Symptome", 2, len(self._cities), self._click_symptome, self._virus)
        self._add_button("Propagation", 3, len(self._cities), self._click_propagation, self._virus)

        #self.resize_image_to_window(self.width(), self.height())

        
        for i in range(len(self._cities)):
            self._add_button(self._cities[i].name, 4, i,self._click_ville, self._cities[i])
        
        #self._grid.setColumnStretch(0, 2)  # Column 0 (image) gets 2x more space
        #self._grid.setColumnStretch(1, 1)  # Column 1 (buttons) gets 1x space

    def _click_virus(self, value):
        print(f"voici les infos sur le {value.nom}")

    def _click_propagation(self, value):
        print("Click de propagation")

    def _click_resistance(self, value):
        print("Click de resistance")

    def _click_symptome(self, value):
        print("Click de symptome")

    def _click_ville(self, value):
        print(value.name)

    def resizeEvent(self, event):
        """
        This method will be called whenever the window is resized.
        We can use this to scale the image appropriately.
        """
        width = event.size().width()
        height = event.size().height()
        resized_width = height * self._resize
        resized_height = width / self._resize


        # Ensure the image doesn't scale below the threshold
        new_width = int(max(self._xmin, min(width,resized_width)))
        new_height = int(max(self._ymin, min(height, resized_height)))

        # Resize the pixmap based on the new window size
        scaled_pixmap = self.pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio)

        # Set the scaled pixmap to the QLabel
        self.image_label.setPixmap(scaled_pixmap)

        # Optionally call the base class's resizeEvent to ensure the layout behaves properly
        super().resizeEvent(event)
