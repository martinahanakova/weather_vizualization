from PySide2.QtCore import QDateTime, Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QTableView, QSizePolicy, QGridLayout)
from PySide2.QtCharts import QtCharts

from spiral import Spiral
from windrose_plot import WindrosePlot


class DetailWidget(QWidget):
    def __init__(self, data):
        QWidget.__init__(self)

        self.data = data

        # Creating Pressure Spiral
        self.pressure_spiral = Spiral(data, 'Eilat', 'pressure')

        # Creating Windrose Plot
        self.windrose_plot = WindrosePlot(data)

        # Creating Temperature Spiral
        self.temperature_spiral = Spiral(data, 'Eilat', 'temperature')

        # QWidget Layout
        self.layout = QGridLayout()
        size = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Left Top Layout
        self.layout.addWidget(self.pressure_spiral , 0, 0)

        # Rigt Top Layout
        self.layout.addWidget(self.windrose_plot , 0, 1)

        # Left Bottom Layout
        #self.layout.addWidget(self.my_open_gl_widget_c , 1, 0)

        # Right Bottom Layout
        self.layout.addWidget(self.temperature_spiral , 1, 1)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

