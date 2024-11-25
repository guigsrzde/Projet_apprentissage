import sys
import PyQt5.QtWidgets as widgets

class Menu(widgets.Qwidget):
    def __init__(self):
        super.__init__(None)
        self._build_ui()
        self.resize(256,256)
        #self._maladie = v

    def _add_button(self, text, row, col, cb):
        button = widgets.QPushButton(text)
        self._grid.addWidget(button, row, col)
        button.clicked.connect(cb)

    def _build_ui(self):
        self.setWindowTitle("Serious Game: Réussiras-tu à faire disparaître l'humanité")
        self._grid = widgets.QGridLayout()
        self._grid.setSpacing(1)
        self._add_button("propagation",0,3,self._click_propagation)
        self._add_button("resistance",1,3,self._click_resistance)
        self._add_button("symptome",2,3,self._click_symptome)

    def _click_propagation(self):
        #self._maladie.propagation += 1
        print("click de propagation")

    def _click_resistance(self):
        #self._maladie.resistance += 1
        print("click de resistance")

    def _click_symptome(self):
        #self._maladie.symptome += 1
        print("click de symptome")








def affiche():
    print("ok affichage")
    return 0