# Лабораторная работа №1. Цветовые модели.

## Выполнил Белоус Артем

1. Постановка задачи:
    
    Изучить цветовые модели: RGB, CMYK, HSV, преобразования между ними.
    Создать приложение/веб-приложение, позволяющее пользователю выбирать, а затем интерактивно менять цвет, показывая при этом его составляющие в трех моделях одновременно.
    
2. Входные данные:
    
    Цветовые модели RGB, CMYK, HSV.
    
3. Листинг программы с комментариями:
    
    Рассмотрим функции, используемые в ходе выполнения программы.
    
    Класс MainWindow содержит в себе все графические объекты программы и реализует ее логику. Конструктор этого класса имеет вид:
    
    ```python
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
    ```
    
    Функция CreateSliderLayout создает слайдер и текстовое поле для изменения цвета с заданным именем, а также соединяет сигналы от текстового поля и слайдера с соответствующими слотами:
    
    ```python
            def CreateSliderLayout(self, color_name, upper_bound):
            slider = QSlider(Qt.Horizontal)
            slider.setRange(0, upper_bound)
            slider.setValue(0)
            line_edit = QLineEdit("0")
            line_edit.setMaximumSize(50, 20)
    
            if color_name == Colors.RED or color_name == Colors.GREEN or color_name == Colors.BLUE:
                slider.valueChanged.connect(self.EditedRGB)
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
    ```
    
    Функция CreateOutputFieldAndSelectButton создает кнопку для вызова диалогового окна выбора цвета, а также поле, в котором будет отображаться текущий цвет:
    
    ```python
            def CreateOutputFieldAndSelectButton(self):
            self.output_layout = QHBoxLayout()
            self.color_display.setMinimumSize(200, 100)
            self.EditedRGB()
    
            change_color_button = QPushButton("Select color")
            change_color_button.setMinimumSize(100, 50)
            change_color_button.setMaximumSize(200,200)
            change_color_button.clicked.connect(self.SelectColor)
    
            self.output_layout.addWidget(self.color_display)
            self.output_layout.addWidget(change_color_button)
    ```
    
    Функция EditedRGB отвечает за изменение статуса всех слайдеров и текстовых полей, вызывается при изменении одного из слайдеров или текстовых полей RGB палитры в результате действия пользователя. Аналогично реализованы функции EditedCMYK и EditedHSV:
    
    ```python
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
    
                self.cyan_slider.itemAt(2).widget().setValue(cyan)
                self.magenta_slider.itemAt(2).widget().setValue(magenta)
                self.yellow_slider.itemAt(2).widget().setValue(yellow)
                self.key_slider.itemAt(2).widget().setValue(key)
            else:
                cyan = self.cyan_slider.itemAt(2).widget().value()
                magenta = self.magenta_slider.itemAt(2).widget().value()
                yellow = self.yellow_slider.itemAt(2).widget().value()
                key = self.key_slider.itemAt(2).widget().value()
                self.cyan_slider.itemAt(1).widget().setText(str(cyan))
                self.magenta_slider.itemAt(1).widget().setText(str(magenta))
                self.yellow_slider.itemAt(1).widget().setText(str(yellow))
                self.key_slider.itemAt(1).widget().setText(str(key))
    
            self.DisconnectHSV()
            self.DisconnectRGB()
    
            r, g, b = self.CMYKtoRGB(cyan, magenta, yellow, key)
            col = QColor(r, g, b)
            self.UpdateHSV(col)
            self.UpdateRGB(col)
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
    
                self.hue_slider.itemAt(2).widget().setValue(hue)
                self.saturation_slider.itemAt(2).widget().setValue(saturation)
                self.value_slider.itemAt(2).widget().setValue(value)
            else:
                hue = self.hue_slider.itemAt(2).widget().value()
                saturation = self.saturation_slider.itemAt(2).widget().value()
                value = self.value_slider.itemAt(2).widget().value()
                self.hue_slider.itemAt(1).widget().setText(str(hue))
                self.saturation_slider.itemAt(1).widget().setText(str(saturation))
                self.value_slider.itemAt(1).widget().setText(str(value))
    
            self.DisconnectSMYK()
            self.DisconnectRGB()
    
            r, g, b = self.HSVtoRGB(hue, saturation, value)
            col = QColor(r, g, b)
            self.UpdateCMYK(col)
            self.UpdateRGB(col)
            self.color_display.setStyleSheet(f"background-color: rgb({col.red()}, {col.green()}, {col.blue()});")
    
            self.ConnectSMYK()
            self.ConnectRGB()
    ```
    
    Функция UpdateRGB отвечает за изменение всех текстовых полей и слайдеров, связанных с палитрой RGB, согласно новому цвету, предаваемому в функцию в качестве параметра. Аналогично реализованы функции UpdateCMYK и UpdateHSV:
    
    ```python
        def UpdateCMYK(self, col):
            c, m, y, k = self.RGBtoCMYK(col)
            self.cyan_slider.itemAt(2).widget().setValue(c)
            self.magenta_slider.itemAt(2).widget().setValue(m)
            self.yellow_slider.itemAt(2).widget().setValue(y)
            self.key_slider.itemAt(2).widget().setValue(k)
    
            self.cyan_slider.itemAt(1).widget().setText(str(c))
            self.magenta_slider.itemAt(1).widget().setText(str(m))
            self.yellow_slider.itemAt(1).widget().setText(str(y))
            self.key_slider.itemAt(1).widget().setText(str(k))
    
        def UpdateHSV(self, col):
            h, s, v = self.RGBtoHSV(col)
            self.hue_slider.itemAt(2).widget().setValue(h)
            self.saturation_slider.itemAt(2).widget().setValue(s)
            self.value_slider.itemAt(2).widget().setValue(v)
    
            self.hue_slider.itemAt(1).widget().setText(str(h))
            self.saturation_slider.itemAt(1).widget().setText(str(s))
            self.value_slider.itemAt(1).widget().setText(str(v))
    
        def UpdateRGB(self, col):
            r, g,b = col.red(), col.green(), col.blue()
            self.red_slider.itemAt(2).widget().setValue(r)
            self.green_slider.itemAt(2).widget().setValue(g)
            self.blue_slider.itemAt(2).widget().setValue(b)
    
            self.red_slider.itemAt(1).widget().setText(str(r))
            self.green_slider.itemAt(1).widget().setText(str(g))
            self.blue_slider.itemAt(1).widget().setText(str(b))
    ```
    
    Функция SelectColor отвечает за выбор цвета с помощью диалогового окна при нажатии на кнопку выбора цвета:
    
    ```python
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
    ```
    
    Функция DisconnectRGB предназначена для временного разъединения слотов и сигналов, связанных с палитрой RGB. Функция ConnectRGB, в свою очередь, предназначена для обратного присоединения слотов и сигналов. Эти функции вызываются с целью избегания зацикливания вызова функций EditedRGB. Аналогично реализованы функции DisconnectCMYK, ConnectCMYK, DisconnectHSV, ConnectHSV:
    
    ```python
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
    
    ```
    
    Для перевода цветов из одной палитры в другую использовались следующие функции:
    
    ```python
        def CMYKtoRGB(self, c, m, y, k):
            r = 255 * (1 - c / 99) * (1 - k / 99)
            g = 255 * (1 - m / 99) * (1 - k / 99)
            b = 255 * (1 - y / 99) * (1 - k / 99)
            return round(r), round(g), round(b)
    
        def HSVtoRGB(self, h, s, v):
            print(h, s, v)
            V = v / 99
            S = s / 99
            C = V * S
            X = C * (1 - abs((h / 60) % 2 - 1))
            m = V - C
            r,g,b = 0,0,0
            if h < 60:
                r,g,b = C,X,0
            elif h < 120:
                r,g,b = X, C, 0
            elif h < 180:
                r, g,b = 0,C,X
            elif h < 240:
                r,g,b = 0,X,C
            elif h < 300:
                r,g,b = X,0,C
            elif h < 360:
                r,g,b = C,0,X
            r,g,b = (r + m) * 255, (g + m) * 255, (b +m) * 255
            print(r, g, b)
            return round(r), round(g), round(b)
    
        def RGBtoCMYK(self, col):
            r = col.red() / 255
            g = col.green() / 255
            b = col.blue() / 255
            if r == 0 and b == 0 and b == 0:
                return 0,0,0,100
    
            k = 1 - max(r, g, b)
            c = round((1 - r - k) / (1 - k) * 99)
            m = round((1 - g - k) / (1 - k) * 99)
            y = round((1 - b - k) / (1 - k) * 99)
            return c, m, y, round(k * 99)
    
        def RGBtoHSV(self, col):
            r = col.red() / 255
            g = col.green() / 255
            b = col.blue() / 255
            cMax = max(r, g, b)
            cMin = min(r, g, b)
            delta = cMax - cMin
    
            if delta == 0:
                h = 0
            elif (cMax - r) < 0.0001:
                h = 60 * (((g - b) / delta) % 6)
            elif (cMax - g) < 0.0001:
                h = 60 * (((b - r) / delta) + 2)
            else:
                h = 60 * (((r - g) / delta) + 4)
    
            if cMax == 0:
                s = 0
            else:
                s = delta / cMax
    
            v = cMax
            return round(h), round(s * 99), round(v * 99)
    
    ```
    
    Класс Colors представляет собой перечислений всех использующихся цветов для создания моделей:
    
    ```python
    class Colors(Enum):
        RED = 'Red'
        GREEN = 'Green'
        BLUE = 'Blue'
        CYAN = 'Cyan'
        MAGENTA = 'Magenta'
        Yellow = 'Yellow'
        KEY = 'Key'
        HUE = 'Hue'
        SATURATION = 'Saturation'
        VALUE = 'Value'
    ```
    
    Наконец, функция main является точкой входа программы и создает оконное приложение
    
    ```python
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    
    ```
    
4. Выходные данные.
    
    Выходными данными является программа для преобразования цвета с помощью различных цветовых моделей:
    
    ![image.png](image.png)
    
5. Вывод
    
    В ходе выполнения лабораторной работы я изучил цветовые модели RGB, CMYK и HSV путем написания программы с удобным графическим интерфейсом для преобразования цветов в данных моделях.