from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt
from gamedata import GameData
from visuals import GameMap, RightColumnInformations, BottomRowInformations



class MainTab(QWidget):
    def __init__(self, filename: str, complete_data: GameData):
        super().__init__()
        self._game_map = filename
        self._data = complete_data

        # Views
        self.map = GameMap(filename, self)
        self.map.image_label.setScaledContents(True)
        # self.map_view.attach_to_label(self.map_view.image_label)
        self.right_info_view = RightColumnInformations(self._data)
        self.bottom_info_view = BottomRowInformations()

        self._build_ui()
    
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
        button_col = 0

        # Add buttons for each virus symptom
        for sympt in self._data.virus.symptoms.keys():
            self._add_button_value(f"Symptom: {self._data.virus.symptoms[sympt].name}",n_row,button_col,self._click_symptom,sympt)
            button_col += 1

        # Add buttons for each city on the right
        for i in range(n_row):
            self._add_button_value(
                self._data.cities[i].name, i, n_col, self._click_city, i
            )

        # Add a "Continue Game" button
        self._add_button("Continue Game", n_row, n_col, self._click_time)
        return

    def _build_ui(self):
        """
        Creates the Game UI: showing the game map, creating buttons to play,
        and adding text boxes to display necessary information.
        """
        nsymptoms = len(self._data.virus.symptoms)
        self.setWindowTitle("Serious Game: Can you end mankind?")
        self._grid = QGridLayout()
        self.setLayout(self._grid)

        # Add the map to the layout
        self._grid.addWidget(self.map.image, 0, 0, self._data.ncities, nsymptoms)

        # Add all buttons to the layout
        self._add_all_buttons()
        
        # Add right column (information panel)
        self._grid.addWidget(self.right_info_view.box, 0, nsymptoms+1,self._data.ncities,1)

        # Add bottom row (messages)
        self._grid.addWidget(self.bottom_info_view._error_label, 1+self._data.ncities, 0, 1, nsymptoms)
        self._grid.addWidget(self.bottom_info_view._unexpected_event_label, 2+self._data.ncities, 0, 1, nsymptoms)

        self.update_all_views()

    def update_all_views(self):
        """
        Update all views based on the current state of the game data.
        """
        for city_name in self._data.cities:
            self.map.update_city_status(city_name)
        self.right_info_view.update_labels(self._data)
        self.bottom_info_view.update_labels(self._data)

    def _click_city(self, index):
        """
        Updates the info box when a new city is selected.
        """
        self._data.selected_city = index
        self.right_info_view.update_labels(self._data)

    def _click_symptom(self, symptom_key):
        """
        Handles symptom upgrades and updates the UI.
        """
        self._data.click_symptom(symptom_key)
        self.update_all_views()

    def _click_time(self):
        """
        Increments the turn number and updates the game state.
        """
        self._data.click_turn()
        self.update_all_views()
        for town in self._data.cities:
            self.map.update_city_status(town)
        if self._data.turn > self._data.maxturns:
            self.parent().close()
