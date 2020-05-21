from PySide2.QtCore import QUrl, QDate, QObject, Slot
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QLabel, QPushButton, QMenu, QAction, QCalendarWidget, QAbstractButton
from PySide2.QtWidgets import QDateTimeEdit, QLineEdit
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os
import numpy
import pandas
import datetime

from functools import partial

from model import MarkerModel


class MapWidget(QQuickWidget):
    def __init__(self, data, model):
        super(MapWidget, self).__init__(resizeMode=QQuickWidget.SizeRootObjectToView)

        self.data = data
        self.model = model

        self.attribute_button = QPushButton(self)
        self.attribute_button.setStyleSheet("color: black")
        self.menu = QMenu("Pick an attribute", self)

        # Create Menu Options
        self.humidity_attribute = QAction("humidity")
        self.pressure_attribute = QAction("pressure")
        self.temperature_attribute = QAction("temperature")
        self.wind_speed_attribute = QAction("wind_speed")

        # due to frequent access of dates based on index, we store this data separately
        self.uniqueDates = self.data["datetime"].apply(lambda x: x.split(' ')[0]).unique().tolist()
        self.aggregation = 1

        self.rootContext().setContextProperty("markermodel", model)
        self.rootContext().setContextProperty("MapWidget", self)
        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QUrl.fromLocalFile(qml_path))

        positions = self.get_positions(self.data)
        names = self.get_names(self.data)

        # get first date of dataset in yy-mm-dd
        self.currentDate = self.uniqueDates[0]

        # Set Labels
        self.date_label = QLabel("selected date: " + str(self.currentDate).replace("-", "."), self)
        self.date_label.setStyleSheet("color: black")

        # Set Previous and Next Buttons
        self.previous_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)

        self.previous_button.clicked.connect(partial(self.on_button_clicked, "previous"))
        self.next_button.clicked.connect(partial(self.on_button_clicked, "next"))

        values = self.get_values(self.data, "humidity")
        colors = self.get_colors(self.data, "humidity")

        for i in range(0, len(names)):
            geo_coordinates = QGeoCoordinate(positions[i][0], positions[i][1])
            name = names[i]
            value = values[i]
            color = colors[i]

            model.append_marker({"position": geo_coordinates, "color": color, "name": name, "value": value, "date": self.currentDate})

        self.create_interface()

        return

    def add_attribute_to_menu(self, attribute_action, attribute):
        attribute_action.triggered.connect(lambda: self.clicked(attribute))
        self.menu.addAction(attribute_action)

    def create_date_picker(self, index):
        tmp_time = self.uniqueDates[index]
        time_QFormat = tmp_time.split("-")

        # date is parsed and converted to int to comply with required format of QDate
        date_picker = QDateTimeEdit(QDate(int(time_QFormat[0]), int(time_QFormat[1]), int(time_QFormat[2])), self)
        date_picker.setDisplayFormat("yyyy.MM.dd")
        date_picker.setCalendarPopup(True)
        date_picker.setCalendarWidget(QCalendarWidget())
        date_picker.resize(date_picker.width() + 20, date_picker.height())

        return date_picker

    def set_date_pickers(self, slider):
        # Set Date Picker for Start of self.slider
        date_picker_start = self.create_date_picker(0)
        date_picker_start.setToolTip("Select the BEGINNING of the time period from which the data is displayed")
        date_picker_start.move(slider.property("x") - date_picker_start.width() - 30, slider.property("y"))

        # Set Date Picker for End of self.slider
        date_picker_end = self.create_date_picker(-1)
        date_picker_end.setToolTip("Select the END of the time period from which the data is displayed")
        date_picker_end.move(slider.property("x") + slider.property("width") + 30, slider.property("y"))

        # Set Date Pickers Boundaries Based on First and Last Date in Given Data
        date_picker_start.setMinimumDate(date_picker_start.date())
        date_picker_end.setMinimumDate(date_picker_start.date())
        date_picker_start.setMaximumDate(date_picker_end.date())
        date_picker_end.setMaximumDate(date_picker_end.date())

        return date_picker_start, date_picker_end

    def create_interface(self):
        self.attribute_button.move(50, 0)

        # Create a Menu Option for Each Attribute
        self.add_attribute_to_menu(self.humidity_attribute, "humidity")
        self.add_attribute_to_menu(self.pressure_attribute, "pressure")
        self.add_attribute_to_menu(self.temperature_attribute, "temperature")
        self.add_attribute_to_menu(self.wind_speed_attribute, "wind_speed")

        self.attribute_button.setMenu(self.menu)
        self.attribute_button.resize(self.menu.width()+50, self.attribute_button.height())

        # Get self.slider from QML File
        self.slider = self.rootObject().findChild(QObject, "slider")

        # Set Date Pickers
        self.date_picker_start, self.date_picker_end = self.set_date_pickers(self.slider)

        self.date_picker_start.dateChanged.connect(lambda: self.change_date(self.slider, self.self.date_picker_start, self.date_picker_end))
        self.date_picker_end.dateChanged.connect(lambda: self.change_date(self.slider, self.self.date_picker_start, self.date_picker_end))

        # Label Holding the Current Date Selected by User
        self.date_label.move(self.slider.property("x") + (self.slider.width() / 2) - 100, self.slider.property("y") + 30)
        self.date_label.adjustSize()

        # Set Buttons Position
        self.previous_button.setStyleSheet("color: black")
        self.previous_button.move(self.slider.property("x"), self.slider.property("y") + 50)
        self.previous_button.adjustSize()
        self.next_button.setStyleSheet("color: black")
        self.next_button.move(self.slider.property("x") + self.slider.width() - 70, self.slider.property("y") + 50)
        self.next_button.adjustSize()

        jump_label = QLabel("self.slider jump (in days): ", self)
        jump_label.setStyleSheet("color: black")
        jump_label.move(self.date_label.x(), self.date_label.y() + 40)
        jump_label.adjustSize()

        self.jump_value = QLineEdit(self)
        self.jump_value.move(jump_label.x() + jump_label.width(), jump_label.y() - 5)
        self.jump_value.resize(35, self.jump_value.height())
        self.jump_value.editingFinished.connect(lambda: self.slider.setProperty("stepSize", self.jump_value.text()))

        agg_label = QLabel(self)
        agg_label.setStyleSheet("color: black")
        agg_label.move(self.date_label.x(), self.jump_value.y() + 40)
        agg_label.setText("mean (in days): ")
        agg_label.adjustSize()

        agg_value = QLineEdit(self)
        agg_value.move(self.jump_value.x(), agg_label.y() - 5)
        agg_value.resize(35, agg_value.height())
        agg_value.editingFinished.connect(lambda:  self.set_agg(agg_value.text()))

        # Initialize Visualization
        self.humidity_attribute.trigger()
        self.change_date(self.slider, self.date_picker_start, self.date_picker_end)

    def on_button_clicked(self, action):
        jump_value = int(self.jump_value.text())
        slider_value = int(self.slider.property("value"))

        current_date = pandas.to_datetime(self.currentDate)

        start_date = self.date_picker_start.date().toPython()
        end_date = self.date_picker_end.date().toPython()

        if action == "next":
            if current_date + datetime.timedelta(days=jump_value) <= end_date:
                self.slider.setProperty("value", slider_value + jump_value)
                self.update_date(int(self.slider.property("value")))
        elif action == "previous":
            if current_date - datetime.timedelta(days=jump_value) >= start_date:
                self.slider.setProperty("value", slider_value - jump_value)
                self.update_date(int(self.slider.property("value")))

    @Slot(int)
    def update_date(self, value):
        self.currentDate = self.uniqueDates[value - 1]
        self.date_label.setText("selected date: " + str(self.currentDate).replace("-", "."))
        self.clicked(self.attribute_button.text())

    # TODO: visualise time series data, not just int created by aggregation
    # TODO: create setting of visualised time period for user

    # calculates the difference (in days) between start date and end date and rescales the self.slider
    def set_agg(self, value):
        self.aggregation = int(value)
        self.clicked(self.attribute_button.text())

    def change_date(self, slider, date_picker_start, date_picker_end):
        dif = self.uniqueDates\
                  .index(date_picker_end.date().toString("yyyy-MM-dd")) - self.uniqueDates.index(date_picker_start.date().toString("yyyy-MM-dd"))
        slider.setProperty("to", dif + 1)

    # when button is clicked, changes values in all model items to a different attribute
    def clicked(self, attribute):
        self.attribute_button.setText(attribute)
        values = self.get_values(self.data, attribute)

        colors = self.get_colors(self.data, attribute)

        for i in range(0, len(values)):
            self.model.setData(i, values[i], colors[i], MarkerModel.ValueRole)

    @staticmethod
    def get_positions(data):
        tmp = data.drop_duplicates('city').sort_values(by=['city'])
        positions = [[x, y] for x, y in zip(tmp['latitude'], tmp['longitude'])]

        return positions

    @staticmethod
    def get_names(data):
        tmp = data.drop_duplicates('city').sort_values(by=['city'])
        names = tmp['city'].values.tolist()

        return names

    # creates an ordered list of aggregated values of a specified attribute
    def get_values(self, data, attribute):
        data['datetime'] = pandas.to_datetime(data['datetime'])

        start_date = pandas.to_datetime(self.currentDate)
        end_date = start_date + datetime.timedelta(days=self.aggregation)

        tmp = data[data['datetime'] >= start_date]
        tmp = tmp[tmp['datetime'] <= end_date]

        values = tmp.groupby('city').apply(lambda x: x[attribute].mean()).values.round(2).tolist()

        return values

    @staticmethod
    def get_colors(data, attribute):
        tmp = data.groupby('city').agg({attribute: 'mean'})

        max_value = round(tmp[attribute].max())
        min_value = round(tmp[attribute].min())

        diff = max_value - min_value
        step = round(1 / 6 * diff)

        if attribute == 'pressure':
            attribute_values = {0: [255, 255, 255], 1: [204, 229, 255], 2: [102, 178, 255], 3: [0, 128, 255],
                                4: [0, 0, 255], 5: [0, 0, 102], 6: [0, 0, 51]}
        elif attribute == 'temperature':
            attribute_values = {0: [0, 102, 204], 1: [102, 178, 255], 2: [204, 229, 255], 3: [255, 204, 204],
                                4: [255, 102, 102], 5: [204, 0, 0], 6: [102, 0, 0]}

        # TODO: create more suited colors for humidity and wind speed

        elif attribute == 'humidity':
            attribute_values = {0: [0, 102, 204], 1: [102, 178, 255], 2: [204, 229, 255], 3: [255, 204, 204],
                                4: [255, 102, 102], 5: [204, 0, 0], 6: [102, 0, 0]}
        elif attribute == 'wind_speed':
            attribute_values = {0: [0, 102, 204], 1: [102, 178, 255], 2: [204,229,255], 3: [255, 204, 204],
                                4: [255, 102, 102], 5: [204, 0, 0], 6: [102, 0, 0]}

        values = numpy.array([min_value, min_value + 1*step, min_value + 2*step, min_value + 3*step,
                              min_value + 4*step, min_value + 5*step, max_value])

        tmp['distances'] = tmp[attribute].apply(lambda x: abs(x - values))
        tmp['index'] = tmp['distances'].apply(lambda x: numpy.argmin(x))
        tmp['color'] = tmp['index'].apply(lambda x: attribute_values.get(x))

        colors = tmp['color'].tolist()
        colors_list = []

        for color_tmp in colors:
            color = QColor(color_tmp[0], color_tmp[1], color_tmp[2], 255)
            colors_list.append(color)

        # returns QJSValue
        return colors_list

    def createAction(self, attribute):
        action = QAction(attribute)
        action.triggered.connect(self.clicked(attribute))
        self.menu.addAction(action)
        return action
