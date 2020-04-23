from PySide2.QtCore import *
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QMainWindow, QAction


class MainWindow(QMainWindow):
    def __init__(self, map):
        QMainWindow.__init__(self)
        self.setWindowTitle("Overview")

        self.setCentralWidget(map)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        ## Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 1, geometry.height() * 1)
