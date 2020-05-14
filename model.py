from PySide2.QtCore import (QAbstractListModel, Qt, QModelIndex, Slot)

from detail_widget import DetailWidget
from detail_window import DetailWindow


class MarkerModel(QAbstractListModel):
    PositionRole, ColorRole, NameRole, ValueRole = range(Qt.UserRole, Qt.UserRole + 4)

    def __init__(self, data, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []
        self.model_data = data

    @Slot(str)
    def open_detail(self, city):
        widget = DetailWidget(self.model_data, city)
        self.dialog = DetailWindow(widget, city)

        self.dialog.show()

    def get_row_count(self):
        return len(self._markers)

    def data(self, index, role=Qt.DisplayRole):
        if 0 <= index.row() < self.get_row_count():
            if role == MarkerModel.PositionRole:
                return self._markers[index.row()]["position"]
            elif role == MarkerModel.ColorRole:
                return self._markers[index.row()]["color"]
            elif role == MarkerModel.NameRole:
                return self._markers[index.row()]["name"]
            elif role == MarkerModel.ValueRole:
                return self._markers[index.row()]["value"]

    def set_data(self, index, value):
        self._markers[index]["value"] = value
        new_index = self.createIndex(index, index)
        self.dataChanged.emit(new_index, new_index, [])
        return True

    def roleNames(self):
        return {
            MarkerModel.PositionRole: b"position_marker",
            MarkerModel.ColorRole: b"color_marker",
            MarkerModel.NameRole: b"name_marker",
            MarkerModel.ValueRole: b"value_marker"}

    def append_marker(self, marker):
        self.beginInsertRows(QModelIndex(), self.get_row_count(), self.get_row_count())
        self._markers.append(marker)
        self.endInsertRows()
