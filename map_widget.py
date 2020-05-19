from PySide2.QtCore import QDateTime, Qt, QUrl, QModelIndex
from PySide2.QtGui import QPainter, QColor
from PySide2.QtWidgets import (QWidget, QHeaderView, QVBoxLayout, QLabel, QSizePolicy, QGridLayout, QPushButton, QMenu, QAction)
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os
import numpy
import pandas as pd

from model import MarkerModel


class MapWidget(QQuickWidget):
    def __init__(self, data, model):
        super(MapWidget, self).__init__(resizeMode=QQuickWidget.SizeRootObjectToView)

        self.data = data
        self.model = model

        self.rootContext().setContextProperty("markermodel", model)
        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QUrl.fromLocalFile(qml_path))

        positions = self.get_positions(self.data)
        names = self.get_names(self.data)
        values = self.get_values(self.data, "humidity")
        colors = self.get_colors(self.data, "humidity")

        for i in range(0, len(names)):
            geo_coordinates = QGeoCoordinate(positions[i][0], positions[i][1])
            name = names[i]
            value = values[i]
            color = colors[i] # QJS value , needs to be QColor
           # color = QColor(color_tmp[0], color_tmp[1], color_tmp[2], 255)
            #print(positions[i][0], positions[i][1], "green", name)
            model.appendMarker({"position": geo_coordinates, "color": color, "name": name, "value": value})


        self.interface()
      #  print(self.get_colors(self.data, "humidity"))

    attribute = "wind_speed"
    def interface(self):

        self.b1 = QPushButton(self)
        self.b1.move(50,0)
       # self.b1.setText(self.attribute)
     #   self.b1.clicked.connect(self.clicked)
    # TODO: add multichoice buttons for all attributes, each triggering change of values in model based on that button value
        self.menu = QMenu("Pick an attribute", self)

        # create a menu option for each attribute (in connect, lambda is necessary in order to be able to send custom params to function)
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

        self.aHumidity.trigger()
    # TODO: add bottom interaction bar for choosing the data time interval
    # TODO: visualise time series data, not just int created bz aggregation -> TODO: create setting of visualised time period for user
    # TODO: implementation of connect makes it unable to dynamically send button content to clicked(function) - figure out how to do it

    # when button is clicked, changes values in all model items to a different attribute
    def clicked(self, attribute):
        self.b1.setText(attribute)
    #    self.l1.setText("selected attribute: "+attribute)
        values = self.get_values(self.data, attribute)
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
        names = tmp['city'].tolist()
        return names

    def get_values(self, data, attribute): # creates an ordered list of aggregated values of a specified attribute
        values = data.groupby('city').apply(lambda x: x[attribute].mean().round(2)).tolist() # groupby sorts rows by specified attribute by default
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
            # create custom colors for humidity and wind speed
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

