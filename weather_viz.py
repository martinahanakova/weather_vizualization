from PySide2.QtWidgets import QApplication

from model import MarkerModel
from map_widget import MapWidget
from main_window import MainWindow
from detail_widget import DetailWidget
from detail_window import DetailWindow
from bars_widget_test import BarsWidgetTest


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

    #widget = DetailWidget(data)
    #window = DetailWindow(widget)

    model = MarkerModel(data)
    widget = MapWidget(data, model)
    #widget = BarsWidgetTest(data, model)
    window = MainWindow(widget)

    window.show()

    sys.exit(app.exec_())
