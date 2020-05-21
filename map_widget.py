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

        self.interface()

    def interface(self):
        # self.l1 = QLabel(self)
        # self.l1.setText("nothing selected")
        # self.l1.move(200,0)

        self.b1 = QPushButton(self)
        self.b1.move(50, 0)

        self.menu = QMenu("Pick an attribute", self)

        # create a menu option for each attribute
        # lambda function is necessary in order to be able to send custom params to the function
        self.aHumidity = QAction("humidity")
        self.aHumidity.triggered.connect(lambda: self.clicked("humidity"))
        self.menu.addAction(self.aHumidity)

        self.aPressure = QAction("pressure")
        self.aPressure.triggered.connect(lambda: self.clicked("pressure"))
        self.menu.addAction(self.aPressure)

        self.aTemp = QAction("temperature")
        self.aTemp.triggered.connect(lambda: self.clicked("temperature"))
        self.menu.addAction(self.aTemp)

        self.aWindSpeed = QAction("wind_speed")
        self.aWindSpeed.triggered.connect(lambda: self.clicked("wind_speed"))
        self.menu.addAction(self.aWindSpeed)


        self.b1.setMenu(self.menu)
        self.b1.resize(self.menu.width()+50,self.b1.height())


        # allows this class an access to specific QML element based on objectName
        self.slider = self.rootObject().findChild(QObject, "slider") # accessing slider from QML file to position datePickers dynamically

        self.dpStart = self.createDatePicker(0)
        self.dpStart.setToolTip("Select the BEGINNING of the time period from which the data is displayed")
        self.dpStart.move(self.slider.property("x") - self.dpStart.width() - 30, self.slider.property("y"))
        self.dpEnd = self.createDatePicker(-1)
        self.dpEnd.setToolTip("Select the END of the time period from which the data is displayed")
        self.dpEnd.move(self.slider.property("x") + self.slider.property("width") + 30, self.slider.property("y"))

        # set date pickers boundaries based on first and last date in given data
        self.dpStart.setMinimumDate(self.dpStart.date())
        self.dpEnd.setMinimumDate(self.dpStart.date())
        self.dpStart.setMaximumDate(self.dpEnd.date())
        self.dpEnd.setMaximumDate(self.dpEnd.date())

        # label holding the current date selected bz user via slider handle
        self.labelDate = QLabel(self)
        self.labelDate.move(self.slider.property("x") + (self.slider.width() / 2) - 100, self.slider.property("y") + 30)
        self.labelDate.setText("selected date: " + str(self.currentDate).replace("-",".") )
        self.labelDate.adjustSize()

        # triggers an update of slider date range values everz time either datepicker value is changed
        self.dpStart.dateChanged.connect(lambda: self.changeDate())
        self.dpEnd.dateChanged.connect(lambda: self.changeDate())

        self.labelJumpInput = QLabel(self)
        self.labelJumpInput.move(self.labelDate.x(), self.labelDate.y() + 40)
        self.labelJumpInput.setText("slider jump (in days): ")
        self.labelJumpInput.adjustSize()

        self.jumpInput = QLineEdit(self)
        self.jumpInput.move(self.labelJumpInput.x() + self.labelJumpInput.width(), self.labelJumpInput.y() - 5)
        self.jumpInput.resize(35, self.jumpInput.height())
        self.jumpInput.editingFinished.connect(lambda:  self.slider.setProperty("stepSize", self.jumpInput.text()))

        self.labelAggInput = QLabel(self)
        self.labelAggInput.move(self.labelDate.x(), self.jumpInput.y() + 40)
        self.labelAggInput.setText("mean (in days): ")
        self.labelAggInput.adjustSize()

        self.aggInput = QLineEdit(self)
        self.aggInput.move(self.jumpInput.x(), self.labelAggInput.y() - 5)
        self.aggInput.resize(35, self.aggInput.height())
        self.aggInput.editingFinished.connect(lambda:  self.setAgg(self.aggInput.text()))

        # lastly, initialize visualisation with specific attribute
        self.aHumidity.trigger()
        self.changeDate()

    @Slot(int)
    def updateDate(self, value):
        self.currentDate = self.uniqueDates[value - 1]
        self.labelDate.setText("selected date: " + str(self.currentDate).replace("-",".") )
        self.clicked(self.b1.text())

    # TODO: add bottom interaction bar for choosing the data time interval
    # TODO: visualise time series data, not just int created by aggregation -> TODO: create setting of visualised time period for user

    # calculates the difference (in days) between start date and end date and rescales the slider
    def setAgg(self, value):
        self.aggregation = int(value)

    def changeDate(self):
        dif = self.uniqueDates.index(self.dpEnd.date().toString("yyyy-MM-dd")) - self.uniqueDates.index(self.dpStart.date().toString("yyyy-MM-dd"))
      #  self.labelDate.setText("dif: " + str(dif) )
        self.slider.setProperty("to", dif + 1)


    # creates datePicker initialized with specific date from given data, based on index
    def createDatePicker(self, index):
        timeTmp = self.uniqueDates[index]
        timeQFormat = timeTmp.split("-")
      #  print(timeQFormat)
        # date is parsed and converted to int to comply with required format of QDate
        datePicker = QDateTimeEdit(QDate(int(timeQFormat[0]),int(timeQFormat[1]),int(timeQFormat[2])), self)
        datePicker.setDisplayFormat("yyyy.MM.dd")
        datePicker.setCalendarPopup(True)
        datePicker.setCalendarWidget(QCalendarWidget())
        datePicker.resize(datePicker.width() + 20, datePicker.height())
        return datePicker

    # when button is clicked, changes values in all model items to a different attribute
    def clicked(self, attribute):
        self.b1.setText(attribute)
    #    self.l1.setText("selected attribute: "+attribute)
        values = self.get_values(self.data, attribute) # TODO: fix date and interval
        colors = self.get_colors(self.data, attribute)
       # self.model.setData(0, values[0], MarkerModel.ValueRole)
        print(attribute)
        for i in range (0,len(values)):
            self.model.setData(i, values[i], colors[i], MarkerModel.ValueRole)

    def get_positions(self, data):
        tmp = data.drop_duplicates('city').sort_values(by=['city'])
        positions = [[x, y] for x, y in zip(tmp['latitude'], tmp['longitude'])]
        return positions

    def get_names(self, data):
        tmp = data.drop_duplicates('city').sort_values(by=['city'])
        names = tmp['city'].values.tolist()
        return names

    # TODO: aggregate all days based on self.aggregation value, not just current day
    def get_values(self, data, attribute): # creates an ordered list of aggregated values of a specified attribute
       # tmp = data.filter(like=startDate, axis=0)
        tmp = data[data['datetime'].str.contains(self.currentDate)]
        values = tmp.groupby('city').apply(lambda x: x[attribute].mean()).values.round(2).tolist() # groupby sorts rows by specified attribute by default
        """
        startIndex = self.uniqueDates.index(self.currentDate)
        tmp2 =
        for i in range(0, self.aggregation):
            tmp = data[data['datetime'].str.contains(self.uniqueDates[startIndex + i])]
            tmp2 = pd.concat(tmp2,tmp)
            print(tmp.size())
        values = tmp.groupby('city').apply(lambda x: x[attribute].mean()).values.round(2).tolist()
        #   print(self.currentDate)
     #   print(values)
     """
        return values

    def get_colors(self, data, attribute):
        tmp = data.groupby('city').agg({attribute : 'mean'})

        max_value = round(tmp[attribute].max())
        min_value = round(tmp[attribute].min())

        diff = max_value - min_value
        step = round(1 / 6 * diff)

        if attribute == 'pressure':
            attribute_values = {0: [255,255,255], 1: [204,229,255], 2: [102,178,255], 3: [0,128,255], \
            4: [0,0,255], 5: [0,0,102], 6: [0,0,51]}
        elif attribute == 'temperature':
            attribute_values = {0: [0,102,204], 1: [102,178,255], 2: [204,229,255], 3: [255,204,204], \
            4: [255,102,102], 5: [204,0,0], 6: [102,0,0]}

            # TODO: create more suited colors for humidity and wind speed
        elif attribute == 'humidity':
            attribute_values = {0: [0,102,204], 1: [102,178,255], 2: [204,229,255], 3: [255,204,204], \
            4: [255,102,102], 5: [204,0,0], 6: [102,0,0]}
        elif attribute == 'wind_speed':
            attribute_values = {0: [0,102,204], 1: [102,178,255], 2: [204,229,255], 3: [255,204,204], \
            4: [255,102,102], 5: [204,0,0], 6: [102,0,0]}

        values = numpy.array([min_value, min_value + 1*step, min_value + 2*step, min_value + 3*step, \
        min_value + 4*step, min_value + 5*step, max_value])

        tmp['distances'] = tmp[attribute].apply(lambda x: abs(x - values))
        tmp['index'] = tmp['distances'].apply(lambda x: numpy.argmin(x))
        tmp['color'] = tmp['index'].apply(lambda x: attribute_values.get(x))

        colors = tmp['color'].tolist()
        colors_list = []

        for color_tmp in colors:
            color = QColor(color_tmp[0], color_tmp[1], color_tmp[2], 255)
            colors_list.append(color)



        return colors_list # returns QJSValue

    def createAction(self, attribute):
        action = QAction(attribute)
        action.triggered.connect(self.clicked(attribute))
        self.menu.addAction(action)
        return action



   # def get_values(self, data):


      #  return data['positions']

  #  def process_data(self, data):

