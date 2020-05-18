from PySide2.QtCore import Qt, QFile
from PySide2 import QtUiTools
from PySide2.QtWidgets import (QWidget, QVBoxLayout, QLabel, QSizePolicy, QGridLayout, QComboBox, QCheckBox)

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

        # UI Elements For Pressure
        pressure_ui_elements = (
            self.interaction_panel.pressure_month_checkbox,
            self.interaction_panel.pressure_day_checkbox,
            self.interaction_panel.pressure_year_comboBox,
            self.interaction_panel.pressure_month_comboBox,
            self.interaction_panel.pressure_day_comboBox
        )

        # Connect UI Elements For Pressure
        for element in pressure_ui_elements:

            if isinstance(element, QComboBox):
                f = element.currentTextChanged
            elif isinstance(element, QCheckBox):
                f = element.stateChanged

            f.connect(partial(
                self.spiralStateChanged,
                self.pressure_spiral,
                *pressure_ui_elements
            ))

        # UI Elements For Wind
        wind_ui_elements = (
            self.interaction_panel.wind_year_checkbox,
            self.interaction_panel.wind_month_checkbox,
            self.interaction_panel.wind_day_checkbox,
            self.interaction_panel.wind_hour_checkbox,
            self.interaction_panel.wind_year_comboBox,
            self.interaction_panel.wind_month_comboBox,
            self.interaction_panel.wind_day_comboBox,
            self.interaction_panel.wind_hour_comboBox
        )

        # Connect UI Elements For Wind
        for element in wind_ui_elements:

            if isinstance(element, QComboBox):
                f = element.currentTextChanged
            elif isinstance(element, QCheckBox):
                f = element.stateChanged

            f.connect(partial(
                self.windStateChanged,
                self.windrose_plot,
                *wind_ui_elements
            ))

        # UI Elements For Humidity
        humidity_ui_elements = (
            self.interaction_panel.humidity_year_checkbox,
            self.interaction_panel.humidity_month_checkbox,
            self.interaction_panel.humidity_day_checkbox,
            self.interaction_panel.humidity_year_comboBox,
            self.interaction_panel.humidity_month_comboBox,
            self.interaction_panel.humidity_day_comboBox
            )

        # Connect UI Elements For Humidity
        for element in humidity_ui_elements:

                if isinstance(element, QComboBox):
                    f = element.currentTextChanged
                elif isinstance(element, QCheckBox):
                    f = element.stateChanged

                f.connect(partial(
                    self.humidityStateChanged,
                    self.humidity_plot,
                    *humidity_ui_elements
                ))

        # UI Elements For Temperature
        temperature_ui_elements = (
            self.interaction_panel.temperature_month_checkbox,
            self.interaction_panel.temperature_day_checkbox,
            self.interaction_panel.temperature_year_comboBox,
            self.interaction_panel.temperature_month_comboBox,
            self.interaction_panel.temperature_day_comboBox
        )

        # Connect UI Elements For Temperature
        for element in temperature_ui_elements:

            if isinstance(element, QComboBox):
                f = element.currentTextChanged
            elif isinstance(element, QCheckBox):
                f = element.stateChanged

            f.connect(partial(
                self.spiralStateChanged,
                self.temperature_spiral,
                *temperature_ui_elements
            ))

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

    def spiralStateChanged(self, widget, monthCheckBox, dayCheckBox, yearComboBox, monthComboBox, dayComboBox, arg):
        if monthCheckBox.isChecked():
            year = yearComboBox.currentText()
            month = monthComboBox.currentIndex() + 1

            if dayCheckBox.isChecked():
                day = dayComboBox.currentText()
                widget.set_paint(0, 0, 1, year, month, day)
            else:
                widget.set_paint(0, 1, 0, year, month)

            widget.update()
        else:
            widget.set_paint(1, 0, 0)
            widget.update()

        return

    def humidityStateChanged(self, widget, yearCheckBox, monthCheckBox, dayCheckBox,
                           yearComboBox, monthComboBox, dayComboBox, arg):

        if yearCheckBox.isChecked():
            year = yearComboBox.currentText()

            if monthCheckBox.isChecked():
                month = monthComboBox.currentIndex() + 1

                if dayCheckBox.isChecked():
                    day = dayComboBox.currentText()
                    widget.set_paint(0, 0, 0, 1, year, month, day)
                else:
                    widget.set_paint(0, 0, 1, 0, year, month)
            else:
                widget.set_paint(0, 1, 0, 0, year)

            widget.update()
        else:
            widget.set_paint(1, 0, 0, 0)
            widget.update()

    def windStateChanged(self, widget, yearCheckBox, monthCheckBox, dayCheckBox, hourCheckBox,
                           yearComboBox, monthComboBox, dayComboBox, hourComboBox, arg):

        if yearCheckBox.isChecked():
            year = yearComboBox.currentText()

            if monthCheckBox.isChecked():
                month = monthComboBox.currentIndex() + 1

                if dayCheckBox.isChecked():
                    day = dayComboBox.currentText()

                    if hourCheckBox.isChecked():
                        hour = hourComboBox.currentText()
                        widget.set_paint(0, 0, 0, 0, 1, year, month, day, hour)
                    else:
                        widget.set_paint(0, 0, 0, 1, 0, year, month, day)
                else:
                    widget.set_paint(0, 0, 1, 0, 0, year, month)
            else:
                widget.set_paint(0, 1, 0, 0, 0, year)

            widget.update()
        else:
            widget.set_paint(1, 0, 0, 0, 0)
            widget.update()
