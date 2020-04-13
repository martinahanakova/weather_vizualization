from PySide2.QtCore import Qt, QRect, QPointF
from PySide2.QtGui import QPainter, QColor, QPen, QLinearGradient, QBrush
from PySide2.QtWidgets import (QWidget, QGridLayout)
from PySide2.QtCharts import QtCharts

import numpy
import pandas as pd
import math


class HumidityPlot(QWidget):
    def __init__(self, data, city):
        super(HumidityPlot, self).__init__()

        self.data = data
        self.city = city

    def paintEvent(self, event):
        width  = self.width()
        height = self.height()

        painter = QPainter(self)

        pi = 3.141592654

        radius = (height/2) - 20

        x = width / 2
        y = height / 2

        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))

        painter.drawEllipse(QPointF(x, y), radius, radius)

        months = 12

        for i in range(months):
            angle = 2.0*pi * i/months

            # Point 2 Coordinates
            x_p2 = radius*numpy.sin(angle)
            y_p2 = radius*numpy.cos(angle)

            x_2 = int(x + x_p2)
            y_2 = int(y + y_p2)

            painter.drawLine(QPointF(x, y), QPointF(x_2, y_2))

        proccessed_data = self.process_data(self.data, self.city, radius)

        counter = 0

        for i in range(1):
            angle_1 = 2.0*pi * i/months
            angle_2 = 2.0*pi * (i+1)/months

            while True:
                actual_month = proccessed_data["month"].loc[proccessed_data.index.values[counter]]
                if counter+1 >= len(proccessed_data):
                    next_month = 13
                else:
                    next_month = proccessed_data["month"].loc[proccessed_data.index.values[counter+1]]

                radius_part = proccessed_data["sum_accross_years"].loc[proccessed_data.index.values[counter]]

                print(x, y)
                print(radius_part)

                x = 0
                y = 0

                x_0 = width*(x + 1.0)/2.0
                y_0 = height*(y + 1.0)/2.0

                x_0 = 0
                y_0 = 0

                radius_part = 0.5

                # Point 1 Coordinates
                x_p1 = radius_part*numpy.sin(angle_1)
                y_p1 = radius_part*numpy.cos(angle_1)

                x_1 = x_0 + x_p1
                y_1 = y_0 + y_p1

                print(x_p1, y_p1)

                # Point 2 Coordinates
                x_p2 = radius_part*numpy.sin(angle_2)
                y_p2 = radius_part*numpy.cos(angle_2)

                x_2 = x_0 + x_p2
                y_2 = y_0 + y_p2

                print(x_p2, y_p2)

                x_t = width*(x_0 + 1.0)/2.0
                y_t = height*(y_0 + 1.0)/2.0

                x_t1 = width*(x_1 + 1.0)/2.0
                y_t1 = height*(y_1 + 1.0)/2.0

                x_t2 = width*(x_2 + 1.0)/2.0
                y_t2 = height*(y_2 + 1.0)/2.0

                # Draw Wedge
                S = QPointF(x_t, y_t)
                A = QPointF(x_t1, y_t1)
                B = QPointF(x_t2, y_t2)

                print(x_t, y_t)
                print(x_t1, y_t1)
                print(x_t2, y_t2)

                halfSide = A.x()-S.x()
                rectangle = QRect(S.x() - halfSide,
                                 S.y() - halfSide,
                                 S.x() + halfSide,
                                 S.y() + halfSide)

                startAngle = 0
                spanAngle = (math.atan2(B.y()-S.y(),B.x()-S.x()) * 180 / pi) * 16;

                painter.drawArc(rectangle, startAngle, spanAngle);

                counter = counter + 1

                if actual_month != next_month:
                    break

        painter.end()

    def process_data(self, data, city, radius):
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['month_year'] = data['datetime'].dt.to_period('M')

        filtered_city = data[data['city'] == city]

        count_years = len(filtered_city['datetime'].dt.year.unique())

        att_data = filtered_city.groupby('month_year').agg({'humidity' : 'mean'})
        att_data = att_data.reset_index()

        att_data['month'] = att_data['month_year'].dt.month
        att_data['year'] = att_data['month_year'].dt.year

        att_data = att_data.sort_values(['month', 'year'], ascending=[True, True])

        max_value = att_data['humidity'].max()

        att_data['per_year_from_radius'] = att_data['humidity'].apply(lambda x: ((x / max_value) / count_years) * radius)

        att_data['sum_accross_years'] = ""
        previous_month = 1
        sum_values = 0

        for row in range(len(att_data.index)):
                actual_month = att_data["month"].loc[att_data.index.values[row]]

                if actual_month != previous_month:
                    sum_values = att_data["per_year_from_radius"].loc[att_data.index.values[row]]
                    previous_month = actual_month
                else:
                    sum_values = sum_values + att_data["per_year_from_radius"].loc[att_data.index.values[row]]

                att_data.loc[att_data.index.values[row], "sum_accross_years"] = sum_values

        att_data = att_data.sort_values(['month', 'year'], ascending=[True, False])
        att_data = att_data.reset_index(drop=True)

        return att_data

