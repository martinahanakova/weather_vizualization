from PySide2.QtCore import (QAbstractListModel, Qt, QModelIndex)


class MarkerModel(QAbstractListModel):
    PositionRole, ColorRole, NameRole, ValueRole, ColorRole = range(Qt.UserRole, Qt.UserRole + 5)

    def __init__(self, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []

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

    def setData(self, index, value, color, role=Qt.DisplayRole):
    #    print(self._markers[index]["value"])
        self._markers[index]["value"] = value
        self._markers[index]["color"] = color
       # print(self._markers[index]["value"])
        newIndex = self.createIndex(index, index)
        #print(newIndex)
        self.dataChanged.emit(newIndex, newIndex, [])
        return True

    def roleNames(self):
        return {MarkerModel.PositionRole: b"position_marker", MarkerModel.ColorRole: b"color_marker",
    MarkerModel.NameRole: b"name_marker", MarkerModel.ValueRole: b"value_marker", MarkerModel.ColorRole: b"color_marker"}


    def appendMarker(self, marker):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()
