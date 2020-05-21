from PySide2.QtCore import QUrl, QDate, QObject, Slot
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QLabel, QPushButton, QMenu, QAction, QCalendarWidget
from PySide2.QtWidgets import QDateTimeEdit, QLineEdit
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os
import numpy

from model import MarkerModel


class MapWidget(QQuickWidget):
    def __init__(self, data, model):
        super(MapWidget, self).__init__(resizeMode=QQuickWidget.SizeRootObjectToView)

        self.data = data
        self.model = model

        self.attribute_button = QPushButton(self)
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

        # TODO: dynamically specify aggregation interval based on user input

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
        # Set Date Picker for Start of Slider
        date_picker_start = self.create_date_picker(0)
        date_picker_start.setToolTip("Select the BEGINNING of the time period from which the data is displayed")
        date_picker_start.move(slider.property("x") - date_picker_start.width() - 30, slider.property("y"))

        # Set Date Picker for End of Slider
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

        # Get Slider from QML File
        slider = self.rootObject().findChild(QObject, "slider")

        date_picker_start, date_picker_end = self.set_date_pickers(slider)

        # label holding the current date selected by user via slider handle
        self.labelDate = QLabel(self)
        self.labelDate.move(slider.property("x") + (slider.width() / 2) - 100, slider.property("y") + 30)
        self.labelDate.setText("selected date: " + str(self.currentDate).replace("-", "."))
        self.labelDate.adjustSize()

        # triggers an update of slider date range values everz time either datepicker value is changed
        date_picker_start.dateChanged.connect(lambda: self.change_date(slider, date_picker_start, date_picker_end))
        date_picker_end.dateChanged.connect(lambda: self.change_date(slider, date_picker_start, date_picker_end))

        self.labelJumpInput = QLabel(self)
        self.labelJumpInput.move(self.labelDate.x(), self.labelDate.y() + 40)
        self.labelJumpInput.setText("slider jump (in days): ")
        self.labelJumpInput.adjustSize()

        self.jumpInput = QLineEdit(self)
        self.jumpInput.move(self.labelJumpInput.x() + self.labelJumpInput.width(), self.labelJumpInput.y() - 5)
        self.jumpInput.resize(35, self.jumpInput.height())
        self.jumpInput.editingFinished.connect(lambda: slider.setProperty("stepSize", self.jumpInput.text()))

        self.labelAggInput = QLabel(self)
        self.labelAggInput.move(self.labelDate.x(), self.jumpInput.y() + 40)
        self.labelAggInput.setText("mean (in days): ")
        self.labelAggInput.adjustSize()

        self.aggInput = QLineEdit(self)
        self.aggInput.move(self.jumpInput.x(), self.labelAggInput.y() - 5)
        self.aggInput.resize(35, self.aggInput.height())
        self.aggInput.editingFinished.connect(lambda:  self.setAgg(self.aggInput.text()))

        # lastly, initialize visualisation with specific attribute
        self.humidity_attribute.trigger()
        self.change_date(slider, date_picker_start, date_picker_end)

    @Slot(int)
    def update_date(self, value):
        self.currentDate = self.uniqueDates[value - 1]
        self.labelDate.setText("selected date: " + str(self.currentDate).replace("-", "."))
        self.clicked(self.attribute_button.text())

    # TODO: add bottom interaction bar for choosing the data time interval
    # TODO: visualise time series data, not just int created by aggregation
    # TODO: create setting of visualised time period for user

    # calculates the difference (in days) between start date and end date and rescales the slider
    def setAgg(self, value):
        self.aggregation = int(value)

    def change_date(self, slider, date_picker_start, date_picker_end):
        dif = self.uniqueDates\
                  .index(date_picker_end.date().toString("yyyy-MM-dd")) - self.uniqueDates.index(date_picker_start.date().toString("yyyy-MM-dd"))
        slider.setProperty("to", dif + 1)

    # when button is clicked, changes values in all model items to a different attribute
    def clicked(self, attribute):
        self.attribute_button.setText(attribute)
        values = self.get_values(self.data, attribute)

        # TODO: fix date and interval

        colors = self.get_colors(self.data, attribute)

        print(attribute)
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

    # TODO: aggregate all days based on self.aggregation value, not just current day

    # creates an ordered list of aggregated values of a specified attribute
    def get_values(self, data, attribute):
        tmp = data[data['datetime'].str.contains(self.currentDate)]

        # groupby sorts rows by specified attribute by default
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
