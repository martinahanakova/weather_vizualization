from PySide2.QtCore import (QAbstractListModel, Qt, QModelIndex, Slot)

from detail_widget import DetailWidget
from detail_window import DetailWindow
from visualization_widget import VisualizationWidget
from visualization_window import VisualizationWindow


class MarkerModel(QAbstractListModel):
    PositionRole, ColorRole, NameRole, ValueRole, ColorRole, DateRole = range(Qt.UserRole, Qt.UserRole + 6)

    def __init__(self, data, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []
        self.model_data = data

        self.dialog_1 = None

    @Slot(str)
    def open_detail(self, city):

        if self.dialog_1:
            widget2 = DetailWidget(self.model_data, city)
            self.dialog_2 = DetailWindow(widget2, city)
            self.dialog_2.show()
        else:
            widget1 = DetailWidget(self.model_data, city)
            self.dialog_1 = DetailWindow(widget1, city)
            self.dialog_1.show()

    @Slot(str)
    def open_visualization(self, city):
        widget = VisualizationWidget(self.model_data, city)
        self.visualization = VisualizationWindow(widget, city)
        self.visualization.show()

    def rowCount(self, parent=QModelIndex()):
        return len(self._markers)

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == MarkerModel.PositionRole:
                return self._markers[index.row()]["position"]
            elif role == MarkerModel.ColorRole:
                return self._markers[index.row()]["color"]
            elif role == MarkerModel.NameRole:
                return self._markers[index.row()]["name"]
            elif role == MarkerModel.ValueRole:
                return self._markers[index.row()]["value"]
            elif role == MarkerModel.ColorRole:
                return self._markers[index.row()]["color"]
            elif role == MarkerModel.DateRole:
                return self._markers[index.row()]["date"]

    def setData(self, index, value, color, role=Qt.DisplayRole):
        self._markers[index]["value"] = value
        self._markers[index]["color"] = color

        new_index = self.createIndex(index, index)
        self.dataChanged.emit(new_index, new_index, [])

        return True

    def roleNames(self):
        return {
            MarkerModel.PositionRole: b"position_marker",
            MarkerModel.ColorRole: b"color_marker",
            MarkerModel.NameRole: b"name_marker",
            MarkerModel.ValueRole: b"value_marker",
            MarkerModel.DateRole: b"dater_marker"
        }

    def append_marker(self, marker):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()
