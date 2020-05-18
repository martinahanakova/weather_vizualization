from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QPainter, QColor, QPen, QPolygonF
from PySide2.QtWidgets import (QWidget)

import numpy
import pandas as pd


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
        self.radius = 0.85

        self.month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        self.all_flag = 1
        self.year_flag = 0
        self.month_flag = 0
        self.day_flag = 0
        self.hour_flag = 0

        self.year = None
        self.month = None
        self.day = None
        self.hour = None

    def set_paint(self, all_flag, year_flag, month_flag, day_flag, year=None, month=None, day=None):
        self.all_flag = all_flag
        self.year_flag = year_flag
        self.month_flag = month_flag
        self.day_flag = day_flag

        self.year = year
        self.month = month
        self.day = day

    def paintEvent(self, event):
        painter = QPainter(self)

        if self.all_flag:
            self.paint_all(painter)
        elif self.year_flag:
            self.paint_detail(painter, 0, 0)
        elif self.month_flag:
            self.paint_detail(painter, 1, 0)
        elif self.day_flag:
            self.paint_detail(painter, 1, 1)

        painter.end()

    def paint_all(self, painter):
        x0 = 0.0 + (self.width() - self.height())/self.height()
        y0 = 0.0

        x, y = self.convert_center(0.0, 0.0)

        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))

        painter.drawEllipse(QPointF(x, y), self.radius*self.height()/2, self.radius*self.height()/2)

        months = 12

        processed_data = self.process_data(self.data, self.city, self.radius)

        for month_id in range(months):
            self.paint_arc_for_month(painter, processed_data, x0, y0, month_id+1, months, 'month')

        self.paint_spacing_lines(painter, x, y, months)

        self.paint_labels(painter, x0, y0, self.radius, self.month_labels)

    def paint_detail(self, painter, month_flag, day_flag):
        x0 = 0.0 + (self.width() - self.height()) / self.height()
        y0 = 0.0

        x, y = self.convert_center(0.0, 0.0)

        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))

        painter.drawEllipse(QPointF(x, y), self.radius * self.height() / 2, self.radius * self.height() / 2)

        processed_data = self.process_detail_data(self.data, self.city, self.radius, month_flag, day_flag)

        count_of_steps = len(processed_data)

        if month_flag and not day_flag:
            labels = processed_data['day']
            time_period = 'day'
        elif day_flag:
            labels = processed_data['hour']
            time_period = 'hour'
        else:
            labels = processed_data['month_name']
            time_period = 'month'

        for step in processed_data[time_period]:
            self.paint_arc_for_month(painter, processed_data, x0, y0, step, count_of_steps, time_period)

        self.paint_spacing_lines(painter, x, y, count_of_steps)

        self.paint_labels(painter, x0, y0, self.radius, labels)

    def paint_arc_for_month(self, painter, data, x0, y0, step, count_of_steps=12, time_period=None):
        painter.setPen(QPen(self.arc_line_color, self.arc_line_width, Qt.SolidLine))
        painter.setBrush(self.arc_fill_color)

        filtered_data = data[data[time_period] == step]

        for i in range(len(filtered_data)):
            arc_length = 2.0*self.pi/count_of_steps
            phi_center = 2.0*self.pi*(step-1)/count_of_steps

            arc_radius = filtered_data["radius"].loc[filtered_data.index.values[i]]

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

    def paint_spacing_lines(self, painter, x, y, count_of_steps):
        painter.setPen(QPen(self.text_color, 2, Qt.SolidLine))
        painter.setBrush(self.text_color)

        height = self.height()

        for i in range(count_of_steps):
            angle = 2.0 * self.pi * i / count_of_steps

            # Point 2 Coordinates
            x_p2 = self.radius * (height / 2) * numpy.cos(angle)
            y_p2 = self.radius * (height / 2) * numpy.sin(angle)

            x_2 = x + x_p2
            y_2 = y + y_p2

            painter.drawLine(QPointF(x, y), QPointF(x_2, y_2))

    def paint_labels(self, painter, x0, y0, radius, labels):
        steps = len(labels)

        radius = radius + 0.11

        for n in range(steps):
            phi = 2.0*self.pi*n/steps + 0.5*2.0*self.pi/steps

            x1 = x0 + radius*numpy.cos(phi) - 0.09
            y1 = y0 + radius*numpy.sin(phi) + 0.05

            xt, yt = self.convert_position(x1, y1)

            text = str(labels[n])
            painter.setPen(QPen(self.text_color, 2, Qt.SolidLine))
            painter.drawText(xt, yt, text)

    def convert_position(self, x, y):
        width = self.width()
        height = self.height()

        d = numpy.min([width, height])

        x_t = d*(x + 1.0)/2.0
        y_t = d*(y + 1.0)/2.0

        return x_t, y_t

    def convert_center(self, x, y):
        width  = self.width()
        height = self.height()

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

        att_data['radius'] = ""
        previous_month = 1
        sum_values = 0

        for row in range(len(att_data.index)):
                actual_month = att_data["month"].loc[att_data.index.values[row]]

                if actual_month != previous_month:
                    sum_values = att_data["per_year_from_radius"].loc[att_data.index.values[row]]
                    previous_month = actual_month
                else:
                    sum_values = sum_values + att_data["per_year_from_radius"].loc[att_data.index.values[row]]

                att_data.loc[att_data.index.values[row], "radius"] = sum_values

        att_data = att_data.sort_values(['month', 'year'], ascending=[True, False])
        att_data = att_data.reset_index(drop=True)

        return att_data

    def process_detail_data(self, data, city, radius, month_flag, day_flag):
        data['datetime'] = pd.to_datetime(data['datetime'])

        data['year'] = data['datetime'].dt.year
        data['month'] = data['datetime'].dt.month
        data['day'] = data['datetime'].dt.day
        data['hour'] = data['datetime'].dt.hour

        filtered_city = data[data['city'] == city]

        filtered_data = filtered_city[filtered_city['year'] == int(self.year)]

        if month_flag:
            filtered_data = filtered_data[filtered_data['month'] == int(self.month)]

            if day_flag:
                filtered_data = filtered_data[filtered_data['day'] == int(self.day)]
                att_data = filtered_data[['datetime', 'humidity', 'hour']]
            else:
                att_data = filtered_data[['datetime', 'humidity', 'day']]
                att_data = att_data.groupby('day').agg({'humidity': 'mean'})
        else:
            att_data = filtered_data[['datetime', 'humidity', 'month']]
            att_data = att_data.groupby('month').agg({'humidity': 'mean'})

        att_data = att_data.reset_index()

        max_value = att_data['humidity'].max()

        att_data['radius'] = att_data['humidity'].apply(
            lambda x: (x / max_value) * radius)

        months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", \
                  7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

        att_data['month_name'] = att_data['month'].apply(lambda x: months.get(x))

        return att_data
