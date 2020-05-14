from PySide2.QtCore import QUrl
from PySide2.QtWidgets import (QPushButton, QMenu, QAction)
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os

from model import MarkerModel


class MapWidget(QQuickWidget):
    def __init__(self, data, model):
        super(MapWidget, self).__init__(resizeMode=QQuickWidget.SizeRootObjectToView)

        self.data = data
        self.model = model

        self.rootContext().setContextProperty("marker_model", model)
        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QUrl.fromLocalFile(qml_path))

        positions = self.get_positions(self.data)
        names = self.get_names(self.data)
        values = self.get_values(self.data, "humidity")

        for i in range(0, len(names)):
            geo_coordinates = QGeoCoordinate(positions[i][0], positions[i][1])
            name = names[i]
            value = values[i]
            model.append_marker({"position": geo_coordinates, "color": "green", "name": name, "value": value})

        self.interface()

    def interface(self):
        self.b1 = QPushButton(self)
        self.b1.move(50, 0)

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

    # when button is clicked, changes values in all model items to a different attribute
    def clicked(self, attribute):
        self.b1.setText(attribute)
    #    self.l1.setText("selected attribute: "+attribute)
        values = self.get_values(self.data, attribute)
       # self.model.set_data(0, values[0], MarkerModel.ValueRole)
        print(attribute)
        for i in range (0,len(values)):
            self.model.set_data(i, values[i], MarkerModel.ValueRole)

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

    def create_action(self, attribute):
        action = QAction(attribute)
        action.triggered.connect(self.clicked(attribute))
        self.menu.addAction(action)
        return action
