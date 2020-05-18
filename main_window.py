from PySide2.QtCore import *
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self, map):
        QMainWindow.__init__(self)
        self.setWindowTitle("Overview")

        self.setCentralWidget(map)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 1, geometry.height() * 1)
