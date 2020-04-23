from PySide2.QtCore import Qt, QRect
from PySide2.QtGui import QPainter, QColor, QPen, QLinearGradient, QBrush
from PySide2.QtWidgets import (QWidget, QGridLayout)

import numpy
import pandas as pd


class Spiral(QWidget):
    def __init__(self, data, city, attribute):
        super(Spiral, self).__init__()

        self.data = data
        self.city = city
        self.attribute = attribute

    def paintEvent(self, event):
        width  = self.width()
        height = self.height()

        painter = QPainter(self)

        pi = 3.141592654
        data_points_count, colors, attribute_values, values, months = self.process_data(self.data, self.city, self.attribute)

        rotations = int(numpy.floor(data_points_count/12))
        spiral_points = (data_points_count//12)*12

        radius_min = 0.1
        radius_max = 0.7

        element_size_min = 5
        element_size_max = 7

        for i in range(spiral_points):
            angle = -2.0*pi * i / spiral_points
            k = i / spiral_points

            radius = (1.0 - k)*radius_min + k*radius_max

            # transformacia suradnic z <-1, 1> sveta do <0, width> a <0, height>
            x = radius*numpy.sin(angle*rotations)
            y = radius*numpy.cos(angle*rotations)

            x_t = int(3*width/4*(x + 1.0)/2.0)
            y_t = int(height*(y + 1.0)/2.0)

            # Set Point Color
            rgb_color = colors.loc[colors.index[i]]
            color = QColor(Qt.black)
            color.setRgb(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
            point_color = color

            # Set Point Radius
            kr = (i//12)/(spiral_points//12)
            circle_radius = (1.0 - kr)*element_size_min + kr*element_size_max*2

            # Draw Point
            painter.setBrush(point_color)
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.drawEllipse(x_t, y_t, circle_radius, circle_radius)

        for i in range(12):
            text = months[i]
            angle = -2.0*pi * i / 12
            k = i / 12

            radius = 1.25*radius_max

            x = radius*numpy.sin(angle)
            y = radius*numpy.cos(angle)

            x_t = int(3*width/4*(x + 1.0)/2.0)
            y_t = int(height*(y + 1.1)/2.0)

            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
            painter.drawText(x_t, y_t, text)

        # Create Colorbar Legend
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))

        for j in range(7):
            text = str(values[6-j])
            rgb_color = attribute_values.get(6-j)
            fill_color = QColor(Qt.white)
            fill_color.setRgb(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
            brush.setColor(fill_color)

            rect_width = 20
            rect_height = 15
            gap = 15

            # Counts Rectangle and Text Coordinates
            x_point = (4*width)/5
            y_point = (height)/7 + (j+1)*rect_height + j*gap
            text_x = x_point + rect_width + gap
            text_y = y_point + 10

            # Draw
            rect = QRect(x_point, y_point, rect_width, rect_height)
            painter.fillRect(rect, brush)
            painter.drawText(text_x, text_y, text)

        painter.end()

    def process_data(self, data, city, attribute):
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['month_year'] = data['datetime'].dt.to_period('M')

        tmp = data.groupby(['city','month_year']).agg({attribute : 'mean'})

        max_value = round(tmp[attribute].max())
        min_value = round(tmp[attribute].min())

        diff = max_value - min_value
        step = round(1 / 6 * diff)

        filtered_city = data[data['city'] == city]
        att_data = filtered_city[['datetime', attribute, 'month_year']]

        data_points_count = len(att_data['month_year'].unique())

        if attribute == 'pressure':
            attribute_values = {0: [255,255,255], 1: [204,229,255], 2: [102,178,255], 3: [0,128,255], \
            4: [0,0,255], 5: [0,0,102], 6: [0,0,51]}
        elif attribute == 'temperature':
            attribute_values = {0: [0,102,204], 1: [102,178,255], 2: [204,229,255], 3: [255,204,204], \
            4: [255,102,102], 5: [204,0,0], 6: [102,0,0]}

        att_data = att_data.groupby('month_year').agg({attribute : 'mean'})

        att_data = att_data.reset_index()

        values = numpy.array([min_value, min_value + 1*step, min_value + 2*step, min_value + 3*step, \
        min_value + 4*step, min_value + 5*step, max_value])

        att_data['distances'] = att_data[attribute].apply(lambda x: abs(x - values))
        att_data['index'] = att_data['distances'].apply(lambda x: numpy.argmin(x))
        att_data['color'] = att_data['index'].apply(lambda x: attribute_values.get(x))

        att_data = att_data.reset_index(drop='True')
        att_data['month'] = att_data['month_year'].dt.month

        months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", \
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

        att_data['month'] = att_data['month'].apply(lambda x: months.get(x))

        return data_points_count, att_data['color'], attribute_values, values, att_data['month']
