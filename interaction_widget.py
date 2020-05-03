from PySide2.QtCore import Qt, QFile
from PySide2 import QtUiTools
from PySide2.QtGui import QPainter, QColor, QPen, QLinearGradient, QBrush
from PySide2.QtWidgets import (QWidget, QGridLayout)
from PySide2.QtCharts import QtCharts


class Interaction(QWidget):
    def __init__(self):
        super(Interaction, self).__init__()

        loader = QtUiTools.QUiLoader()

        file = QFile("detail_interaction.ui")

        widget = QWidget()
        widget = loader.load(file)

        #WidgetUI = uic.loadUiType('mywidget.ui'))
