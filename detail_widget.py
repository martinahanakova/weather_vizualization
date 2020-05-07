from PySide2.QtCore import QDateTime, Qt, QFile
from PySide2 import QtUiTools
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QGridLayout, QComboBox)
from PySide2.QtCharts import QtCharts

from functools import partial

from spiral import Spiral
from windrose_plot import WindrosePlot
from humidity_plot import HumidityPlot


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

        # Buttons For Pressure
        pressure_month_checkbox = self.interaction_panel.pressure_month_checkbox
        pressure_year_comboBox = self.interaction_panel.pressure_year_comboBox
        pressure_month_comboBox = self.interaction_panel.pressure_month_comboBox
        pressure_day_checkbox = self.interaction_panel.pressure_day_checkbox
        pressure_day_comboBox = self.interaction_panel.pressure_day_comboBox

        # Connections For Month Pressure
        pressure_month_checkbox.stateChanged.connect(partial(self.stateChanged, self.pressure_spiral, pressure_month_checkbox, \
        pressure_day_checkbox, pressure_year_comboBox, pressure_month_comboBox, pressure_day_comboBox))
        pressure_month_comboBox.currentTextChanged.connect(partial(self.stateChanged, self.pressure_spiral, pressure_month_checkbox, \
        pressure_day_checkbox, pressure_year_comboBox, pressure_month_comboBox, pressure_day_comboBox))
        pressure_year_comboBox.currentTextChanged.connect(partial(self.stateChanged, self.pressure_spiral, pressure_month_checkbox, \
        pressure_day_checkbox, pressure_year_comboBox, pressure_month_comboBox, pressure_day_comboBox))

        # Connections For Day Pressure
        pressure_day_checkbox.stateChanged.connect(partial(self.stateChanged, self.pressure_spiral, pressure_month_checkbox, \
        pressure_day_checkbox, pressure_year_comboBox, pressure_month_comboBox, pressure_day_comboBox))
        pressure_day_comboBox.currentTextChanged.connect(partial(self.stateChanged, self.pressure_spiral, pressure_month_checkbox, \
        pressure_day_checkbox, pressure_year_comboBox, pressure_month_comboBox, pressure_day_comboBox))

        # QWidget Layout
        self.layout = QGridLayout()

        self.layout.addLayout(self.grid_layout, 0, 0, 1, 3)
        self.layout.addWidget(self.interaction_panel, 0, 3, 1, 1)

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

    def stateChanged(self, widget, monthCheckBox, dayCheckBox, yearComboBox, monthComboBox, dayComboBox, arg):
        if monthCheckBox.isChecked():
            year = yearComboBox.currentText()
            month = monthComboBox.currentText()

            if dayCheckBox.isChecked():
                day = dayComboBox.currentText()
                widget.set_paint(0, 0, 1, year, month, day)
            else:
                widget.set_paint(0, 1, 0, year, month)

            widget.update()
        else:
            widget.set_paint(1, 0, 0)
            widget.update()
