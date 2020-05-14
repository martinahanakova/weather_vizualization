from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QPixmap, QImage, QPainter
from PySide2.QtCore import QByteArray, Qt

import plotly.express as px
import numpy as np


class WindrosePlot(QWidget):
    def __init__(self, data, city):
        super(WindrosePlot, self).__init__()

        self.data = data
        self.city = city

    def paintEvent(self, event):
        wind_data = self.process_data(self.data, self.city)

        painter = QPainter(self)

        figure = px.bar_polar(wind_data, r="frequency", theta="direction",\
                           color="wind_speed", template="plotly_dark",\
                           )

        figure.update_layout({
                    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                    })

        figure.update_layout(legend=dict(font=dict(size=50)))

        img_bytes = figure.to_image(format="png")

        img = QImage()
        img.loadFromData(img_bytes)

        pixmap = QPixmap(img)

        pixmap = pixmap.scaled(self.width(), 1.2*self.height(), Qt.KeepAspectRatio)

        painter.drawPixmap(0, 0, pixmap)

        painter.end()

    def process_data(self, data, city):
        data = data[data['city'] == city]

        data = data[['wind_speed', 'wind_direction']]
        data_len = len(data)

        directions = {0: 'N', 1: 'NNE', 2: 'NE', 3: 'ENE', 4: 'E', 5: 'ESE', 6: 'SE', 7: 'SSE', 8: 'S', \
        9: 'SSW', 10: 'SW', 11: 'WSW', 12: 'W', 13: 'WNW', 14: 'NW', 15: 'NNW', 16: 'N'}

        angles = np.array([0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5, 360])

        data['distances'] = data['wind_direction'].apply(lambda x: abs(x - angles))
        data['index'] = data['distances'].apply(lambda x: np.argmin(x))
        data['direction'] = data['index'].apply(lambda x: directions.get(x))

        counts = data.groupby(['direction', 'wind_speed']).size()
        counts = counts.reset_index()
        counts['frequency'] = counts[0].apply(lambda x: x / data_len)
        counts = counts.dropna()

        sorter = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

        sorterIndex = dict(zip(sorter,range(len(sorter))))
        counts['rank'] = counts['direction'].map(sorterIndex)
        counts = counts.sort_values(['rank'])

        return counts
