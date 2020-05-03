from PySide2.QtCore import QDateTime, Qt, QFile
from PySide2 import QtUiTools
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QGridLayout, QComboBox)
from PySide2.QtCharts import QtCharts

from spiral import Spiral
from windrose_plot import WindrosePlot
from humidity_plot import HumidityPlot

from interaction_widget import Interaction


class DetailWidget(QWidget):
    def __init__(self, data, city):
        QWidget.__init__(self)

        self.data = data
        self.city = city

        loader = QtUiTools.QUiLoader()
        file = QFile("detail_interaction.ui")

        # QWidget Grid Layout
        self.grid_layout = QGridLayout()

        # Creating Pressure Spiral
        self.pressure_spiral = Spiral(data, city, 'pressure')
        self.set_weather_widget("Pressure in hPa", self.pressure_spiral, 0, 0)

        # Creating Windrose Plot
        self.windrose_plot = WindrosePlot(data, city)
        self.set_weather_widget("Wind speed in m/s", self.windrose_plot, 0, 1)

        # Creating Humidity Plot
        self.humidity_plot = HumidityPlot(data, city)
        self.set_weather_widget("Humidity", self.humidity_plot, 1, 0)

        # Creating Temperature Spiral
        self.temperature_spiral = Spiral(data, city, 'temperature')
        self.set_weather_widget("Temperature in °K", self.temperature_spiral, 1, 1)

        # Intearction Panel Layout
        self.interaction_panel = QWidget()
        self.interaction_panel = loader.load(file)

        '''
        self.interaction_layout = QGridLayout()
        self.interaction_layout.addWidget(pressure, 0, 0)

        pressure = self.create_interation('Wind')
        self.interaction_layout.addLayout(pressure, 0, 1)

        pressure = self.create_interation('Humidity')
        self.interaction_layout.addLayout(pressure, 1, 0)

        pressure = self.create_interation('Temperature')
        self.interaction_layout.addLayout(pressure, 1, 1)
        '''

        # QWidget Layout
        self.layout = QHBoxLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        #size.setHorizontalStretch(4)
        self.layout.addLayout(self.grid_layout)

        #size.setHorizontalStretch(1)
        #self.interaction_panel.setSizePolicy(size)
        self.layout.addWidget(self.interaction_panel)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

    def set_weather_widget(self, heading, plot, grid_pos_1, grid_pos_2):
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

        self.grid_layout.addLayout(layout , grid_pos_1, grid_pos_2)

        return
