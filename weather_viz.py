from PySide2.QtWidgets import QApplication

from main_window import MainWindow
from main_widget import Widget
from detail_widget import DetailWidget
from detail_window import DetailWindow

import sys
import argparse
import pandas as pd


def read_data(fname):
    # Read the CSV content
    df = pd.read_csv(fname)

    return df


if __name__ == "__main__":
    options = argparse.ArgumentParser()
    options.add_argument("-f", "--file", type=str, required=True)
    args = options.parse_args()
    data = read_data(args.file)

    # Qt Application
    app = QApplication(sys.argv)

    widget = DetailWidget(data)
    window = DetailWindow(widget)

    #widget = Widget(data)
    #window = MainWindow(widget)
    window.show()

    sys.exit(app.exec_())
