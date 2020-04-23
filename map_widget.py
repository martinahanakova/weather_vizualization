from PySide2.QtCore import QDateTime, Qt, QUrl
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QVBoxLayout, QLabel, QSizePolicy, QGridLayout)
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os


class MapWidget(QQuickWidget):
    def __init__(self, data, model):
        super(MapWidget, self).__init__(resizeMode=QQuickWidget.SizeRootObjectToView)

        self.data = data
        self.model = model

        self.rootContext().setContextProperty("markermodel", model)
        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QUrl.fromLocalFile(qml_path))

        positions = self.get_positions(self.data)

        marker_url = "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"

        for coordinates in positions:
            geo_coordinates = QGeoCoordinate(*coordinates)
            marker = QUrl(marker_url)
            model.appendMarker({"position": geo_coordinates , "source": marker})

    def get_positions(self, data):
        data = data.drop_duplicates('city')
        data['positions'] = [[x, y] for x, y in zip(data['latitude'], data['longitude'])]

        return data['positions']
