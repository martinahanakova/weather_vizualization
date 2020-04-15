from PySide2.QtCore import Qt, QRect, QPointF
from PySide2.QtGui import QPainter, QColor, QPen, QLinearGradient, QBrush, QPolygonF
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

        self.arc_line_color = Qt.white
        self.arc_fill_color = QColor(0, 191,255)
        self.text_color = Qt.white

        self.arc_line_width = 1.0
        self.pi = 3.141592654

        self.labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def paintEvent(self, event):
        width  = self.width()
        height = self.height()

        painter = QPainter(self)

        self.radius = 0.85

        x0 = 0.0 + (self.width() - self.height())/self.height()
        y0 = 0.0

        x, y = self.convert_center(0.0, 0.0)

        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))

        painter.drawEllipse(QPointF(x, y), self.radius*self.height()/2, self.radius*self.height()/2)

        months = 12

        proccessed_data = self.process_data(self.data, self.city, self.radius)

        for month_id in range(months):
            self.paint_arc_for_month(painter, proccessed_data, x0, y0, month_id)

        for i in range(months):
                    angle = 2.0*self.pi * i/months

                    # Point 2 Coordinates
                    x_p2 = self.radius*(height/2)*numpy.cos(angle)
                    y_p2 = self.radius*(height/2)*numpy.sin(angle)

                    x_2 = int(x + x_p2)
                    y_2 = int(y + y_p2)

                    painter.drawLine(QPointF(x, y), QPointF(x_2, y_2))

        self.paint_labels(painter, x0, y0, self.radius, self.labels)

        painter.end()

    def paint_arc_for_month(self, painter, data, x0, y0, month_id, months = 12):
        painter.setPen(QPen(self.arc_line_color, self.arc_line_width, Qt.SolidLine))
        painter.setBrush(self.arc_fill_color)

        month_data = data[data['month'] == month_id+1]

        for i in range(len(month_data)):
            arc_length = 2.0*self.pi/months
            phi_center = 2.0*self.pi*month_id/months

            arc_radius = month_data["sum_accross_years"].loc[month_data.index.values[i]]

            polygon_points = self.compute_circle_arc_polygon(x0, y0, arc_radius, phi_center, arc_length)
            painter.drawConvexPolygon(polygon_points)

    def compute_circle_arc_polygon(self, x0, y0, radius, phi_begin, arc_length, steps = 32):
        polygon = QPolygonF()

        x0_t, y0_t = self.convert_position(x0, y0)
        polygon.append(QPointF(x0_t, y0_t))

        begin = phi_begin
        end = arc_length + phi_begin
        step = (begin - end)/steps

        angle = float(begin)

        for i in range(steps):
            x = x0 + radius*numpy.cos(angle)
            y = y0 + radius*numpy.sin(angle)

            x_t, y_t = self.convert_position(x, y)

            polygon.append(QPointF(x_t, y_t))

            angle+= step

        return polygon

    def paint_spacing_lines(self, painter, x0, y0, radius, steps):
        painter.setPen(QPen(self.text_color, 2, Qt.SolidLine))
        painter.setBrush(self.text_color)

        for n in range(steps):
            phi = 2.0*self.pi*n/steps

            x1 = x0 + radius*numpy.cos(phi)
            y1 = y0 + radius*numpy.sin(phi)

            x0_t, y0_t = self.convert_position(x0, y0)
            x1_t, y1_t = self.convert_position(x1, y1)

            painter.drawLine(x0_t, y0_t, x1_t, y1_t)

    def paint_labels(self, painter, x0, y0, radius, labels):
        steps = len(labels)

        radius = radius + 0.11

        for n in range(steps):
            phi = 2.0*self.pi*n/steps + 0.5*2.0*self.pi/steps

            x1 = x0 + radius*numpy.cos(phi) - 0.09
            y1 = y0 + radius*numpy.sin(phi) + 0.05

            xt, yt = self.convert_position(x1, y1)

            text = labels[n]
            painter.setPen(QPen(self.text_color, 2, Qt.SolidLine))
            painter.drawText(xt, yt, labels[n])

    def convert_position(self, x, y):
        width  = self.width()
        height = self.height()

        d = numpy.min([width, height])

        x_t = int(d*(x + 1.0)/2.0)
        y_t = int(d*(y + 1.0)/2.0)

        return x_t, y_t

    def convert_center(self, x, y):
        width  = self.width()
        height = self.height()

        d = numpy.min([width, height])

        x_t = int(width*(x + 1.0)/2.0)
        y_t = int(height*(y + 1.0)/2.0)

        return x_t, y_t

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

