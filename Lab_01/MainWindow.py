from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QColorDialog, QLineEdit, QWidget, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor

from Colors import Colors


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Color converter")
        self.setMinimumSize(600,600)
        self.setMaximumSize(1500,1000)

        self.color_display = QLabel()

        # Основной вертикальный layout
        self.layout = QVBoxLayout()

        # Слайдеры для RGB
        self.RGB_layout = QVBoxLayout()
        self.red_slider = self.CreateSliderLayout(Colors.RED, 255)
        self.green_slider = self.CreateSliderLayout(Colors.GREEN, 255)
        self.blue_slider = self.CreateSliderLayout(Colors.BLUE, 255)

        self.RGB_layout.addLayout(self.red_slider)
        self.RGB_layout.addLayout(self.green_slider)
        self.RGB_layout.addLayout(self.blue_slider)

        #Слайдеры для CMYK
        self.CMYK_layout = QVBoxLayout()
        self.cyan_slider = self.CreateSliderLayout(Colors.CYAN, 99)
        self.magenta_slider = self.CreateSliderLayout(Colors.MAGENTA, 99)
        self.yellow_slider = self.CreateSliderLayout(Colors.Yellow, 99)
        self.key_slider = self.CreateSliderLayout(Colors.KEY, 99)

        self.CMYK_layout.addLayout(self.cyan_slider)
        self.CMYK_layout.addLayout(self.magenta_slider)
        self.CMYK_layout.addLayout(self.yellow_slider)
        self.CMYK_layout.addLayout(self.key_slider)


        # Слайдеры для HSV
        self.HSV_layout = QVBoxLayout()
        self.hue_slider = self.CreateSliderLayout(Colors.HUE, 359)
        self.saturation_slider = self.CreateSliderLayout(Colors.SATURATION, 99)
        self.value_slider = self.CreateSliderLayout(Colors.VALUE, 99)

        self.HSV_layout.addLayout(self.hue_slider)
        self.HSV_layout.addLayout(self.saturation_slider)
        self.HSV_layout.addLayout(self.value_slider)

        self.CreateOutputFieldAndSelectButton()

        # Добавляем все элементы в layout
        self.layout.addLayout(self.output_layout)
        self.layout.addLayout(self.RGB_layout)
        self.layout.addLayout(self.CMYK_layout)
        self.layout.addLayout(self.HSV_layout)


        self.setLayout(self.layout)

    def CreateSliderLayout(self, color_name, upper_bound):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, upper_bound)
        slider.setValue(0)
        line_edit = QLineEdit("0")
        line_edit.setMaximumSize(50, 20)

        if color_name == Colors.RED or color_name == Colors.GREEN or color_name == Colors.BLUE:
            slider.valueChanged.connect(self.EditedRGB)
            #val = QIntValidator(0,255, line_edit)
            rx = QtCore.QRegExp("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)?$")
            val = QRegExpValidator(rx)
            line_edit.setValidator(val)
            line_edit.textChanged.connect(self.EditedRGB)

        elif color_name == Colors.HUE or color_name == Colors.SATURATION or color_name == Colors.VALUE:
            slider.valueChanged.connect(self.EditedHSV)
            if color_name == Colors.HUE:
                rx = QtCore.QRegExp("^(3[0-5][0-9]|[1-2][0-9]{2}|[0-9]{1,2})?$")
            else:
                rx = QtCore.QRegExp("^(99|[1-9][0-9]?|0)?$")

            val = QRegExpValidator(rx)
            line_edit.setValidator(val)
            line_edit.textChanged.connect(self.EditedHSV)
        else:
            slider.valueChanged.connect(self.EditedCMYK)
            rx = QtCore.QRegExp("^(99|[1-9][0-9]?|0)?$")
            val = QRegExpValidator(rx)
            line_edit.setValidator(val)
            line_edit.textChanged.connect(self.EditedCMYK)

        label = QLabel(color_name.value + ":")

        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(line_edit)
        h_layout.addWidget(slider)

        return h_layout

    def CreateOutputFieldAndSelectButton(self):
        # Label для отображения цвета
        self.output_layout = QHBoxLayout()

        self.color_display.setMinimumSize(200, 100)

        self.EditedRGB()

        change_color_button = QPushButton("Select color")
        change_color_button.setMinimumSize(100, 50)
        change_color_button.setMaximumSize(200,200)
        change_color_button.clicked.connect(self.SelectColor)

        self.output_layout.addWidget(self.color_display)
        self.output_layout.addWidget(change_color_button)


    def EditedRGB(self):
        if isinstance(self.sender(), QLineEdit):
            redText = self.red_slider.itemAt(1).widget().text();
            red = int(redText) if redText != '' else 0
            greenText = self.green_slider.itemAt(1).widget().text()
            green = int(greenText) if greenText != '' else 0
            blueText = self.blue_slider.itemAt(1).widget().text()
            blue = int(blueText) if blueText != '' else 0
            col = QColor(red, green, blue)
            self.red_slider.itemAt(2).widget().setValue(red)
            self.green_slider.itemAt(2).widget().setValue(green)
            self.blue_slider.itemAt(2).widget().setValue(blue)
        else:
            red = self.red_slider.itemAt(2).widget().value()
            green = self.green_slider.itemAt(2).widget().value()
            blue = self.blue_slider.itemAt(2).widget().value()
            col = QColor(red, green, blue)
            self.red_slider.itemAt(1).widget().setText(str(red))
            self.green_slider.itemAt(1).widget().setText(str(green))
            self.blue_slider.itemAt(1).widget().setText(str(blue))

        self.DisconnectSMYK()
        self.DisconnectHSV()

        self.UpdateCMYK(col)
        self.UpdateHSV(col)
        self.color_display.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});")

        self.ConnectSMYK()
        self.ConnectHSV()

    def EditedCMYK(self):
        if isinstance(self.sender(), QLineEdit):
            cyanText = self.cyan_slider.itemAt(1).widget().text()
            cyan = int(cyanText) if cyanText != "" else 0
            magentaText = self.magenta_slider.itemAt(1).widget().text()
            magenta = int(magentaText) if magentaText != "" else 0
            yellowText = self.yellow_slider.itemAt(1).widget().text()
            yellow = int(yellowText) if yellowText != "" else 0
            keyText = self.key_slider.itemAt(1).widget().text()
            key = int(keyText) if keyText != "" else 0
            col = QColor.fromCmykF(cyan/99, magenta/99, yellow/99, key/99)

            self.cyan_slider.itemAt(2).widget().setValue(cyan)
            self.magenta_slider.itemAt(2).widget().setValue(magenta)
            self.yellow_slider.itemAt(2).widget().setValue(yellow)
            self.key_slider.itemAt(2).widget().setValue(key)
        else:
            cyan = self.cyan_slider.itemAt(2).widget().value()
            magenta = self.magenta_slider.itemAt(2).widget().value()
            yellow = self.yellow_slider.itemAt(2).widget().value()
            key = self.key_slider.itemAt(2).widget().value()
            col = QColor.fromCmykF(cyan/99, magenta/99, yellow/99, key/99)
            self.cyan_slider.itemAt(1).widget().setText(str(cyan))
            self.magenta_slider.itemAt(1).widget().setText(str(magenta))
            self.yellow_slider.itemAt(1).widget().setText(str(yellow))
            self.key_slider.itemAt(1).widget().setText(str(key))

        self.DisconnectHSV()
        self.DisconnectRGB()

        self.UpdateHSV(col)
        self.UpdateRGB(col)
        col = col.toRgb()
        self.color_display.setStyleSheet(f"background-color: rgb({col.red()}, {col.green()}, {col.blue()});")

        self.ConnectHSV()
        self.ConnectRGB()

    def EditedHSV(self):
        if isinstance(self.sender(), QLineEdit):
            hueText = self.hue_slider.itemAt(1).widget().text()
            hue = int(hueText) if hueText != "" else 0
            saturationText = self.saturation_slider.itemAt(1).widget().text()
            saturation = int(saturationText) if saturationText != "" else 0
            valueText = self.value_slider.itemAt(1).widget().text()
            value = int(valueText) if valueText != "" else 0
            col = QColor.fromHsvF(hue / 359, saturation / 99, value / 99)

            self.hue_slider.itemAt(2).widget().setValue(hue)
            self.saturation_slider.itemAt(2).widget().setValue(saturation)
            self.value_slider.itemAt(2).widget().setValue(value)
        else:
            hue = self.hue_slider.itemAt(2).widget().value()
            saturation = self.saturation_slider.itemAt(2).widget().value()
            value = self.value_slider.itemAt(2).widget().value()
            col = QColor.fromHsvF(hue / 359, saturation / 99, value / 99)
            self.hue_slider.itemAt(1).widget().setText(str(hue))
            self.saturation_slider.itemAt(1).widget().setText(str(saturation))
            self.value_slider.itemAt(1).widget().setText(str(value))

        self.DisconnectSMYK()
        self.DisconnectRGB()

        self.UpdateCMYK(col)
        self.UpdateRGB(col)
        col = col.toRgb()
        self.color_display.setStyleSheet(f"background-color: rgb({col.red()}, {col.green()}, {col.blue()});")

        self.ConnectSMYK()
        self.ConnectRGB()

    def SelectColor(self):
        col = QColorDialog.getColor()

        self.DisconnectRGB()
        self.DisconnectSMYK()
        self.DisconnectHSV()

        self.color_display.setStyleSheet(f"background-color: rgb({col.red()}, {col.green()}, {col.blue()});")
        self.UpdateRGB(col)
        self.UpdateCMYK(col)
        self.UpdateHSV(col)

        self.ConnectRGB()
        self.ConnectSMYK()
        self.ConnectHSV()


    def UpdateCMYK(self, col):
        color = col.toCmyk()
        self.cyan_slider.itemAt(2).widget().setValue(round(color.cyanF() * 99))
        self.magenta_slider.itemAt(2).widget().setValue(round(color.magentaF() * 99))
        self.yellow_slider.itemAt(2).widget().setValue(round(color.yellowF() * 99))
        self.key_slider.itemAt(2).widget().setValue(round(color.blackF() * 99))

        self.cyan_slider.itemAt(1).widget().setText(str(round(color.cyanF() * 99)))
        self.magenta_slider.itemAt(1).widget().setText(str(round(color.magentaF() * 99)))
        self.yellow_slider.itemAt(1).widget().setText(str(round(color.yellowF() * 99)))
        self.key_slider.itemAt(1).widget().setText(str(round(color.blackF() * 99)))

    def UpdateHSV(self, col):
        color = col.toHsv()
        self.hue_slider.itemAt(2).widget().setValue(round(max(color.hueF() * 359, 0)))
        self.saturation_slider.itemAt(2).widget().setValue(round(color.saturationF() * 99))
        self.value_slider.itemAt(2).widget().setValue(round(color.valueF() * 99))

        self.hue_slider.itemAt(1).widget().setText(str(round(max(color.hueF() * 359, 0))))
        self.saturation_slider.itemAt(1).widget().setText(str(round(color.saturationF() * 99)))
        self.value_slider.itemAt(1).widget().setText(str(round(color.valueF() * 99)))

    def UpdateRGB(self, col):
        color = col.toRgb()
        self.red_slider.itemAt(2).widget().setValue(round(color.redF() * 255))
        self.green_slider.itemAt(2).widget().setValue(round(color.greenF() * 255))
        self.blue_slider.itemAt(2).widget().setValue(round(color.blueF() * 255))

        self.red_slider.itemAt(1).widget().setText(str(round(color.redF() * 255)))
        self.green_slider.itemAt(1).widget().setText(str(round(color.greenF() * 255)))
        self.blue_slider.itemAt(1).widget().setText(str(round(color.blueF() * 255)))

    def DisconnectSMYK(self):
        self.cyan_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedCMYK)
        self.cyan_slider.itemAt(1).widget().textChanged.disconnect(self.EditedCMYK)
        self.magenta_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedCMYK)
        self.magenta_slider.itemAt(1).widget().textChanged.disconnect(self.EditedCMYK)
        self.yellow_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedCMYK)
        self.yellow_slider.itemAt(1).widget().textChanged.disconnect(self.EditedCMYK)
        self.key_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedCMYK)
        self.key_slider.itemAt(1).widget().textChanged.disconnect(self.EditedCMYK)

    def ConnectSMYK(self):
        self.cyan_slider.itemAt(2).widget().valueChanged.connect(self.EditedCMYK)
        self.cyan_slider.itemAt(1).widget().textChanged.connect(self.EditedCMYK)
        self.magenta_slider.itemAt(2).widget().valueChanged.connect(self.EditedCMYK)
        self.magenta_slider.itemAt(1).widget().textChanged.connect(self.EditedCMYK)
        self.yellow_slider.itemAt(2).widget().valueChanged.connect(self.EditedCMYK)
        self.yellow_slider.itemAt(1).widget().textChanged.connect(self.EditedCMYK)
        self.key_slider.itemAt(2).widget().valueChanged.connect(self.EditedCMYK)
        self.key_slider.itemAt(1).widget().textChanged.connect(self.EditedCMYK)

    def DisconnectHSV(self):
        self.hue_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedHSV)
        self.hue_slider.itemAt(1).widget().textChanged.disconnect(self.EditedHSV)
        self.saturation_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedHSV)
        self.saturation_slider.itemAt(1).widget().textChanged.disconnect(self.EditedHSV)
        self.value_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedHSV)
        self.value_slider.itemAt(1).widget().textChanged.disconnect(self.EditedHSV)

    def ConnectHSV(self):
        self.hue_slider.itemAt(2).widget().valueChanged.connect(self.EditedHSV)
        self.hue_slider.itemAt(1).widget().textChanged.connect(self.EditedHSV)
        self.saturation_slider.itemAt(2).widget().valueChanged.connect(self.EditedHSV)
        self.saturation_slider.itemAt(1).widget().textChanged.connect(self.EditedHSV)
        self.value_slider.itemAt(2).widget().valueChanged.connect(self.EditedHSV)
        self.value_slider.itemAt(1).widget().textChanged.connect(self.EditedHSV)

    def DisconnectRGB(self):
        self.red_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedRGB)
        self.red_slider.itemAt(1).widget().textChanged.disconnect(self.EditedRGB)
        self.green_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedRGB)
        self.green_slider.itemAt(1).widget().textChanged.disconnect(self.EditedRGB)
        self.blue_slider.itemAt(2).widget().valueChanged.disconnect(self.EditedRGB)
        self.blue_slider.itemAt(1).widget().textChanged.disconnect(self.EditedRGB)

    def ConnectRGB(self):
        self.red_slider.itemAt(2).widget().valueChanged.connect(self.EditedRGB)
        self.red_slider.itemAt(1).widget().textChanged.connect(self.EditedRGB)
        self.green_slider.itemAt(2).widget().valueChanged.connect(self.EditedRGB)
        self.green_slider.itemAt(1).widget().textChanged.connect(self.EditedRGB)
        self.blue_slider.itemAt(2).widget().valueChanged.connect(self.EditedRGB)
        self.blue_slider.itemAt(1).widget().textChanged.connect(self.EditedRGB)
