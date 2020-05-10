from PySide2.QtCore import QDateTime, Qt, QUrl, QModelIndex
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QVBoxLayout, QLabel, QSizePolicy, QGridLayout, QPushButton)
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os

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
        self.interface()

        for i in range(0, len(names)):
            geo_coordinates = QGeoCoordinate(positions[i][0], positions[i][1])
            name = names[i]
            value = values[i]
            #print(positions[i][0], positions[i][1], "green", name)
            model.appendMarker({"position": geo_coordinates, "color": "green", "name": name, "value": value})

    attribute = "wind_speed"
    def interface(self):

        self.l1 = QLabel(self)
        self.l1.setText("nothing selected")
        self.l1.move(200,50)

        self.b1 = QPushButton(self)
        self.b1.setText(self.attribute)
        self.b1.clicked.connect(self.clicked)
    # TODO: add multichoice buttons for all attributes, each triggering change of values in model based on that button value
    # TODO: add bottom interaction bar for choosing the data time interval
    # TODO: visualise time series data, not just int created bz aggregation -> TODO: create setting of visualised time period for user
    # TODO: implementation of connect makes it unable to dynamically send button content to clicked(function) - figure out how to do it

    # when button is clicked, changes values in all model items to a different attribute
    def clicked(self):
        self.l1.setText("selected attribute: "+self.attribute)
        values = self.get_values(self.data, self.attribute)
       # self.model.setData(0, values[0], MarkerModel.ValueRole)
        print(values)
        for i in range (0,len(values)):

            self.model.setData(i, values[i], MarkerModel.ValueRole)
            # TODO: send index of i row instead of int i - index object is needed for emit function params


    def get_positions(self, data):
        tmp = data.drop_duplicates('city').sort_values(by=['city'])
        positions = [[x, y] for x, y in zip(tmp['latitude'], tmp['longitude'])]
        return positions

    def get_names(self, data):
        tmp = data.drop_duplicates('city').sort_values(by=['city'])
        names = tmp['city'].tolist()
        return names

    def get_values(self, data, attribute): # creates an ordered list of aggregated values of a specified attribute
        values = data.groupby('city').apply(lambda x: x[attribute].mean()).tolist() # groupby sorts rows by specified attribute by default
        return values



   # def get_values(self, data):


      #  return data['positions']

  #  def process_data(self, data):

