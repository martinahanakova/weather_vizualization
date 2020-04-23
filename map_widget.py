from PySide2.QtCore import QDateTime, Qt, QUrl
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QVBoxLayout, QLabel, QSizePolicy, QGridLayout)
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtPositioning import QGeoCoordinate

import os


class MapWidget(QQuickWidget):
    def __init__(self, model):
        super(MapWidget, self).__init__(resizeMode=QQuickWidget.SizeRootObjectToView)

        self.model = model

        self.rootContext().setContextProperty("markermodel", model)
        qml_path = os.path.join(os.path.dirname(__file__), "map.qml")
        self.setSource(QUrl.fromLocalFile(qml_path))

        positions = [(44.97104,-93.46055), (44.96104,-93.16055)]

        urls = ["http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
                "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"]

        for c, u in zip(positions, urls):
            coord = QGeoCoordinate(*c)
            source = QUrl(u)
            model.appendMarker({"position": coord , "source": source})
