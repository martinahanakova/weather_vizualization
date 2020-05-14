from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSizePolicy, QGridLayout)

from spiral import Spiral
from windrose_plot import WindrosePlot
from humidity_plot import HumidityPlot


class DetailWidget(QWidget):
    def __init__(self, data, city):
        QWidget.__init__(self)

        self.data = data
        self.city = city

        # Creating Pressure Spiral
        self.pressure_spiral = Spiral(data, self.city, 'pressure')

        # Creating Windrose Plot
        self.windrose_plot = WindrosePlot(data, self.city)

        # Creating Humidity Plot
        self.humidity_plot = HumidityPlot(data, self.city)

        # Creating Temperature Spiral
        self.temperature_spiral = Spiral(data, self.city, 'temperature')

        # QWidget Layout
        self.layout = QGridLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left Top Layout
        self.left_top_layout = QVBoxLayout()

        size.setVerticalStretch(1)
        text = QLabel("<h1 color=blue>Pressure in hPa</h1>", self)
        text.setSizePolicy(size)
        text.setAlignment(Qt.AlignCenter)
        self.left_top_layout.addWidget(text)

        size.setVerticalStretch(4)
        self.pressure_spiral.setSizePolicy(size)
        self.left_top_layout.addWidget(self.pressure_spiral)

        self.layout.addLayout(self.left_top_layout , 0, 0)

        # Rigt Top Layout
        self.right_top_layout = QVBoxLayout()

        size.setVerticalStretch(1)
        text = QLabel("<h1 color=blue>Wind speed in m/s</h1>", self)
        text.setSizePolicy(size)
        text.setAlignment(Qt.AlignCenter)
        self.right_top_layout.addWidget(text)

        size.setVerticalStretch(4)
        self.windrose_plot.setSizePolicy(size)
        self.right_top_layout.addWidget(self.windrose_plot)

        self.layout.addLayout(self.right_top_layout , 0, 1)

        # Left Bottom Layout
        self.left_bottom_layout = QVBoxLayout()

        size.setVerticalStretch(1)
        text = QLabel("<h1 color=blue>Humidity</h1>", self)
        text.setSizePolicy(size)
        text.setAlignment(Qt.AlignCenter)
        self.left_bottom_layout.addWidget(text)

        size.setVerticalStretch(4)
        self.humidity_plot.setSizePolicy(size)
        self.left_bottom_layout.addWidget(self.humidity_plot)

        self.layout.addLayout(self.left_bottom_layout , 1, 0)

        # Right Bottom Layout
        self.right_bottom_layout = QVBoxLayout()

        size.setVerticalStretch(1)
        text = QLabel("<h1 color=blue>Temperature in °K</h1>", self)
        text.setSizePolicy(size)
        text.setAlignment(Qt.AlignCenter)
        self.right_bottom_layout.addWidget(text)

        size.setVerticalStretch(4)
        self.temperature_spiral.setSizePolicy(size)
        self.right_bottom_layout.addWidget(self.temperature_spiral)

        self.layout.addLayout(self.right_bottom_layout , 1, 1)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

