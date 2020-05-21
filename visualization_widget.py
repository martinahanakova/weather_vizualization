from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSizePolicy, QGridLayout)

from spiral import Spiral
from windrose_plot import WindrosePlot


class VisualizationWidget(QWidget):
    def __init__(self, data, city):
        QWidget.__init__(self)

        self.data = data
        self.city = city

        # QWidget Grid Layout
        self.grid_layout = QGridLayout()

        # Creating Chart 1
        self.pressure_spiral = Spiral(data, city)
        self.set_widget("Popis", "tu vloz objekt chartu", 0)

        # Creating Chart 2 Plot
        self.windrose_plot = WindrosePlot(data, city)
        self.set_widget("Popis", "tu vloz objekt chartu", 1)

    def set_widget(self, heading, plot, grid_pos):
        layout = QVBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        size.setVerticalStretch(1)
        text = QLabel("<h1 color=blue>"+heading+"</h1>", self)
        text.setSizePolicy(size)
        text.setAlignment(Qt.AlignCenter)
        layout.addWidget(text)

        size.setVerticalStretch(4)
        plot.setSizePolicy(size)
        layout.addWidget(plot)

        self.grid_layout.addLayout(layout, grid_pos)
