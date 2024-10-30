# Лабораторная работа №2. Основы обработки цифровых изображений/сжатие изображений.

## Выполнил Белоус Артем

1. Постановка задачи:
    
    Написать приложение/веб-приложение, реализующее указанные в варианте методы
    обработки изображений
    Вариант 7: Реализация низкочастотных фильтров (сглаживающих), Глобальная пороговая обработка (2 метода на выбор, сравнить)
    
2. Листинг программы с комментариями:
    
    Рассмотрим функции, используемые в ходе выполнения программы.
    
    Класс MainWindow содержит в себе все графические объекты программы и реализует ее логику. Конструктор этого класса имеет вид:
    
    ```python
        def __init__(self):
            super().__init__()
            self.cur_image = None
            self.initial_image = None
            self.applied_filters_stack = []
    
            self.setMinimumSize(1000, 600)
    
            self.init_ui()
            self.init_shortcuts()
    
        def init_ui(self):
            self.layout = QVBoxLayout()
            #self.layout.setSpacing(int(self.height() * 0.03))
            self.layout.setSpacing(5)
    
            self.label = QLabel(self)
            self.label.setScaledContents(True)
            self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.layout.addWidget(self.label)
    
            self.btn_load = QPushButton('Load Image', self)
            self.btn_load.clicked.connect(self.load_image)
            self.layout.addWidget(self.btn_load)
    
            self.filters_layout = QHBoxLayout()
    
            self.threshold_layout = QVBoxLayout()
    
            self.threshold_label = QLabel("Global thresholding methods:")
            font = QFont()
            font.setBold(True)
            font.setItalic(True)
            font.setPointSize(10)
            self.threshold_label.setStyleSheet("QLabel { background-color : #8cd1d7; color : blue; }")
            self.threshold_label.setFont(font)
            self.threshold_label.setFixedSize(300,30)
    
            self.threshold_layout.addWidget(self.threshold_label)
    
            self.global_filters_layout = QHBoxLayout()
    
            self.btn_grayscale = QPushButton('Grayscale Filter', self)
            self.btn_grayscale.clicked.connect(self.apply_grayscale)
            self.global_filters_layout.addWidget(self.btn_grayscale)
    
            self.btn_OTSU = QPushButton('Otsu Filter', self)
            self.btn_OTSU.clicked.connect(self.apply_OTSU)
            self.global_filters_layout.addWidget(self.btn_OTSU)
    
            self.custom_threshold_layout = QVBoxLayout()
            self.custom_threshold_label = QLabel("Enter threshold value:")
            self.custom_threshold_label.setFixedSize(200, 15)
            self.input_field = QLineEdit(self)
            # rx = QtCore.QRegExp("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)?$")
            # val = QRegExpValidator(rx)
            validator = QIntValidator(bottom=0, top=255, parent=self)
            self.input_field.setValidator(validator)
            self.custom_threshold_btn = QPushButton("Apply custom", self)
            self.custom_threshold_btn.clicked.connect(self.apply_custom_threshold)
            self.custom_threshold_layout.addWidget(self.custom_threshold_label)
            self.custom_threshold_layout.addWidget(self.input_field)
            self.custom_threshold_layout.addWidget(self.custom_threshold_btn)
            self.global_filters_layout.addLayout(self.custom_threshold_layout)
    
            self.threshold_layout.addLayout(self.global_filters_layout)
            self.filters_layout.addLayout(self.threshold_layout)
    
            self.anti_aliased_layout = QVBoxLayout()
    
            self.anti_aliased_label = QLabel("Anti-aliased filters:")
            self.anti_aliased_label.setStyleSheet("QLabel { background-color : #8cd1d7; color : blue; }")
            self.anti_aliased_label.setFont(font)
            self.anti_aliased_label.setFixedSize(300, 30)
            self.anti_aliased_layout.addWidget(self.anti_aliased_label)
    
            self.kernel_label = QLabel("Enter kernel size:")
            self.kernel_label.setFixedSize(200, 15)
            self.kernel_input_field = QLineEdit(self)
            validator = QIntValidator(bottom=1, parent=self)
            self.kernel_input_field.setValidator(validator)
            self.anti_aliased_layout.addWidget(self.kernel_label)
            self.anti_aliased_layout.addWidget(self.kernel_input_field)
    
            self.anti_aliased_filters_layout = QHBoxLayout()
    
            self.btn_avg_blur = QPushButton('Averaging blur', self)
            self.btn_avg_blur.clicked.connect(self.apply_averaging_blur)
            self.anti_aliased_filters_layout.addWidget(self.btn_avg_blur)
    
            self.btn_gauss_blur = QPushButton('Gaussian blur', self)
            self.btn_gauss_blur.clicked.connect(self.apply_gaussian_blur)
            self.anti_aliased_filters_layout.addWidget(self.btn_gauss_blur)
    
            self.btn_median_blur = QPushButton('Median blur', self)
            self.btn_median_blur.clicked.connect(self.apply_median_blur)
            self.anti_aliased_filters_layout.addWidget(self.btn_median_blur)
    
            self.anti_aliased_layout.addLayout(self.anti_aliased_filters_layout)
            self.filters_layout.addLayout(self.anti_aliased_layout)
    
            self.layout.addLayout(self.filters_layout)
    
            self.features_layout = QHBoxLayout()
    
            self.btn_clear = QPushButton('Clear Filters', self)
            self.btn_clear.clicked.connect(self.clear_all_filters)
            self.features_layout.addWidget(self.btn_clear)
    
            self.btn_undo = QPushButton('Undo Last Filter', self)
            self.btn_undo.clicked.connect(self.undo_filter)
            self.features_layout.addWidget(self.btn_undo)
    
            self.layout.addLayout(self.features_layout)
    
            self.btn_save = QPushButton('Save Image', self)
            self.btn_save.clicked.connect(self.save_image)
            self.layout.addWidget(self.btn_save)
    
            self.setLayout(self.layout)
    
            self.setWindowTitle('Image Filter App')
            self.show()
    ```
    
    Функция init_shortcuts задает сочетания клавиш ctrl+S, ctrl + Z для удобного пользования программой :
    
    ```python
        def init_shortcuts(self):
            save_shortcut = QKeySequence(Qt.CTRL + Qt.Key_S)
            self.save_shortcut = QShortcut(save_shortcut, self)
            self.save_shortcut.activated.connect(self.save_image)
    
            undo_shortcut = QKeySequence(Qt.CTRL + Qt.Key_Z)
            self.undo_shortcut = QShortcut(undo_shortcut, self)
            self.undo_shortcut.activated.connect(self.undo_filter)
    ```
    
    Функция load_image предназначена для загрузи изображения:
    
    ```python
        def load_image(self):
            fname, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image files (*.jpg *.png)')
            if fname:
                self.applied_filters_stack.clear()
                self.cur_image = cv2.imread(fname)
                if np.all(self.cur_image[:, :, 0] == self.cur_image[:, :, 1]) and np.all(self.cur_image[:, :, 1] == self.cur_image[:, :, 2]):
                    self.cur_image = cv2.cvtColor(self.cur_image, cv2.COLOR_BGR2GRAY)
                self.initial_image = self.cur_image
                self.display_image(self.cur_image)
    ```
    
    Функция display_image отвечает за прорисовку изображения на экране пользователя:
    
    ```python
        def display_image(self, image):
            shape = image.shape
            if len(shape) < 3:
                q_img = QImage(image.data, shape[1], shape[0], QImage.Format_Grayscale8)
            else:
                height, width, channel = shape
                bytes_per_line = 3 * width
                q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.pixmap = QPixmap.fromImage(q_img)
            # self.pixmap = QPixmap.convertFromImage(q_img, Qt.MonoOnly)
            self.label.setPixmap(self.pixmap.scaled(self.label.size(), Qt.KeepAspectRatio))
    ```
    
    Функция apply_grayscale отвечает применения фильтра, благодаря которому изображение состоит из оттенков серого:
    
    ```python
        def apply_grayscale(self):
            if self.cur_image is not None and not self.is_grayscaled(self.cur_image):
                self.applied_filters_stack.append(self.cur_image)
                gray_image = cv2.cvtColor(self.cur_image, cv2.COLOR_BGR2GRAY)
                self.cur_image = gray_image
                self.display_image(self.cur_image)
    ```
    
    Функция apply_gaussian_blur отвечает за применения сглаживающего фильтра Гаусса:
    
    ```python
        def apply_gaussian_blur(self):
            if self.cur_image is not None:
                ker_size = self.get_kernel_size()
                if ker_size % 2 == 0:
                    self.show_median_blur_warning_pop_up()
                    return
                if ker_size > min(self.cur_image.shape[0], self.cur_image.shape[1]):
                    self.show_to_large_kernel_size_warning_pop_up()
                    return
                self.applied_filters_stack.append(self.cur_image)
                blurred_image = cv2.GaussianBlur(self.cur_image, (ker_size, ker_size), 0)
                self.cur_image = blurred_image
                self.display_image(blurred_image)
    ```
    
    Функция apply_averaging_blur отвечает за применения стандартного сглаживающего фильтра, считающегося как среднее значение соседних пикселей:
    
    ```python
        def apply_averaging_blur(self):
            if self.cur_image is not None:
                ker_size = self.get_kernel_size()
                if ker_size > min(self.cur_image.shape[0], self.cur_image.shape[1]):
                    self.show_to_large_kernel_size_warning_pop_up()
                    return
                try:
                    self.applied_filters_stack.append(self.cur_image)
                    blurred_image = cv2.blur(self.cur_image, (ker_size, ker_size), 0)
                    self.cur_image = blurred_image
                    self.display_image(blurred_image)
                except:
                    self.show_to_large_kernel_size_warning_pop_up()
    ```
    
    Функция apply_median_blur отвечает за применения стандартного сглаживающего фильтра, считающегося как медиана из значений соседней пикселей:
    
    ```python
        def apply_median_blur(self):
            if self.cur_image is not None:
                ker_size = self.get_kernel_size()
                if ker_size % 2 == 0:
                    self.show_median_blur_warning_pop_up()
                    return
                if ker_size > min(self.cur_image.shape[0], self.cur_image.shape[1]):
                    self.show_to_large_kernel_size_warning_pop_up()
                    return
                try:
                    self.applied_filters_stack.append(self.cur_image)
                    blurred_image = cv2.medianBlur(self.cur_image, ker_size, 0)
                    self.cur_image = blurred_image
                    self.display_image(blurred_image)
                except:
                    self.show_to_large_kernel_size_warning_pop_up()
    ```
    
    Функция apply_OTSU отвечает за применения фильтра Отсу глобальной пороговой обработки:
    
    ```python
        def apply_OTSU(self):
            if self.cur_image is None:
                return
            if not self.is_grayscaled(self.cur_image):
                self.show_not_grayscaled_image_warning_pop_up()
                return
            try:
                self.applied_filters_stack.append(self.cur_image)
                ret,thr = cv2.threshold(self.cur_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                self.cur_image = thr
                self.display_image(thr)
            except:
                self.show_to_large_kernel_size_warning_pop_up()
    ```
    
    Функция apply_custom_threshold отвечает за применения фильтра  глобальной пороговой обработки для значения, вводимого самим пользователем:
    
    ```python
        def apply_custom_threshold(self):
            if self.cur_image is None:
                return
            if not self.is_grayscaled(self.cur_image):
                self.show_not_grayscaled_image_warning_pop_up()
                return
            self.applied_filters_stack.append(self.cur_image)
            threshold = int(self.input_field.text()) if self.input_field.text() != '' else 1
            ret, thr = cv2.threshold(self.cur_image, threshold, 255, cv2.THRESH_BINARY)
            self.cur_image = thr
            self.display_image(thr)
    ```
    
    Функция save_image отвечает за сохранения полученного результата:
    
    ```python
        def save_image(self):
            if self.cur_image is not None:
                fname, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Image files (*.png *.jpg *.jpeg *.bmp)')
                if fname:
                    cv2.imwrite(fname, self.cur_image)
    ```
    
    Функция resizeEvent отвечает за обработку события изменения размеров окна приложения:
    
    ```python
        def resizeEvent(self, event):
            self.layout.setSpacing(int(self.height() * 0.03))
            if self.cur_image is not None:
                self.display_image(self.cur_image)
    ```
    
    Функции clear_all_filters и undo_filter отвечают за полное обнуление фильтров и за снятие действия последнего примененного фильтра соответственно:
    
    ```python
        def clear_all_filters(self):
            if self.cur_image is not None:
                self.applied_filters_stack.clear()
                self.cur_image = self.initial_image
                self.display_image(self.initial_image)
    
        def undo_filter(self):
            if len(self.applied_filters_stack) > 0:
                last_filter = self.applied_filters_stack[-1]
                self.applied_filters_stack = self.applied_filters_stack[:-1]
                self.cur_image = last_filter
                self.display_image(self.cur_image)
    ```
    
    Функция is_grayscaled проверят, является ли изображение оттенками серого:
    
    ```python
        def is_grayscaled(self, img):
            if len(img.shape) < 3:
                return True
            return False
    ```
    
    Функция get_kernel_size получает пользовательское значение размеров ядра:
    
    ```python
        def get_kernel_size(self):
            text = self.kernel_input_field.text()
            return int(text) if text != '' else 1
    ```
    
    Далее представлены функции, генерирующие сообщения для пользователя:
    
    ```python
        def show_median_blur_warning_pop_up(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("The median blurring filter can not be applied(")
            msg_box.setInformativeText("To fix this, set the value of the kernel size to odd number, greater than 1")
            msg_box.exec()
            return
    
        def show_gaussian_blur_warning_pop_up(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("The gaussian blurring filter can not be applied(")
            msg_box.setInformativeText("To fix this, set the value of the kernel size to positive odd number")
            msg_box.exec()
            return
    
        def show_not_grayscaled_image_warning_pop_up(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Thresholding filter can not be applied(")
            msg_box.setInformativeText("To fix this, you should apply gray scaling filter in the first place")
            msg_box.exec()
            return
    
        def show_to_large_kernel_size_warning_pop_up(self):
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Blurring filter can not be applied(")
            msg_box.setInformativeText("You have entered too large kernel size")
            msg_box.exec()
            return
    ```
    
    Наконец, функция main является точкой входа программы и создает оконное приложение
    
    ```python
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    
    ```
    
3. Выходные данные.
    
    Выходными данными является программа для преобразования изображений:
    
    ![image](https://github.com/user-attachments/assets/8583adb7-0817-47a2-8141-04b32157d751)

    
4. Вывод
    
    В ходе выполнения лабораторной работы я рассмотрел работу трех сглаживающих фильтров (средний, медианный и Гаусса), а также два способа пороговой обработки (методом Отсу и через явное указание порога ).
