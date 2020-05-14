from PySide2.QtCore import *
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QDialog, QAction


class DetailWindow(QDialog):
    def __init__(self, widget):
        QDialog.__init__(self)

        self.setWindowTitle("Detail")

        self.setCentralWidget(widget)

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        # Window dimensions
        geometry = qApp.desktop().availableGeometry(self)
        self.setFixedSize(geometry.width() * 0.6, geometry.height())
