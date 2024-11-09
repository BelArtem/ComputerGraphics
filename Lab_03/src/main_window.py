from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QGraphicsScene, QGraphicsView, \
    QGraphicsTextItem, QLineEdit, QLabel, QHBoxLayout

from PyQt5.QtGui import QPen, QColor, QFont, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp

import time
import random


class MainWindow(QWidget):
    def __init__(self):
        self.CELL_SIZE = 20
        super().__init__()
        self.layout = QVBoxLayout()
        self.initUI()
        self.scene = QGraphicsScene(self)
        self.view = ZoomableGraphicsView(self.scene)

        self.layout.addWidget(self.view)

        self.setLayout(self.layout)
        self.draw_grid()

    def initUI(self):
        self.setWindowTitle('Raster Algorithms')
        self.setGeometry(100, 100, 800, 600)

        x_rx = QRegExp("^(-?([1][0-9]|20)|-?([0-9]))$")
        x_val = QRegExpValidator(x_rx, self)
        y_rx = QRegExp("^(-?([1][0-5]|15)|-?([0-9]|[1][0-5]))$")
        y_val = QRegExpValidator(y_rx, self)
        r_rx = QRegExp("^(0|[1-9]|1[0-5])$")
        r_val = QRegExpValidator(r_rx, self)

        self.start_x_input = QLineEdit(self)
        self.start_y_input = QLineEdit(self)
        self.end_x_input = QLineEdit(self)
        self.end_y_input = QLineEdit(self)
        self.radius_input = QLineEdit(self)

        self.start_x_input.setPlaceholderText("X start")
        self.start_y_input.setPlaceholderText("y start")
        self.end_x_input.setPlaceholderText("x end")
        self.end_y_input.setPlaceholderText("y end")
        self.radius_input.setPlaceholderText("radius")

        self.start_x_input.setValidator(x_val)
        self.end_x_input.setValidator(x_val)
        self.start_y_input.setValidator(y_val)
        self.end_y_input.setValidator(y_val)
        self.radius_input.setValidator(r_val)

        btn_bresenham = QPushButton('Bresenham Line', self)
        btn_bresenham.clicked.connect(self.draw_bresenham_line)

        btn_dda = QPushButton('DDA Line', self)
        btn_dda.clicked.connect(self.draw_dda_line)

        btn_bresenham_circle = QPushButton('Bresenham Circle', self)
        btn_bresenham_circle.clicked.connect(self.draw_bresenham_circle)

        btn_step_by_step = QPushButton('Step by step', self)
        btn_step_by_step.clicked.connect(self.draw_step_by_step)

        btn_test = QPushButton('Test', self)
        btn_test.clicked.connect(self.test_all_algorithms)

        btn_clear = QPushButton('Clear', self)
        btn_clear.clicked.connect(self.clear_grid)

        v1_layout = QVBoxLayout()
        v2_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        v1_layout.addWidget(QLabel("Start point:"))
        v1_layout.addWidget(self.start_x_input)
        v1_layout.addWidget(self.start_y_input)
        v2_layout.addWidget(QLabel("End point:"))
        v2_layout.addWidget(self.end_x_input)
        v2_layout.addWidget(self.end_y_input)
        h_layout.addLayout(v1_layout)
        h_layout.addLayout(v2_layout)
        self.layout.addLayout(h_layout)

        self.layout.addWidget(QLabel("Circle radius:"))
        self.layout.addWidget(self.radius_input)

        self.layout.addWidget(btn_bresenham)
        self.layout.addWidget(btn_dda)
        self.layout.addWidget(btn_bresenham_circle)
        self.layout.addWidget(btn_step_by_step)
        test_clear_layout = QHBoxLayout()
        test_clear_layout.addWidget(btn_clear)
        test_clear_layout.addWidget(btn_test)
        self.layout.addLayout(test_clear_layout)

    def draw_grid(self):
        pen = QPen(QColor(200, 200, 200))

        self.scene.clear()

        for i in range(-420, 421, self.CELL_SIZE):
            self.scene.addLine(i, -320, i, 320, pen)
        for j in range(-320, 321, self.CELL_SIZE):
            self.scene.addLine(-420, j, 420, j, pen)

        self.scene.addLine(0, -320, 0, 320, QPen(QColor(0, 0, 0), 2))  # Ось Y
        self.scene.addLine(-420, 0, 420, 0, QPen(QColor(0, 0, 0), 2))  # Ось X

        font = QFont()
        font.setPointSize(10)

        x_label = QGraphicsTextItem("X")
        x_label.setFont(font)
        x_label.setPos(400, 10)
        self.scene.addItem(x_label)

        y_label = QGraphicsTextItem("Y")
        y_label.setFont(font)
        y_label.setPos(10, -310)
        self.scene.addItem(y_label)

        font.setPointSize(4)
        for i in range(-420, 421, self.CELL_SIZE):
            x_scale_label = QGraphicsTextItem(str(i // self.CELL_SIZE))
            x_scale_label.setFont(font)
            x_scale_label.setPos(i-10, 0)
            self.scene.addItem(x_scale_label)

        for i in range(-320, 321, self.CELL_SIZE):
            y_scale_label = QGraphicsTextItem(str(-(i // self.CELL_SIZE)))
            y_scale_label.setFont(font)
            y_scale_label.setPos(-20, i-10)
            self.scene.addItem(y_scale_label)

    def draw_bresenham_line(self):
        x0 = int(self.start_x_input.text() if self.start_x_input.text() != "" else 0)
        y0 = int(self.start_y_input.text() if self.start_y_input.text() != "" else 0)
        x1 = int(self.end_x_input.text() if self.end_x_input.text() != "" else 0)
        y1 = int(self.end_y_input.text() if self.end_y_input.text() != "" else 0)

        y0 = -y0
        y1 = -y1

        self.clear_grid()
        self.bresenham_line_algorithm(x0, y0, x1, y1)

    def bresenham_line_algorithm(self, x0, y0, x1, y1):
        if y1 - y0 < 0:
            y1 -= 1
            y0 -= 1
        if x1 - x0 < 0:
            x1 -= 1
            x0 -= 1
        dx = x1 - x0
        dy = y1 - y0
        sx = 1 if dx > 0 else -1
        sy = 1 if dy > 0 else -1
        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            err = dx / 2.0
            while x0 != x1:
                self.scene.addRect(x0 * self.CELL_SIZE, y0 * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE,
                                   QPen(Qt.black), brush=QColor(0, 0, 0))
                err -= dy
                if err < 0:
                    y0 += sy
                    err += dx
                x0 += sx
        else:
            err = dy / 2.0
            while y0 != y1:
                self.scene.addRect(x0 * self.CELL_SIZE, y0 * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE,
                                   QPen(Qt.black), brush=QColor(0, 0, 0))
                err -= dx
                if err < 0:
                    x0 += sx
                    err += dy
                y0 += sy

    def draw_dda_line(self):
        x0 = int(self.start_x_input.text() if self.start_x_input.text() != "" else 0)
        y0 = int(self.start_y_input.text() if self.start_y_input.text() != "" else 0)
        x1 = int(self.end_x_input.text() if self.end_x_input.text() != "" else 0)
        y1 = int(self.end_y_input.text() if self.end_y_input.text() != "" else 0)

        y0 = -y0
        y1 = -y1

        if y1 - y0 < 0:
            y1 -= 1
            y0 -= 1
        if x1 - x0 < 0:
            x1 -= 1
            x0 -= 1

        self.clear_grid()
        self.dda_line_algorithm(x0, y0, x1, y1)

    def dda_line_algorithm(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))

        x_inc = dx / float(steps)
        y_inc = dy / float(steps)

        x = x0
        y = y0

        for _ in range(steps + 1):
            self.scene.addRect(round(x) * self.CELL_SIZE, round(y) * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE,
                               QPen(Qt.red), brush=QColor(255, 0, 0))
            x += x_inc
            y += y_inc

    def draw_bresenham_circle(self):
        x_center = int(self.start_x_input.text() if self.start_x_input.text() != "" else 0)
        y_center = -int(self.start_y_input.text() if self.start_y_input.text() != "" else 0)
        radius = int(self.radius_input.text() if self.radius_input.text() != "" else 0)

        self.clear_grid()
        self.bresenham_circle_algorithm(x_center, y_center, radius)

    def bresenham_circle_algorithm(self, x_center, y_center, radius):
        x = radius
        y = 0
        p = 1 - radius

        while x >= y:
            points = [
                (x_center + x, y_center + y),
                (x_center + y, y_center + x),
                (x_center - y - 1, y_center + x),
                (x_center - x - 1, y_center + y),
                (x_center - x - 1, y_center - y - 1),
                (x_center - y - 1, y_center - x - 1),
                (x_center + y, y_center - x - 1),
                (x_center + x, y_center - y - 1),
            ]
            for point in points:
                self.scene.addRect(point[0] * self.CELL_SIZE, point[1] * self.CELL_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE,
                                   QPen(Qt.blue), brush=QColor(0, 0, 255))

            y += 1
            if p <= 0:
                p = p + (2 * y) + 1
            else:
                x -= 1
                p = p + (2 * y) - (2 * x) + 1

    def draw_step_by_step(self):
        x0 = int(self.start_x_input.text() if self.start_x_input.text() != "" else 0)
        y0 = -int(self.start_y_input.text() if self.start_y_input.text() != "" else 0)
        x1 = int(self.end_x_input.text() if self.end_x_input.text() != "" else 0)
        y1 = -int(self.end_y_input.text() if self.end_y_input.text() != "" else 0)

        if y1 - y0 < 0:
            y1 -= 1
            y0 -= 1
        if x1 - x0 < 0:
            x1 -= 1
            x0 -= 1

        self.clear_grid()
        self.step_by_step_algorithm(x0, y0, x1, y1)

    def step_by_step_algorithm(self, x0, y0, x1, y1):
        step = 0.01
        A = y0 - y1
        B = x1 - x0
        C = x0 * y1 - x1 * y0
        direction_x = x1 - x0
        if abs(direction_x) < 0.01:
            direction_y = y1 - y0
            if abs(direction_y) < 0.01:
                self.scene.addRect(x0 * self.CELL_SIZE, y0 * self.CELL_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE,
                                   QPen(QColor(255, 0, 255)), brush=QColor(255, 0, 255))
                return
            y = min(y0, y1)
            while y < max(y0, y1):
                self.scene.addRect(x0 * self.CELL_SIZE, round(y) * self.CELL_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE,
                                   QPen(QColor(255, 0, 255)), brush=QColor(255, 0, 255))
                y += step
            return
        x = min(x0, x1)
        while x < max(x0, x1):
            y = (-C - A * x) / B
            self.scene.addRect(round(x) * self.CELL_SIZE, round(y) * self.CELL_SIZE,
                               self.CELL_SIZE, self.CELL_SIZE,
                               QPen(QColor(255, 0, 255)), brush=QColor(255, 0, 255))

            x += step

    def test_all_algorithms(self):
        f = open('test_results.txt', 'w')
        points = []
        for i in range(200):
            x0, x1 = random.randint(-20, 20), random.randint(-20, 20)
            y0, y1 = random.randint(-15, 15), random.randint(-15, 15)
            points.append((x0, y0, x1, y1))

        self.clear_grid()

        step_by_step_time = self.test_step_by_step(points)
        f.write("Step by step algorithm " + str(step_by_step_time) + ' s\n')

        self.clear_grid()

        bresenham_line_time = self.test_bresenham(points)
        f.write("Bresenham line algorithm " + str(bresenham_line_time) + ' s\n')

        self.clear_grid()

        dda_line_time = self.test_dda(points)
        f.write("DDA line algorithm " + str(dda_line_time) + ' s\n')

        self.clear_grid()

        points = []
        for i in range(200):
            x, y = random.randint(-20, 20), random.randint(-15, 15)
            r = random.randint(0, min(20 - abs(x), 15 - abs(y)))
            points.append((x, y, r))

        circle_time = self.test_circle(points)
        f.write("Circle algorithm " + str(circle_time) + ' s\n')

        self.clear_grid()

    def test_step_by_step(self, points):
        start = time.time()
        for point in points:
            self.step_by_step_algorithm(point[0], point[1], point[2], point[3])
        end = time.time()
        return end - start

    def test_bresenham(self, points):
        start = time.time()
        for point in points:
            self.bresenham_line_algorithm(point[0], point[1], point[2], point[3])
        end = time.time()
        return end - start

    def test_dda(self, points):
        start = time.time()
        for point in points:
            self.dda_line_algorithm(point[0], point[1], point[2], point[3])
        end = time.time()
        return end - start

    def test_circle(self, points):
        start = time.time()
        for point in points:
            self.bresenham_circle_algorithm(point[0], point[1], point[2])
        end = time.time()
        return end - start

    def clear_grid(self):
        self.scene.clear()
        self.draw_grid()


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            factor = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
            self.scale_view(factor)

    def scale_view(self, scale_factor):
        self.scale(scale_factor, scale_factor)
