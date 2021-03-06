from PySide2.QtCore import *
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction


class DetailWindow(QMainWindow):
    def __init__(self, widget, city):
        QMainWindow.__init__(self)

        self.setWindowTitle("Detail of " + city)

        self.setCentralWidget(widget)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(0.8*geometry.width(), geometry.height())
