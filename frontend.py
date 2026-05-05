import sys, re
from decimal import Decimal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QFrame, QStackedWidget, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QLineEdit,QGridLayout, QRadioButton,  QCheckBox,QStyledItemDelegate, QStyleOptionViewItem
)
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtGui import QFont
import ml,database

class ClassificationLoginWindow(QWidget):
    """
    Первый экран: «Система, основанная на знаниях»
    Визуал полностью соответствует вашему скриншоту.
    """

    def __init__(self,stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Классификация химических элементов")
        self.setMinimumSize(720, 520)          # размер как на скриншоте
        self.setStyleSheet("background-color: white;")

        # Основной layout — всё выравнивается по центру
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(60, 60, 60, 80)
        self.main_layout.setSpacing(40)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setup_ui()

    def setup_ui(self):
        """Весь визуал здесь. Никогда не трогаем этот метод при изменении логики."""

        # ====================== ЗАГОЛОВОК ======================
        title1 = QLabel("Система, основанная на знаниях")
        title1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title1.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        title1.setStyleSheet("color: #1f2937;")

        title2 = QLabel("«Классификация химических элементов»")
        title2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title2.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        title2.setStyleSheet("color: #1f2937;")

        self.main_layout.addWidget(title1)
        self.main_layout.addWidget(title2)

        # Отступ перед кнопками
        self.main_layout.addStretch(1)

        # ====================== КНОПКА «Эксперт» ======================
        self.btn_expert = QPushButton("Войти как эксперт")
        self.btn_expert.setFixedSize(420, 68)
        self.btn_expert.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.btn_expert.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_expert.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)

        self.main_layout.addWidget(self.btn_expert, alignment=Qt.AlignmentFlag.AlignCenter)

        # ====================== КНОПКА «Специалист» ======================
        self.btn_specialist = QPushButton("Войти как специалист")
        self.btn_specialist.setFixedSize(420, 58)
        self.btn_specialist.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.btn_specialist.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_specialist.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)

        self.main_layout.addWidget(self.btn_specialist, alignment=Qt.AlignmentFlag.AlignCenter)

        # Нижний отступ
        self.main_layout.addStretch(2)

        # ====================== ПРИМЕР ПОДКЛЮЧЕНИЯ СИГНАЛОВ ======================
        # Здесь вы потом будете подключать свою логику.
        # Сейчас просто выводим в консоль — чтобы сразу проверить.
        self.btn_expert.clicked.connect(self._on_expert_clicked)
        self.btn_specialist.clicked.connect(self._on_specialist_clicked)

    # ====================== МЕСТО ДЛЯ ВАШЕЙ ЛОГИКИ ======================
    def _on_expert_clicked(self):
        self.stack.setCurrentIndex(4)
        # Здесь будет ваш код (открытие следующего окна и т.д.)

    def _on_specialist_clicked(self):
        self.open_database()
    def open_database(self):
        self.stack.setCurrentIndex(1)


class DataBaseWindow(QWidget):
    """
    окно специалиста со списком слева
    """

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setWindowTitle("База данных")
        self.setMinimumSize(720, 520)
        self.setStyleSheet("background-color: white;")

        # ОСНОВНОЙ LAYOUT
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(30)

        # ЛЕВАЯ ПАНЕЛЬ
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title1 = QLabel("Элементы")
        title1.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        title1.setStyleSheet("color: #1f2937;")
        title1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)      
        self.scroll_area.setFixedWidth(240)
        self.scroll_area.setMinimumHeight(320)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
            }
        """)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setContentsMargins(8, 12, 8, 12)

        self.active_button = None

        rows, columns = database.fetch_table("chem_element")
        for row in rows:
            item = QPushButton(str(row[1]))
            item.setProperty("id", int(row[0]))
            item.setFont(QFont("Helvetica", 15))
            item.setFixedHeight(36)
            item.setCursor(Qt.CursorShape.PointingHandCursor)

            item.clicked.connect(self.on_item_clicked)

            item.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    text-align: left;
                    padding-left: 12px;
                    border-bottom: 1px solid rgba(148, 163, 184, 0.4);
                }
                QPushButton:hover {
                    background-color: #f8fafc;
                    border-radius: 4px;
                }
                QPushButton:pressed {
                    background-color: #e2e8f0;
                }
            """)
            self.scroll_layout.addWidget(item)

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)

        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedHeight(50)
        self.btn_back.setFont(QFont("Helvetica", 15))

        
        btn_style = """
            QPushButton {
                background-color: #f1f5f9;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """

        self.btn_back.setStyleSheet(btn_style)
        

        buttons_layout.addWidget(self.btn_back)    
                        
        #buttons_layout.addWidget(self.btn_class)    

        # ПРАВАЯ ЧАСТЬ
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(20)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.active_title = QLabel()
        self.active_title.setFont(QFont("Helvetica", 22, QFont.Weight.Medium))
        self.active_title.setStyleSheet("color: #3b82f6;")
        self.active_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.active_title.hide()

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Свойство", "Тип данных", "Значение"])

        self.table.setFont(QFont("Helvetica", 14))
        header_font = QFont("Helvetica", 15, QFont.Weight.Medium)

        header = self.table.horizontalHeader()
        header.setFont(header_font)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
                gridline-color: #f1f5f9;
                outline: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)

        right_layout.addWidget(self.active_title)
        self.btn_class = QPushButton("Перейти к классификации")
        self.btn_class.setFixedHeight(50)
        self.btn_class.setFont(QFont("Helvetica", 15))
        self.btn_class.setStyleSheet(btn_style)
        right_layout.addWidget(self.table)
        right_layout.addWidget(self.btn_class)

        # СБОРКА ОСНОВНОГО LAYOUT
        left_layout.addWidget(title1)
        left_layout.addWidget(self.scroll_area)
        left_layout.addStretch()           
        left_layout.addLayout(buttons_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        main_layout.setStretchFactor(left_widget, 1)
        main_layout.setStretchFactor(right_widget, 3)

        self.btn_back.clicked.connect(self.go_back)
        self.btn_class.clicked.connect(self.go_class)

    def update_scroll(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.active_button = None

        rows,columns =  database.fetch_table("chem_element")
        for row in rows:
            item = QPushButton(str(row[1]))
            item.setProperty("id", int(row[0]))
            item.setFont(QFont("Helvetica", 13))
            item.setFixedHeight(20)
            item.setFixedWidth(100)
            item.setCursor(Qt.CursorShape.PointingHandCursor)

            item.clicked.connect(self.on_item_clicked)

            item.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    text-align: left;
                    padding-left: 10px;
                    border-bottom: 2px solid rgba(148, 163, 184, 0.5); /* серая полоска */
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                }
                """)

            self.scroll_layout.addWidget(item)

    def update_table_data(self):
        element_id = self.active_button.property("id")
        print("ID:", element_id)

        data = database.get_properties_value(element_id)
        print("DATA:", data)

        # очистка таблицы
        self.table.setRowCount(0)

        # заполнение новой
        self.table.setRowCount(len(data))

        for row, (key, value) in enumerate(data.items()):

            # тип
            if str(value).replace('.', '', 1).isdigit():
                value_type = "Вещественный"
            else:
                value_type = "Качественный"

            item0 = QTableWidgetItem(key)
            item0.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            item1 = QTableWidgetItem(value_type)
            item1.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            item2 = QTableWidgetItem(str(value))
            item2.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(row, 0, item0)
            self.table.setItem(row, 1, item1)
            self.table.setItem(row, 2, item2)

    def set_active_button(self, button):
            # сброс старой активной кнопки
            self.active_title.setText(button.text())
            self.active_title.show()
            self.table.show()
            
            if self.active_button:
                self.active_button.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background: transparent;
                        text-align: left;
                        padding-left: 10px;
                        border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                    }
                    QPushButton:hover {
                        background-color: #f1f5f9;
                    }
                """)

            # устанавливаем новую
            button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: #eef2ff;
                    text-align: left;
                    padding-left: 10px;

                    border-bottom: 2px solid #3b82f6; /* синяя полоска */
                }
            """)

            self.active_button = button
            self.update_table_data()

    def on_item_clicked(self):
       
        button = self.sender()
        self.set_active_button(button)
        print("active_button =", self.active_button)
        print("type =", type(self.active_button))
        print(self.active_button.property("id"))

    def go_back(self):
        self.stack.setCurrentIndex(0)

    def go_class(self):
        self.stack.setCurrentIndex(2)
    

    
class FullWidthDelegate(QStyledItemDelegate):
    """Делегат для QLineEdit чтобы занимать всю ширину ячейки"""
    
    def createEditor(self, parent, option: QStyleOptionViewItem, index):
        editor = super().createEditor(parent, option, index)
        if editor:
            
            editor.setContentsMargins(0, 0, 0, 0)
           
            editor.setFixedHeight(option.rect.height() - 2)
        return editor

    def updateEditorGeometry(self, editor, option: QStyleOptionViewItem, index):
        rect = option.rect
        rect.setLeft(rect.left() + 4)      
        rect.setRight(rect.right() - 4)    
        rect.setTop(rect.top() + 2)
        rect.setBottom(rect.bottom() - 2)
        editor.setGeometry(rect)

class ClassWindow(QWidget):

    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setWindowTitle("Классификация")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 40)
        main_layout.setSpacing(30)

        # ТАБЛИЦА
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Свойство", "Тип данных", "Значение"])
        self.table.setItemDelegateForColumn(2, FullWidthDelegate(self.table))
        data = database.get_properties()

        for key in list(data.keys()):
            if data[key] == "Не определён":
                del data[key]

        self.table.setRowCount(len(data))

        for row, (name, typ) in enumerate(data.items()):

            itemclass0 = QTableWidgetItem(name)
            itemclass0.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            itemclass1 = QTableWidgetItem(typ)
            itemclass1.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(row, 0, itemclass0)
            self.table.setItem(row, 1, itemclass1)

            # третий столбец для ввода
            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 2, item)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.setFont(QFont("Helvetica", 16))
        header_font = QFont("Helvetica", 18, QFont.Weight.Medium)

        header = self.table.horizontalHeader()
        for i in range(self.table.columnCount()):
            if header_item := self.table.horizontalHeaderItem(i):
                header_item.setFont(header_font)

        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                background: white;
                gridline-color: #f1f5f9;
                outline: none;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

        main_layout.addWidget(self.table)

        # КНОПКИ
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        # КНОПКА Назад
        self.btn_left = QPushButton("Назад")
        self.btn_left.setFixedSize(220, 60)
        self.btn_left.setFont(QFont("Helvetica", 16))

        self.btn_left.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)

        # КНОПКА Классифицировать
        self.btn_right = QPushButton("Классифицировать")
        self.btn_right.setFixedSize(260, 60)
        self.btn_right.setFont(QFont("Helvetica", 16))

        self.btn_right.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 12px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)

        self.btn_left.clicked.connect(self.go_back)
        self.btn_right.clicked.connect(self.go_res)

        bottom_layout.addWidget(self.btn_left, alignment=Qt.AlignmentFlag.AlignLeft)
        bottom_layout.addStretch()                     # раздвигает кнопки
        bottom_layout.addWidget(self.btn_right, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(bottom_layout)

    def update_class_table(self):
        print("ОБНОВИЛОСЬ")
        
        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Свойство", "Тип данных", "Значение"])

        data = database.get_properties()

        for key in list(data.keys()):
            if data[key] == "Не определён":
                del data[key]

        self.table.setRowCount(len(data))

        for row, (name, typ) in enumerate(data.items()):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(typ))

            item = QTableWidgetItem("")
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 2, item)

        # Применяем те же стили после обновления
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setItemDelegateForColumn(2, FullWidthDelegate(self.table))
        self.table.setFont(QFont("Helvetica", 16))
        header_font = QFont("Helvetica", 18, QFont.Weight.Medium)

        for i in range(self.table.columnCount()):
            if header_item := self.table.horizontalHeaderItem(i):
                header_item.setFont(header_font)
    def get_user_answers(self):
        answers = {}

        for row in range(self.table.rowCount()):
            key_item = self.table.item(row, 0)
            type_item = self.table.item(row, 1)
            val_item = self.table.item(row, 2)

            key = key_item.text().strip() if key_item else ""
            value = val_item.text().strip() if val_item else ""
            value_type = type_item.text().strip() if type_item else ""

            if value_type == "Качественный":
                value = value.lower()

            answers[key] = value

        return answers

    def go_back(self):
            self.stack.setCurrentIndex(1)
    def go_res(self):
            valid, row, message = self.validate_table()
            if not valid:
                self.show_error(row, message)
                return
            answers = self.get_user_answers()
            self.stack.widget(3).set_data(answers)
            self.stack.setCurrentIndex(3)
    
    def is_number(self, value: str):
        try:
            float(value)
            return True
        except:
            return False

    def validate_table(self):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 2)
            type_item = self.table.item(row, 1)

            # ячейка пустая или None
            if item is None or item.text().strip() == "":
                return False, row, "Пустое значение"
            
            value = item.text().strip()
            value_type = type_item.text().strip()

            is_num = self.is_number(value)

            if value_type == "Вещественный" and not is_num:
                return False, row, "Ожидалось число"

            if value_type == "Качественный" and is_num:
                return False, row, "Ожидалась строка"
            

        return True, None, None
    
    def show_error(self, row=None, message="Ошибка"):
        if row is not None:
            full_text = f"Ошибка в строке {row + 1}: {message}"
        else:
            full_text = message
        msg = QMessageBox(self)
        msg.setWindowTitle("Ошибка")
        msg.setText(full_text)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()



class ResultWindow(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.data = {}
        self.stack = stack
        self.setWindowTitle("Классификация химического элемента")
        self.setMinimumSize(820, 620)
        self.setStyleSheet("background-color: white;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(60, 50, 60, 50)
        self.main_layout.setSpacing(30)

        self.setup_ui()

    def to_float_safe(self,x):
        try:
            return float(x)
        except ValueError:
            return x
    
    def update_info(self):
        if not self.data:
            return
        
        atomic_mass = self.data.get("Атомная масса")
        density = self.data.get("Плотность")
        atomic_radius = self.data.get("Радиус атома")
        element_type = self.data.get("Тип")

        result = database.find_chem_element(self.data)

        namemodel, conf, top3 = ml.predict_element(self.to_float_safe(atomic_mass),self.to_float_safe(atomic_radius),self.to_float_safe(density),self.to_float_safe(element_type) )
        print(self.to_float_safe(atomic_mass),int(atomic_radius),self.to_float_safe(density),self.to_float_safe(element_type))
        print(f"Предсказание: {namemodel} ({conf}%)")
        print(top3)
        if result:
            chem_id, name = result
            explain = database.explain_excluded_elements(chem_id)
            self.system_answer_box.setText(name)
            self.explanation_text.setText(explain)
            
        else:
            self.system_answer_box.setText("Не найдено")
            self.explanation_text.setText("""Химический элемент не определён. Знания об этом химическом элементе не занесены в систему или элемент не относится к известным химическим элементам. Обратитесь к эксперту для разрешения проблемы.""")
        if top3 != []:
            self.model_answer_box.setText(f"{namemodel} ({conf}%)")
    def set_data(self, data):
        self.data = data
        #print(self.data)
        self.update_info()


    def setup_ui(self):

        # Ответ системы
        system_layout = QHBoxLayout()
        system_layout.setSpacing(30)

        label_system = QLabel("Ответ системы")
        label_system.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        label_system.setStyleSheet("color: #1f2937;")
        system_layout.addWidget(label_system)

        print(*self.data.values())
        result = None #database.find_chem_element(*self.data.values())
        
        
        if result:
            chem_id, name = result
            explain = database.explain_excluded_elements(chem_id)

        self.system_answer_box = QLabel("Не найдено")
        self.system_answer_box.setFixedSize(320, 58)
        self.system_answer_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.system_answer_box.setFont(QFont("Helvetica", 20, QFont.Weight.Medium))
        self.system_answer_box.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px solid #64748b;
                border-radius: 8px;
                color: #1e2937;
            }
        """)
        system_layout.addWidget(self.system_answer_box)
        system_layout.addStretch(1)

        self.main_layout.addLayout(system_layout)

        # Ответ модели
        model_layout = QHBoxLayout()
        model_layout.setSpacing(30)

        label_model = QLabel("Ответ модели")
        label_model.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        label_model.setStyleSheet("color: #1f2937;")
        model_layout.addWidget(label_model)

        self.model_answer_box = QLabel("Не определено")
        self.model_answer_box.setFixedSize(320, 58)
        self.model_answer_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.model_answer_box.setFont(QFont("Helvetica", 20, QFont.Weight.Medium))
        self.model_answer_box.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px solid #64748b;
                border-radius: 8px;
                color: #1e2937;
            }
        """)
        model_layout.addWidget(self.model_answer_box)
        model_layout.addStretch(1)

        self.main_layout.addLayout(model_layout)

        # ОБЪЯСНЕНИЕ
        explanation_title = QLabel("Объяснение")
        explanation_title.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        explanation_title.setStyleSheet("color: #1f2937;")
        self.main_layout.addWidget(explanation_title)

        self.explanation_scroll = QScrollArea()
        self.explanation_scroll.setWidgetResizable(True)
        self.explanation_scroll.setMinimumHeight(220)
        self.explanation_scroll.setMaximumHeight(400)
        self.explanation_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.explanation_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.explanation_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #f8fafc;
                border: 2px solid #cbd5e1;
                border-radius: 12px;
            }
            QScrollArea > QWidget > QWidget {   /* внутренний виджет */
                background-color: #f8fafc;
            }
        """)

        inner_widget = QWidget()
        explanation_layout = QVBoxLayout(inner_widget)
        explanation_layout.setContentsMargins(25, 20, 25, 20)
        explanation_layout.setSpacing(0)

        self.explanation_text = QLabel("""
                                       Химический элемент не определён.
                                        Знания об этом химическом элементе не занесены в систему или
                                        элемент не относится к известным химическим элементам.
                                        Обратитесь к эксперту для разрешения проблемы.
                                        """)
        self.explanation_text.setFont(QFont("Helvetica", 16))
        self.explanation_text.setStyleSheet("color: #334155; line-height: 1.4;")
        self.explanation_text.setWordWrap(True)
        explanation_layout.addWidget(self.explanation_text)

        self.explanation_scroll.setWidget(inner_widget)

        self.main_layout.addWidget(self.explanation_scroll)

        self.main_layout.addStretch(1)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Кнопка Назад
        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedSize(240, 62)
        self.btn_back.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)

        # Кнопка К базе знаний
        self.btn_knowledge = QPushButton("К базе знаний")
        self.btn_knowledge.setFixedSize(320, 62)
        self.btn_knowledge.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.btn_knowledge.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_knowledge.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)

        buttons_layout.addWidget(self.btn_back)
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.btn_knowledge)

        self.main_layout.addLayout(buttons_layout)

        self.btn_back.clicked.connect(self._on_back_clicked)
        self.btn_knowledge.clicked.connect(self._on_knowledge_clicked)

    
    def _on_back_clicked(self):
        self.stack.setCurrentIndex(2)

    def _on_knowledge_clicked(self):
        self.stack.setCurrentIndex(1)


class SpecialWindow(QWidget):
    """
    Окно «Редактор базы знаний» (режим специалиста)
    Добавлена страница «Химические элементы» точно по скриншоту.
    """

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Редактор базы знаний")
        self.setMinimumSize(1020, 640)       # чуть шире для красивой сетки
        self.setStyleSheet("background-color: white;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.setup_ui()

    def setup_ui(self):
        """Весь визуал здесь. Никогда не трогаем этот метод при добавлении функционала."""

        # ОСНОВНОЙ HORIZONTAL LAYOUT
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # ЛЕВАЯ ПАНЕЛЬ
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(350)
        self.left_panel.setStyleSheet("background-color: white;")

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        menu_items = [
            "Химические элементы",
            "Свойства",
            "Возможные значения",
            "Описание свойств класса",
            "Значение для класса"
        ]

        self.active_button = None
        self.menu_buttons = []
        for text in menu_items:
            btn = QPushButton(text)
            btn.setFont(QFont("Helvetica", 18))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 16px 28px;
                    border: none;
                    border-bottom: 1px solid #e5e7eb;
                    background-color: white;
                    color: #1f2937;
                }
                QPushButton:hover {
                    background-color: #f8fafc;
                }
                QPushButton:pressed {
                    background-color: #f1f5f9;
                }
            """)
            left_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        # Разделитель
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #e5e7eb;")
        left_layout.addWidget(separator)

        # Кнопка «Проверка полноты знаний»
        self.btn_check = QPushButton("Проверка полноты знаний")
        self.btn_check.setFont(QFont("Helvetica", 18))
        self.btn_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_check.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 18px 28px;
                border: none;
                border-top: 1px solid #e5e7eb;
                background-color: white;
                color: #1f2937;
            }
            QPushButton:hover {
                background-color: #f8fafc;
            }
            QPushButton:pressed {
                background-color: #f1f5f9;
            }
        """)
        left_layout.addWidget(self.btn_check)

        left_layout.addStretch(1)

        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedSize(240, 62)
        self.btn_back.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
            QPushButton:pressed {
                background-color: #cbd5e1;
            }
        """)
        back_container = QHBoxLayout()
        back_container.setContentsMargins(40, 20, 40, 30)
        back_container.addWidget(self.btn_back)
        back_container.addStretch(1)
        left_layout.addLayout(back_container)

        content_layout.addWidget(self.left_panel)

        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFixedWidth(1)
        v_line.setStyleSheet("background-color: #e5e7eb;")
        content_layout.addWidget(v_line)

        # ПРАВАЯ ПАНЕЛЬ
        self.right_panel = QStackedWidget()
        self.right_panel.setStyleSheet("background-color: white;")

        empty_page = QWidget()
        empty_layout = QVBoxLayout(empty_page)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder = QLabel("Выберите раздел слева")
        placeholder.setFont(QFont("Helvetica", 20))
        placeholder.setStyleSheet("color: #64748b;")
        empty_layout.addWidget(placeholder)
        self.right_panel.addWidget(empty_page)   # index 0

        # ХИМИЧЕСКИЕ ЭЛЕМЕНТЫ
        self.chemical_page = QWidget()
        chemical_layout = QVBoxLayout(self.chemical_page)
        chemical_layout.setContentsMargins(40, 30, 40, 30)
        chemical_layout.setSpacing(25)

        # Прокручиваемая сетка
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        scroll_content = QWidget()
        self.chemical_grid_layout = QGridLayout(scroll_content)
        self.chemical_grid_layout.setSpacing(14)
        self.chemical_grid_layout.setContentsMargins(0, 0, 0, 0)

        

        drows,columns =  database.fetch_table("chem_element")
        

        rows = 0
        cols = 0
        for drow in drows:

            item = QLabel(f'<a href="chemical_delete" style="color:#ef4444; text-decoration: none;">✕</a> {str(drow[1])}')
            item.setTextFormat(Qt.TextFormat.RichText)
            item.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            item.setOpenExternalLinks(False)
            item.linkActivated.connect(self.on_link_clicked)

            item.setProperty("id", int(drow[0]))
            item.setProperty("name", drow[1])
            item.setFont(QFont("Helvetica", 18))
            item.setStyleSheet("padding: 2px 0; color: #1f2937;")
            self.chemical_grid_layout.addWidget(item, rows, cols)
            cols += 1
            if cols == 3:
                cols = 0
                rows += 1

        scroll.setWidget(scroll_content)
        chemical_layout.addWidget(scroll)

        # Нижняя панель с вводом и кнопкой
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        self.chemical_element_input = QLineEdit()
        self.chemical_element_input.setPlaceholderText("Введите название химического элемента")
        self.chemical_element_input.setFont(QFont("Helvetica", 15))
        self.chemical_element_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 8px;
                background: transparent;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #3b82f6;
            }
        """)
        bottom_layout.addWidget(self.chemical_element_input)

        self.chemical_btn_add = QPushButton("Добавить")
        self.chemical_btn_add.setFixedSize(160, 52)
        self.chemical_btn_add.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.chemical_btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.chemical_btn_add.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover { background-color: #e2e8f0; }
            QPushButton:pressed { background-color: #cbd5e1; }
        """)
        bottom_layout.addWidget(self.chemical_btn_add)

        chemical_layout.addLayout(bottom_layout)

        self.right_panel.addWidget(self.chemical_page)   # index 1

        


        # СТРАНИЦА СВОЙСТВА
        self.property_page = QWidget()
        property_layout = QVBoxLayout(self.property_page)
        property_layout.setContentsMargins(40, 30, 40, 30)
        property_layout.setSpacing(25)

        # Прокручиваемая сетка
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        scroll_content = QWidget()
        self.property_grid_layout = QGridLayout(scroll_content)
        self.property_grid_layout.setSpacing(0)
        self.property_grid_layout.setContentsMargins(0, 0, 0, 0)

        

        drows,columns =  database.fetch_table("property")
        

        rows = 0
        cols = 0
        for drow in drows:

            item = QLabel(f'<a href="property_delete" style="color:#ef4444; text-decoration: none;">✕</a> {str(drow[1])}')
            item.setTextFormat(Qt.TextFormat.RichText)
            item.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            item.setOpenExternalLinks(False)
            item.linkActivated.connect(self.on_link_clicked)

            item.setProperty("id", int(drow[0]))
            item.setProperty("name", drow[1])
            item.setFont(QFont("Helvetica", 18))
            item.setStyleSheet("padding: 0px 0; color: #1f2937;")
            self.property_grid_layout.addWidget(item, rows, cols)
            cols += 1
            if cols == 1:
                cols = 0
                rows += 1

        scroll.setWidget(scroll_content)
        property_layout.addWidget(scroll)

        # Нижняя панель с вводом и кнопкой
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)

        self.property_element_input = QLineEdit()
        self.property_element_input.setPlaceholderText("Введите название свойства")
        self.property_element_input.setFont(QFont("Helvetica", 15))
        self.property_element_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 8px;
                background: transparent;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #3b82f6;
            }
        """)
        bottom_layout.addWidget(self.property_element_input)

        self.property_btn_add = QPushButton("Добавить")
        self.property_btn_add.setFixedSize(160, 52)
        self.property_btn_add.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.property_btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        self.property_btn_add.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover { background-color: #e2e8f0; }
            QPushButton:pressed { background-color: #cbd5e1; }
        """)
        bottom_layout.addWidget(self.property_btn_add)

        property_layout.addLayout(bottom_layout)

        self.right_panel.addWidget(self.property_page)   # index 2

        

# self.possible_val_page (index 3)
        self.possible_val_page = QWidget()
        possible_layout = QVBoxLayout(self.possible_val_page)
        possible_layout.setContentsMargins(40, 30, 40, 30)
        possible_layout.setSpacing(25)

        # Верхние вкладки
        self.tabs_layout = QHBoxLayout()

        
        tabs,columns =  database.fetch_table("property")
        

        for text in tabs:
            tab = QPushButton(str(text[1]))
            tab.setProperty("id", int(text[0]))
            tab.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
            tab.setStyleSheet("""
                    QPushButton {
                        border: none; background: transparent; color: #64748b; padding-bottom: 6px;
                    }
                    QPushButton:hover {
                        background-color: #f1f5f9;
                    }
                """)
            tab.setCursor(Qt.CursorShape.PointingHandCursor)
            tab.clicked.connect(self.on_property_tab_clicked)
            self.tabs_layout.addWidget(tab)

        
        possible_layout.addLayout(self.tabs_layout)
        


        # Заголовок "Значения"
        values_title = QLabel("Значения")
        values_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        possible_layout.addWidget(values_title)

        # Радиокнопки
        radio_layout = QHBoxLayout()
        self.radio_substance = QRadioButton("Вещественные")
        self.radio_substance.setChecked(True)
        self.radio_substance.setFont(QFont("Helvetica", 18))
        self.radio_qualitative = QRadioButton("Качественные")
        self.radio_qualitative.setFont(QFont("Helvetica", 18))
        radio_layout.addWidget(self.radio_substance)
        radio_layout.addWidget(self.radio_qualitative)
        radio_layout.addStretch(1)
        possible_layout.addLayout(radio_layout)
        self.radio_substance.toggled.connect(self.on_radio_changed)
        self.radio_qualitative.toggled.connect(self.on_radio_changed)


        # Диапазоны

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: white; }")
        possibles_scroll_content = QWidget()
        self.possibles_property_grid_layout =  QGridLayout(possibles_scroll_content)
        self.possibles_property_grid_layout.setSpacing(0)
        self.possibles_property_grid_layout.setContentsMargins(0, 0, 0, 0)

        self.active_property_tab = None
        possibles, columns = database.fetch_table("possible_value")

        #print(possibles)
        rows = 0
        cols = 0
        for possible in possibles:
            if self.active_property_tab and self.active_property_tab.property("id") == possible[1]:

                value = str(possible[2])
                if self.radio_substance.isChecked():
                    # оставляем только числа/диапазоны (например: 10-20)
                    if not re.fullmatch(r"[0-9.\-]+", value):
                        continue 
                elif self.radio_qualitative.isChecked():
                    # оставляем только слова
                    if not re.fullmatch(r"[а-яА-Яa-zA-Z\s]+", value):
                        continue

                range_label = QLabel(f"<a href='property_possible_delete' style='color:#ef4444; text-decoration: none;'>✕</a>[{value.replace('-', ';')}]")
                range_label.setTextFormat(Qt.TextFormat.RichText)
                range_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                range_label.setOpenExternalLinks(False)
                range_label.linkActivated.connect(self.on_link_clicked)
                
                range_label.setProperty("id", int(possible[0]))
                range_label.setProperty("name", possible[2])
                range_label.setFont(QFont("Helvetica", 20))
                range_label.setStyleSheet("padding: 0px 0; color: #1f2937;")
                self.possibles_property_grid_layout.addWidget(range_label, rows, cols,alignment=Qt.AlignmentFlag.AlignTop)
                cols += 1
                if cols == 1:
                    cols = 0
                    rows += 1

        scroll.setWidget(possibles_scroll_content)
        possible_layout.addWidget(scroll)

        
        buttons = [self.tabs_layout.itemAt(i).widget() 
           for i in range(self.tabs_layout.count())]
        if len(buttons) >= 3:
            self.set_active_property_tab_button(buttons[2])

        # Чекбокс
        self.checkbox_integer = QCheckBox("Только целые числа")
        self.checkbox_integer.setFont(QFont("Helvetica", 18))
        self.checkbox_integer.setStyleSheet("""
                                            QCheckBox::indicator {
                                            width: 44px;
                                            height: 44px;
                                        }""")
        #possible_layout.addStretch(1)
        possible_layout.addWidget(self.checkbox_integer)
        self.checkbox_integer.stateChanged.connect(self.on_checkbox_integer_toggle)

        # Поля От / До
        self.from_to_layout = QHBoxLayout()
        self.from_to_layout.setSpacing(20)

        from_label = QLabel("От")
        from_label.setFont(QFont("Helvetica", 18))
        self.from_input = QLineEdit()
        self.from_input.setPlaceholderText("0.00")
        self.from_input.setFixedWidth(140)
        self.from_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #e5e7eb;
                font-size: 18px;
                padding-bottom: 6px;
                background: transparent;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #3b82f6;
            }
        """)

        to_label = QLabel("До")
        to_label.setFont(QFont("Helvetica", 18))
        self.to_input = QLineEdit()
        self.to_input.setPlaceholderText("20.00")
        self.to_input.setFixedWidth(140)
        self.to_input.setStyleSheet(self.from_input.styleSheet())

        self.from_to_layout.addWidget(from_label)
        self.from_to_layout.addWidget(self.from_input)
        self.from_to_layout.addWidget(to_label)
        self.from_to_layout.addWidget(self.to_input)
        self.from_to_layout.addStretch(1)
        
        possible_layout.addLayout(self.from_to_layout)

        # Кнопка Добавить
        add_btn_layout = QHBoxLayout()
        add_btn_layout.addStretch(1)
        self.btn_add_possible = QPushButton("Добавить")
        self.btn_add_possible.setFixedSize(160, 52)
        self.btn_add_possible.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.btn_add_possible.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_add_possible.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover { background-color: #e2e8f0; }
            QPushButton:pressed { background-color: #cbd5e1; }
        """)
        add_btn_layout.addWidget(self.btn_add_possible)
        
        possible_layout.addLayout(add_btn_layout)

        
        self.right_panel.addWidget(self.possible_val_page)   # index 3

        


# self.element_property_page (index 4)
        self.element_property_page = QWidget()
        prop_layout = QHBoxLayout(self.element_property_page)
        prop_layout.setContentsMargins(40, 30, 40, 30)
        prop_layout.setSpacing(40)

        # ХИМИЧЕСКИЕ ЭЛЕМЕНТЫ scroll
        left_col_widget = QWidget()
        left_col_layout = QVBoxLayout(left_col_widget)
        left_col_layout.setSpacing(8)

        left_title = QLabel("ХИМИЧЕСКИЕ ЭЛЕМЕНТЫ")
        left_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        left_title.setStyleSheet("color: #1f2937;")
        left_col_layout.addWidget(left_title)

        # Прокрутка для элементов
        self.left_elements_scroll = QScrollArea()
        self.left_elements_scroll.setWidgetResizable(True)
        self.left_elements_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;
            }
        """)

        left_scroll_content = QWidget()
        self.left_scroll_layout = QVBoxLayout(left_scroll_content)
        self.left_scroll_layout.setSpacing(8)
        self.left_scroll_layout.setContentsMargins(0, 0, 0, 0)


        self.active_element = None
        elements, columns = database.fetch_table("chem_element")
        self.element_labels = []
        for element in elements:
            lbl = QPushButton(element[1])
            lbl.setFont(QFont("Helvetica", 18))
            lbl.setProperty("id", int(element[0]))
            lbl.setStyleSheet("""QPushButton {
                                border: none;
                            background: transparent;
                            color: #1f2937;
                        padding-bottom: 4px;
                        padding-left: 10px;
                        margin-right: 40px;
                        text-align: left;
                        border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                        }
                        QPushButton:hover {
                    background-color: #f1f5f9;
                }
                """)
            lbl.setCursor(Qt.CursorShape.PointingHandCursor)
            lbl.clicked.connect(self.on_element_clicked)
            self.left_scroll_layout.addWidget(lbl)
            self.element_labels.append(lbl)

        self.left_elements_scroll.setWidget(left_scroll_content)
        left_col_layout.addWidget(self.left_elements_scroll)
        #left_col_layout.addStretch(1)

        prop_layout.addWidget(left_col_widget)

        col_separator = QFrame()
        col_separator.setFrameShape(QFrame.Shape.VLine)
        col_separator.setFixedWidth(1)
        col_separator.setStyleSheet("background-color: #cbd5e1;")
        prop_layout.addWidget(col_separator)

        # СВОЙСТВА scroll
        right_col_widget = QWidget()
        right_col_layout = QVBoxLayout(right_col_widget)
        right_col_layout.setSpacing(12)

        right_title = QLabel("СВОЙСТВА")
        right_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        right_title.setStyleSheet("color: #1f2937;")
        right_col_layout.addWidget(right_title)

        # Прокрутка для чекбоксов
        self.right_properties_scroll = QScrollArea()
        self.right_properties_scroll.setWidgetResizable(True)
        self.right_properties_scroll.setMinimumHeight(380)
        self.right_properties_scroll.setMinimumWidth(250)
        self.right_properties_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;
            }
        """)

        self.right_scroll_content = QWidget()
        self.right_scroll_layout = QVBoxLayout(self.right_scroll_content)
        self.right_scroll_layout.setSpacing(12)
        
        self.right_scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Чекбоксы
        self.check_all = QCheckBox("Выбрать все")
        self.check_all.setChecked(True)
        self.check_all.setFont(QFont("Helvetica", 18))
        self.check_all.setStyleSheet("""
            QCheckBox {
                color: #1f2937;
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 6px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
        """)
        #self.right_scroll_layout.addWidget(self.check_all,alignment=Qt.AlignmentFlag.AlignTop)


        properties_element, columns = database.get_elements_properties()
        unsign_properties,columns = database.fetch_table("property")
        
        self.property_checks = []
        for prop in properties_element:
           
                
                if self.active_element and self.active_element.property("id") == prop[1]:
                    cb = QCheckBox(prop[3])
                    cb.setProperty("id", int(prop[0]))
                    cb.setChecked(True)
                    cb.setFont(QFont("Helvetica", 18))
                    cb.setStyleSheet("""
                        QCheckBox {
                            color: #1f2937;
                        }
                        QCheckBox::indicator {
                            width: 24px;
                            height: 24px;
                        }
                    """)
                    cb.stateChanged.connect(self.on_element_property_checkbox_toggle)
                    self.right_scroll_layout.addWidget(cb,alignment=Qt.AlignmentFlag.AlignTop)
                    self.property_checks.append(cb)

        if self.active_element:
                for unsign in unsign_properties:
                    if unsign[0] not in self.property_checks:
                        cb = QCheckBox(unsign[1])
                        cb.setProperty("id", int(unsign[0]))
                        cb.setChecked(False)
                        cb.setFont(QFont("Helvetica", 18))
                        cb.setStyleSheet("""
                            QCheckBox {
                                color: #1f2937;
                            }
                            QCheckBox::indicator {
                                width: 24px;
                                height: 24px;
                            }
                        """)
                        cb.stateChanged.connect(self.on_element_property_checkbox_toggle)

                        self.right_scroll_layout.addWidget(cb,alignment=Qt.AlignmentFlag.AlignTop)                      
                
        
        
            


        self.right_properties_scroll.setWidget(self.right_scroll_content)
        right_col_layout.addWidget(self.right_properties_scroll)
        right_col_layout.addStretch(1)

        prop_layout.addWidget(right_col_widget)

        self.right_panel.addWidget(self.element_property_page)   # index 4

# self.element_value_page (index 5)
        self.element_value_page = QWidget()
        value_layout = QVBoxLayout(self.element_value_page)
        value_layout.setContentsMargins(40, 30, 40, 30)
        value_layout.setSpacing(30)

        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(40)

        #Левая колонка элементы
        left_col_widget = QWidget()
        left_col_layout = QVBoxLayout(left_col_widget)
        left_col_layout.setSpacing(8)

        left_title = QLabel("Элементы")
        left_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        left_title.setStyleSheet("color: #1f2937;")
        left_col_layout.addWidget(left_title)

        self.value_elements_scroll = QScrollArea()
        self.value_elements_scroll.setWidgetResizable(True)
        self.value_elements_scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        self.value_elements_content = QWidget()
        self.value_elements_inner = QVBoxLayout(self.value_elements_content)
        self.value_elements_inner.setSpacing(8)
        self.value_elements_inner.setContentsMargins(0, 0, 0, 0)

        self.active_element_inner = None

        elements, _ = database.fetch_table("chem_element")
        self.value_element_buttons = []
        for elem in elements:
            btn = QPushButton(elem[1])
            btn.setProperty("id", int(elem[0]))
            btn.setFont(QFont("Helvetica", 18))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""QPushButton {
                border: none;
                background: transparent;
                color: #1f2937;
                padding-bottom: 4px;
                padding-left: 10px;
                text-align: left;
                border-bottom: 2px solid rgba(148, 163, 184, 0.5);
            }
            QPushButton:hover { background-color: #f1f5f9; }""")
            btn.clicked.connect(self.on_value_element_clicked)
            self.value_elements_inner.addWidget(btn)
            self.value_element_buttons.append(btn)

        self.value_elements_scroll.setWidget(self.value_elements_content)
        left_col_layout.addWidget(self.value_elements_scroll)
        columns_layout.addWidget(left_col_widget)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet("background-color: #cbd5e1;")
        columns_layout.addWidget(sep)

        # Правая колонка свойства
        right_col_widget = QWidget()
        right_col_layout = QVBoxLayout(right_col_widget)
        right_col_layout.setSpacing(8)

        right_title = QLabel("Свойства")
        right_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        right_title.setStyleSheet("color: #1f2937;")
        right_col_layout.addWidget(right_title)

        self.value_props_scroll = QScrollArea()
        self.value_props_scroll.setWidgetResizable(True)
        self.value_props_scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        self.value_props_content = QWidget()
        self.value_props_inner = QVBoxLayout(self.value_props_content)
        self.value_props_inner.setSpacing(8)
        self.value_props_inner.setContentsMargins(0, 0, 0, 0)

        self.active_property_inner = None

        properties_inner_element, columns = database.get_elements_properties()

        #properties, _ = database.fetch_table("property")
        self.value_prop_buttons = []
        for prop in properties_inner_element:
            if self.active_element_inner and self.active_element_inner.property("id") == prop[1]:
                btn = QPushButton(prop[3])
                btn.setProperty("id", int(prop[2]))
                btn.setProperty("element_property_id", int(prop[0]))
                btn.setFont(QFont("Helvetica", 18))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("""QPushButton {
                    border: none;
                    background: transparent;
                    color: #1f2937;
                    padding-bottom: 4px;
                    padding-left: 10px;
                    text-align: left;
                    border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                }
                QPushButton:hover { background-color: #f1f5f9; }""")
                btn.clicked.connect(self.on_value_prop_clicked)
                self.value_props_inner.addWidget(btn)
                self.value_prop_buttons.append(btn)

        self.value_props_scroll.setWidget(self.value_props_content)
        right_col_layout.addWidget(self.value_props_scroll)
        columns_layout.addWidget(right_col_widget)

        value_layout.addLayout(columns_layout)

        # ЗНАЧЕНИЯ scroll
        values_title = QLabel("Возможные значения")
        values_title.setFont(QFont("Helvetica", 22, QFont.Weight.Bold))
        values_title.setAlignment(Qt.AlignmentFlag.AlignRight)
        value_layout.addWidget(values_title)

        self.values_scroll = QScrollArea()
        self.values_scroll.setWidgetResizable(True)
        self.values_scroll.setMinimumHeight(120)
        self.values_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: white;
            }
        """)

        values_content = QWidget()
        values_inner_layout = QVBoxLayout(values_content)
        values_inner_layout.setSpacing(12)
        values_inner_layout.setContentsMargins(0, 0, 0, 0)

        # текущее значение
        self.info_layout = QHBoxLayout()
        self.info_layout.setSpacing(30)

        

        current_label = QLabel("Текущее значение :")
        current_label.setFont(QFont("Helvetica", 19, QFont.Weight.Bold))

        

        self.current_value_label = QLabel("")
        self.current_value_label.setFont(QFont("Helvetica", 19))

        
        self.info_layout.addWidget(current_label)
        self.info_layout.addWidget(self.current_value_label)

        self.info_layout.addStretch(1)
        
        self.possibles_container = QWidget()
        self.possibles_layout = QVBoxLayout(self.possibles_container)
        self.possibles_layout.setSpacing(6)
        self.possibles_layout.setContentsMargins(0, 0, 0, 0)


        possibles_values, columns = database.fetch_table("possible_value")

        for possible_value in possibles_values:
            if self.active_element_inner and self.active_property_inner and self.active_property_inner.property("id") == possible_value[1]:
                value_pos = str(possible_value[2])
                formatted_value_pos = value_pos.replace('-', ';')
                if any(c.isdigit() for c in value_pos):
                        formatted_value_pos = f"[{formatted_value_pos}]"

                possible_value_label = QLabel(formatted_value_pos)
                possible_value_label.setFont(QFont("Helvetica", 18))
                self.possibles_layout.addWidget(possible_value_label)
        

        self.info_layout.addWidget(self.possibles_container)
        values_inner_layout.addLayout(self.info_layout)

        self.values_scroll.setWidget(values_content)
        value_layout.addWidget(self.values_scroll)

        # ввод + добавить
        input_layout = QHBoxLayout()
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Введите значение")
        self.value_input.setFont(QFont("Helvetica", 18))
        self.value_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 8px;
                background: transparent;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #3b82f6;
            }
        """)

        self.value_add_btn = QPushButton("Добавить")
        self.value_add_btn.setFixedSize(160, 52)
        self.value_add_btn.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
        self.value_add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.value_add_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                border: 2px solid transparent;
                border-radius: 12px;
                color: #334155;
            }
            QPushButton:hover { background-color: #e2e8f0; }
            QPushButton:pressed { background-color: #cbd5e1; }
        """)

        input_layout.addWidget(self.value_input)
        input_layout.addWidget(self.value_add_btn)
        value_layout.addLayout(input_layout)

        value_layout.addStretch(1)

        self.right_panel.addWidget(self.element_value_page)  # index 5



# self.check_data_page (Проверка полноты знаний)
        self.check_data_page = QWidget()
        check_layout = QVBoxLayout(self.check_data_page)
        check_layout.setContentsMargins(40, 30, 40, 30)
        check_layout.setSpacing(25)

        self.warning_label = QLabel("Есть незаполненные значения")
        self.warning_label.setFont(QFont("Helvetica", 20, QFont.Weight.Bold))
        self.warning_label.setStyleSheet("color: #ef4444;")
        self.warning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        check_layout.addWidget(self.warning_label)

        self.warning_label.hide()


        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(40)

        # СВОЙСТВА
        left_widget = QWidget()
        left_col = QVBoxLayout(left_widget)
        left_col.setSpacing(8)

        left_title = QLabel("Свойства")
        left_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        left_title.setStyleSheet("color: #1f2937;")
        left_col.addWidget(left_title)
        
        self.check_properties_scroll = QScrollArea()
        self.check_properties_scroll.setWidgetResizable(True)
        self.check_properties_scroll.setMinimumHeight(220)
        self.check_properties_scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        props_content = QWidget()
        self.props_inner = QVBoxLayout(props_content)
        self.props_inner.setSpacing(6)
        self.props_inner.setContentsMargins(0, 0, 0, 0)


        self.active_property_unsigned = None

        seen_ids = set()

        unsigned_rows, cols = database.get_unvalued_property_for_element()

        if unsigned_rows != []:
            self.warning_label.show()
        else:
            self.warning_label.hide()

        for unsigned_row in unsigned_rows:
            prop_id = int(unsigned_row[2])

            if prop_id in seen_ids:
                continue

            seen_ids.add(prop_id)

            lbl = QPushButton(database.get_property_name(unsigned_row[2]))
            lbl.setProperty("id", int(unsigned_row[2]))
            lbl.setFont(QFont("Helvetica", 18))
            lbl.setStyleSheet("""QPushButton {
                    border: none;
                    background: transparent;
                    color: #1e40af;
                    padding: 2px 0;
                    
                    border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                }
                QPushButton:hover { background-color: #f1f5f9; }""")
            lbl.setCursor(Qt.CursorShape.PointingHandCursor)
            lbl.clicked.connect(self.on_unsigned_prop_clicked)
            self.props_inner.addWidget(lbl)

        self.check_properties_scroll.setWidget(props_content)
        left_col.addWidget(self.check_properties_scroll)
        columns_layout.addWidget(left_widget)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedWidth(1)
        sep.setStyleSheet("background-color: #cbd5e1;")
        columns_layout.addWidget(sep)

        # ХИМИЧЕСКИЕ ЭЛЕМЕНТЫ
        right_widget = QWidget()
        right_col = QVBoxLayout(right_widget)
        right_col.setSpacing(8)

        right_title = QLabel("Химические элементы")
        right_title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        right_title.setStyleSheet("color: #1f2937;")
        right_col.addWidget(right_title)

        self.check_elements_scroll = QScrollArea()
        self.check_elements_scroll.setWidgetResizable(True)
        self.check_elements_scroll.setMinimumHeight(220)
        self.check_elements_scroll.setStyleSheet("QScrollArea { border: none; background: white; }")

        elems_content = QWidget()
        self.elems_inner = QVBoxLayout(elems_content)
        self.elems_inner.setSpacing(6)
        self.elems_inner.setContentsMargins(0, 0, 0, 0)

        unsigned_rows, cols = database.get_unvalued_property_for_element()

        for unsigned_row in unsigned_rows:
            if self.active_property_unsigned and self.active_property_unsigned.property("id") == unsigned_row[2]:
                lbl = QLabel(database.get_chem_element_name(unsigned_row[1]))
                lbl.setFont(QFont("Helvetica", 18))
                lbl.setStyleSheet("color: #1e40af; padding: 2px 0;")
                self.elems_inner.addWidget(lbl)

        self.check_elements_scroll.setWidget(elems_content)
        right_col.addWidget(self.check_elements_scroll)
        columns_layout.addWidget(right_widget)

        check_layout.addLayout(columns_layout)
        check_layout.addStretch(1)

        self.right_panel.addWidget(self.check_data_page)   # index 6


        content_layout.addWidget(self.right_panel)
        self.main_layout.addLayout(content_layout)

        for i, btn in enumerate(self.menu_buttons):
            btn.clicked.connect(lambda checked=False, idx=i: self._on_menu_clicked(idx))

        self.btn_check.clicked.connect(self._on_check_clicked)
        self.btn_back.clicked.connect(self._on_back_clicked)
        self.chemical_btn_add.clicked.connect(self._on_chemical_add_clicked)
        self.property_btn_add.clicked.connect(self._on_property_add_clicked)
        self.btn_add_possible.clicked.connect(self._on_possible_add_clicked)

        self.value_add_btn.clicked.connect(self._on_value_add_clicked)

# def
    def load_elements(self,widget):
        if widget == 1:
            drows, columns = database.fetch_table("chem_element")

            rows = 0
            cols = 0

            for drow in drows:
                item = QLabel(f'<a href="chemical_delete" style="color:#ef4444; text-decoration: none;">✕</a> {str(drow[1])}')
                item.setTextFormat(Qt.TextFormat.RichText)
                item.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                item.setOpenExternalLinks(False)
                item.linkActivated.connect(self.on_link_clicked)

                item.setProperty("id", int(drow[0]))
                item.setProperty("name", drow[1])
                item.setFont(QFont("Helvetica", 18))
                item.setStyleSheet("padding: 2px 0; color: #1f2937;")

                self.chemical_grid_layout.addWidget(item, rows, cols)

                cols += 1
                if cols == 3:
                    cols = 0
                    rows += 1
        elif widget == 2:
            drows,columns =  database.fetch_table("property")
    
            rows = 0
            cols = 0
            for drow in drows:

                item = QLabel(f'<a href="property_delete" style="color:#ef4444; text-decoration: none;">✕</a> {str(drow[1])}')
                item.setTextFormat(Qt.TextFormat.RichText)
                item.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                item.setOpenExternalLinks(False)
                item.linkActivated.connect(self.on_link_clicked)

                item.setProperty("id", int(drow[0]))
                item.setProperty("name", drow[1])
                item.setFont(QFont("Helvetica", 18))
                item.setStyleSheet("padding: 0px 0; color: #1f2937;")
                self.property_grid_layout.addWidget(item, rows, cols)
                cols += 1
                if cols == 1:
                    cols = 0
                    rows += 1
        elif widget == 3:
            possibles, columns = database.fetch_table("possible_value")

            #print(possibles)
            rows = 0
            cols = 0
            for possible in possibles:
                if self.active_property_tab.property("id") == possible[1]:

                    value = str(possible[2])
                    if self.radio_substance.isChecked():
                        # только числа/диапазоны
                        if not re.fullmatch(r"[0-9.\-]+", value):
                            continue 
                    elif self.radio_qualitative.isChecked():
                        # только слова
                        if not re.fullmatch(r"[а-яА-Яa-zA-Z\s]+", value):
                            continue

                    formatted = value.replace('-', ';')

                    if any(c.isdigit() for c in value):
                        formatted = f"[{formatted}]"

                    range_label = QLabel(
                        f"<a href='property_possible_delete' style='color:#ef4444; text-decoration: none;'>✕</a>{formatted}"
                    )
                    range_label.setTextFormat(Qt.TextFormat.RichText)
                    range_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
                    range_label.setOpenExternalLinks(False)
                    range_label.linkActivated.connect(self.on_link_clicked)
                    
                    range_label.setProperty("id", int(possible[0]))
                    range_label.setProperty("name", possible[2])
                    range_label.setFont(QFont("Helvetica", 20))
                    range_label.setStyleSheet("padding: 0px 0; color: #1f2937;")
                    self.possibles_property_grid_layout.addWidget(range_label, rows, cols,alignment=Qt.AlignmentFlag.AlignTop)
                    cols += 1
                    if cols == 1:
                        cols = 0
                        rows += 1
        elif widget == 31:
            

            
            tabs,columns =  database.fetch_table("property")
            for text in tabs:
                tab = QPushButton(str(text[1]))
                tab.setProperty("id", int(text[0]))
                tab.setFont(QFont("Helvetica", 18, QFont.Weight.Medium))
                tab.setStyleSheet("""
                        QPushButton {
                            border: none; background: transparent; color: #64748b; padding-bottom: 6px;
                        }
                        QPushButton:hover {
                            background-color: #f1f5f9;
                        }
                    """)
                tab.setCursor(Qt.CursorShape.PointingHandCursor)
                tab.clicked.connect(self.on_property_tab_clicked)
                self.tabs_layout.addWidget(tab)
        elif widget == 4:
                # Чекбоксы

            self.check_all = QCheckBox("Выбрать все")
            self.check_all.setChecked(True)
            self.check_all.setFont(QFont("Helvetica", 18))
            self.check_all.setStyleSheet("""
                QCheckBox {
                    color: #1f2937;
                    border-bottom: 3px solid #3b82f6;
                    padding-bottom: 6px;
                }
                QCheckBox::indicator {
                    width: 24px;
                    height: 24px;
                }
            """)
            #self.right_scroll_layout.addWidget(self.check_all,alignment=Qt.AlignmentFlag.AlignTop)


            properties_element, columns = database.get_elements_properties()
            unsign_properties, columns = database.fetch_table("property")
            
            self.property_checks = []
            for prop in properties_element:
                    if self.active_element and self.active_element.property("id") == prop[1]:
                        cb = QCheckBox(prop[3])
                        cb.setProperty("id", int(prop[0]))
                        cb.setChecked(True)
                        cb.setFont(QFont("Helvetica", 18))
                        cb.setStyleSheet("""
                            QCheckBox {
                                color: #1f2937;
                            }
                            QCheckBox::indicator {
                                width: 24px;
                                height: 24px;
                            }
                        """)
                        cb.stateChanged.connect(self.on_element_property_checkbox_toggle)
                        self.right_scroll_layout.addWidget(cb,alignment=Qt.AlignmentFlag.AlignTop)
                        self.property_checks.append(prop[2])
            if self.active_element:
                for unsign in unsign_properties:
                    if unsign[0] not in self.property_checks:
                        cb = QCheckBox(unsign[1])
                        cb.setProperty("id", int(unsign[0]))
                        cb.setChecked(False)
                        cb.setFont(QFont("Helvetica", 18))
                        cb.setStyleSheet("""
                            QCheckBox {
                                color: #1f2937;
                            }
                            QCheckBox::indicator {
                                width: 24px;
                                height: 24px;
                            }
                        """)
                        cb.stateChanged.connect(self.on_element_property_checkbox_toggle)
                        self.right_scroll_layout.addWidget(cb,alignment=Qt.AlignmentFlag.AlignTop)

                    



        elif widget == 41:
            elements, columns = database.fetch_table("chem_element")
            self.element_labels = []
            for element in elements:
                lbl = QPushButton(element[1])
                lbl.setFont(QFont("Helvetica", 18))
                lbl.setProperty("id", int(element[0]))
                lbl.setStyleSheet("""QPushButton {
                                    border: none;
                                background: transparent;
                                color: #1f2937;
                            padding-bottom: 4px;
                            padding-left: 10px;
                            margin-right: 40px;
                            text-align: left;
                            border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                            }
                            QPushButton:hover {
                        background-color: #f1f5f9;
                    }
                    """)
                lbl.setCursor(Qt.CursorShape.PointingHandCursor)
                lbl.clicked.connect(self.on_element_clicked)
                self.left_scroll_layout.addWidget(lbl)
                self.element_labels.append(lbl)
        elif widget == 5:
            elements, _ = database.fetch_table("chem_element")
            self.value_element_buttons = []
            for elem in elements:
                btn = QPushButton(elem[1])
                btn.setProperty("id", int(elem[0]))
                btn.setFont(QFont("Helvetica", 18))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setStyleSheet("""QPushButton {
                    border: none;
                    background: transparent;
                    color: #1f2937;
                    padding-bottom: 4px;
                    padding-left: 10px;
                    text-align: left;
                    border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                }
                QPushButton:hover { background-color: #f1f5f9; }""")
                btn.clicked.connect(self.on_value_element_clicked)
                self.value_elements_inner.addWidget(btn)
                self.value_element_buttons.append(btn)
        elif widget == 51:
            properties_inner_element, columns = database.get_elements_properties()


            #properties, _ = database.fetch_table("property")
            self.value_prop_buttons = []
            for prop in properties_inner_element:
                if self.active_element_inner and self.active_element_inner.property("id") == prop[1]:
                    possibles = database.get_property_possible(prop[2])
                    if possibles != []:
                        btn = QPushButton(prop[3])
                        btn.setProperty("id", int(prop[2]))
                        btn.setProperty("element_property_id", int(prop[0]))
                        btn.setFont(QFont("Helvetica", 18))
                        btn.setCursor(Qt.CursorShape.PointingHandCursor)
                        btn.setStyleSheet("""QPushButton {
                            border: none;
                            background: transparent;
                            color: #1f2937;
                            padding-bottom: 4px;
                            padding-left: 10px;
                            text-align: left;
                            border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                        }
                        QPushButton:hover { background-color: #f1f5f9; }""")
                        btn.clicked.connect(self.on_value_prop_clicked)
                        self.value_props_inner.addWidget(btn)
                        self.value_prop_buttons.append(btn)
        elif widget == 52:
            
    
            
            possibles_values, columns = database.fetch_table("possible_value")

            for possible_value in possibles_values:
                #print(f"id кнопки property: {self.active_property_inner.property('id')}")
                #print(f"id из possible {possible_value[1]}")
                if self.active_element_inner and self.active_property_inner and self.active_property_inner.property("id") == possible_value[1]:
                    #print("uslovie")
                    value_pos = str(possible_value[2])
                    formatted_value_pos = value_pos.replace('-', ';')
                    if any(c.isdigit() for c in value_pos):
                            formatted_value_pos = f"[{formatted_value_pos}]"

                    possible_value_label = QLabel(formatted_value_pos)
                    possible_value_label.setFont(QFont("Helvetica", 18))
                    self.possibles_layout.addWidget(possible_value_label)
        elif widget == 6:
            seen_ids = set()

            unsigned_rows, cols = database.get_unvalued_property_for_element()

            for unsigned_row in unsigned_rows:
                prop_id = int(unsigned_row[2])

                if prop_id in seen_ids:
                    continue

                seen_ids.add(prop_id)
                lbl = QPushButton(database.get_property_name(unsigned_row[2]))
                lbl.setProperty("id", int(unsigned_row[2]))
                lbl.setFont(QFont("Helvetica", 18))
                lbl.setStyleSheet("""QPushButton {
                        border: none;
                        background: transparent;
                        color: #1e40af;
                        padding: 2px 0;
                        
                        border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                    }
                    QPushButton:hover { background-color: #f1f5f9; }""")
                lbl.setCursor(Qt.CursorShape.PointingHandCursor)
                lbl.clicked.connect(self.on_unsigned_prop_clicked)
                self.props_inner.addWidget(lbl)


    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def refresh_list(self, widget):
        if widget == 1:
            self.clear_layout(self.chemical_grid_layout)
            self.load_elements(1)
        elif widget == 2:
            self.clear_layout(self.property_grid_layout)
            self.load_elements(2)
        elif widget == 3:
            self.clear_layout(self.possibles_property_grid_layout)
            self.load_elements(3)
        elif widget == 31:
            active_id = None
            if self.active_property_tab:
                active_id = self.active_property_tab.property("id")

            self.active_property_tab = None

            self.clear_layout(self.tabs_layout)
            self.load_elements(31)

            # активная вкладка
            found = False
            if active_id is not None:
                for i in range(self.tabs_layout.count()):
                    btn = self.tabs_layout.itemAt(i).widget()
                    if btn and btn.property("id") == active_id:
                        self.set_active_property_tab_button(btn)
                        found = True
                        break

            if not found and self.tabs_layout.count() > 0:
                first_button = self.tabs_layout.itemAt(0).widget()
                if first_button:
                    self.set_active_property_tab_button(first_button)
        elif widget == 4:
            self.clear_layout(self.right_scroll_layout)
            self.load_elements(4)
        
        elif widget == 41:
            self.active_element = None
            self.clear_layout(self.left_scroll_layout)
            self.load_elements(41)
        elif widget == 5:
            self.active_element_inner = None
            self.clear_layout(self.value_elements_inner)
            self.load_elements(5)
            self.refresh_list(53)
        elif widget == 51:
            self.active_property_inner = None
            self.clear_layout(self.value_props_inner)
            self.load_elements(51)
            self.refresh_list(53)
        elif widget == 52:
            
            self.clear_layout(self.possibles_layout)
            self.load_elements(52)
            self.refresh_list(53)
            
        elif widget == 53:
            self.current_value_label.setText("")
            if self.active_element_inner:
                element_values = database.get_properties_value(self.active_element_inner.property("id"))
                if element_values and self.active_property_inner:
                    name_property = database.get_property_name(self.active_property_inner.property("id"))
                    
                    if name_property in element_values:
                        self.current_value_label.setText(element_values[name_property])
        elif widget == 6:
            self.active_property_unsigned = None
            self.clear_layout(self.props_inner)
            self.load_elements(6)
            self.refresh_list(61)
        elif widget == 61:
            self.clear_layout(self.elems_inner)
            unsigned_rows, cols = database.get_unvalued_property_for_element()

            if unsigned_rows != []:
                self.warning_label.show()
            else:
                self.warning_label.hide()
                
            for unsigned_row in unsigned_rows:
                if self.active_property_unsigned and self.active_property_unsigned.property("id") == unsigned_row[2]:
                    lbl = QLabel(database.get_chem_element_name(unsigned_row[1]))
                    lbl.setFont(QFont("Helvetica", 18))
                    lbl.setStyleSheet("color: #1e40af; padding: 2px 0;")
                    self.elems_inner.addWidget(lbl)


    def _on_menu_clicked(self, index: int):
        button = self.sender()
        self.set_active_button(button)

        texts = [
            "Химические элементы",
            "Свойства",
            "Возможные значения",
            "Описание свойств класса",
            "Значение для класса"
        ]
        #print(f"{texts[index]} (index {index})")

        # Переключение правой панели
        if index == 0:                                      # Химические элементы
            self.right_panel.setCurrentIndex(1)
        elif index == 1:
            self.right_panel.setCurrentIndex(2)
        elif index == 2:
            self.right_panel.setCurrentIndex(3)   
        elif index == 3:
            self.right_panel.setCurrentIndex(4)
        elif index == 4:
            self.right_panel.setCurrentIndex(5)
        elif index == 5:
            self.right_panel.setCurrentIndex(6)          
        else:
            self.right_panel.setCurrentIndex(0)# placeholder

    def _on_check_clicked(self):
        button = self.sender()
        self.set_active_button(button)
        self.right_panel.setCurrentIndex(6)

    def _on_back_clicked(self):
        self.stack.setCurrentIndex(0)

    def on_link_clicked(self, link):
        if link == "chemical_delete":
            label = self.sender()
            element_id = label.property("id")
            text = label.property("name")
            count = database.count_chem_elements()

            if count <= 1:
                self.show_error("Нельзя удалить последний элемент")
                return

            self.show_delete_dialog(element_id, text,1)

        if link == "property_delete":
            label = self.sender()
            property_id = label.property("id")
            text = label.property("name")
            count = database.count_property()

            if count <= 1:
                self.show_error("Нельзя удалить последнее свойство")
                return

            self.show_delete_dialog(property_id, text,2)
        if link == "property_possible_delete":
            label = self.sender()
            property_possible_id = label.property("id")
            text = label.property("name")
            self.show_delete_dialog(property_possible_id, text,3)



    def show_delete_success(self, text):
        msg = QMessageBox(self)
        msg.setWindowTitle("Удаление")
        msg.setText(f"Успешное удаление: \"{text}\"")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    update_class_table_signal = pyqtSignal()

    def show_delete_dialog(self, _id, text, widget):
        msg = QMessageBox(self)
        msg.setWindowTitle("Подтверждение удаления")
        msg.setText(f"Вы действительно хотите удалить \"{text}\"?")
        msg.setIcon(QMessageBox.Icon.Warning)

        btn_yes = msg.addButton("Да", QMessageBox.ButtonRole.YesRole)
        btn_no = msg.addButton("Нет", QMessageBox.ButtonRole.NoRole)

        msg.exec()

        if msg.clickedButton() == btn_yes:
            if widget == 1:
                database.delete_chem_element(_id)
                self.refresh_list(1)
                self.show_delete_success(text)
                self.refresh_list(41)
                self.refresh_list(5)
                self.refresh_list(51)
                self.refresh_list(52)
                self.update_table_data_signal.emit()
                self.refresh_list(6)
            if widget == 2:
                database.delete_property(_id)
                self.refresh_list(2)
                self.show_delete_success(text)
                self.refresh_list(31)
                self.refresh_list(4)
                self.refresh_list(51)
                self.refresh_list(52)
                self.update_class_table_signal.emit()
                self.refresh_list(6)
            if widget ==3:
                database.delete_possible_value(_id)
                self.refresh_list(3)
                self.refresh_list(52)
                self.refresh_list(51)
                self.show_delete_success(text)
                self.update_class_table_signal.emit()

    def is_valid_name(self,name: str) -> bool:
        return bool(re.fullmatch(r"[А-Яа-яЁё\s]+", name))

    def show_success(self, name):
        msg = QMessageBox(self)
        msg.setWindowTitle("Успешно")
        msg.setText(f"Успешное добавление: \"{name}\"")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    update_table_data_signal = pyqtSignal()

    def _on_chemical_add_clicked(self):
        name = self.chemical_element_input.text().strip()

        if not name:
            self.show_error("Введите название элемента")
            return
        
        if not self.is_valid_name(name):
            self.show_error("Название должно содержать только русские буквы")
            return

        result = database.add_chem_element(name)
        if not result:
            self.show_error("Такой элемент уже существует")
            return

        self.chemical_element_input.clear()
        self.refresh_list(1)
        self.refresh_list(41)
        self.refresh_list(5)
        self.refresh_list(51)
        self.refresh_list(52)
        self.update_table_data_signal.emit()
        
        self.show_success(name)

    def _on_property_add_clicked(self):
            name = self.property_element_input.text().strip()

            if not name:
                self.show_error("Введите название свойства")
                return
            
            if not self.is_valid_name(name):
                self.show_error("Название должно содержать только русские буквы")
                return

            result = database.add_property(name)
            if not result:
                self.show_error("Такое свойство уже существует")
                return

            self.property_element_input.clear()
            self.refresh_list(2)
            self.show_success(name)
            self.refresh_list(31)
            self.refresh_list(4)
            self.refresh_list(51)
            self.refresh_list(52)
    
    def _on_possible_add_clicked(self):
        property_id = self.active_property_tab.property("id")
        if self.radio_substance.isChecked():

            existing = database.get_property_possible(property_id)

            if any(not self.is_numeric_range(v) for v in existing):
                self.show_error("Для данного свойства уже задано качественное значение")
                return
            
            from_l = self.from_input.text().strip()
            to_l = self.to_input.text().strip()
            #Пусто в От
            if not from_l:
                self.show_error("Введите поле 'От'")
                return
            
            #Пусто в До
            if not to_l:
                self.show_error("Введите поле 'До'")
                return
            
            #Не целое От Или До
            if self.checkbox_integer.isChecked():

                if not from_l.isdigit():
                    self.show_error("В поле 'От' не целое число")
                    return
                elif not to_l.isdigit():
                    self.show_error("В поле 'До' не целое число")
                    return
                elif from_l.isdigit() and to_l.isdigit():
                    result = database.add_possible_value(property_id,(int(from_l),int(to_l)))
                    if not result:
                        self.show_error("Ошибка при добавлении или такое возможное значение уже существует")
                        return
                    self.property_element_input.clear()
                    self.refresh_list(3)
                    self.refresh_list(52)
                    self.refresh_list(51)
                    self.show_success(f"{from_l} и {to_l}")
                    self.update_class_table_signal.emit()
                    
                    
            # целое или символы
            else:

                if not self.is_two_decimal_number(from_l):
                    self.show_error("В поле 'От' не число с двумя знаками после запятой")
                    return
                elif not self.is_two_decimal_number(to_l):
                    self.show_error("В поле 'До' не число с двумя знаками после запятой")
                    return
                elif self.is_two_decimal_number(from_l) and self.is_two_decimal_number(to_l):
                    result = database.add_possible_value(property_id,(Decimal(from_l), Decimal(to_l)))
                    if not result:
                        self.show_error("Ошибка при добавлении или такое возможное значение уже существует")
                        return
                    self.property_element_input.clear()
                    self.refresh_list(3)
                    self.refresh_list(52)
                    self.refresh_list(51)
                    self.show_success(f"{from_l} и {to_l}")
                    self.update_class_table_signal.emit()
                    

        elif self.radio_qualitative.isChecked():
            existing = database.get_property_possible(property_id)

            if any(self.is_numeric_range(v) for v in existing):
                self.show_error("Для данного свойства уже задан вещественный диапазон")
                return

            newvalue = self.single_input.text().strip()
            if not newvalue:
                self.show_error("Введите строку")
                return
            
            if not self.is_word(newvalue):
                self.show_error("Некорректная строка")
                return

            result = database.add_possible_value(property_id, newvalue)
            if not result:
                self.show_error("Ошибка при добавлении или такое возможное значение уже существует")
                return
            self.property_element_input.clear()
            self.refresh_list(3)
            self.refresh_list(52)
            self.refresh_list(51)
            self.show_success(f"{newvalue}")
            self.update_class_table_signal.emit()
            
    def show_patch_dialog(self,exist, p_e_id,new_value_text):
        msg = QMessageBox(self)
        msg.setWindowTitle("Подтверждение")
        msg.setText(f"Для этого свойства уже существует значение {exist}. Заменить?")
        msg.setIcon(QMessageBox.Icon.Warning)

        btn_yes = msg.addButton("Да", QMessageBox.ButtonRole.YesRole)
        btn_no = msg.addButton("Нет", QMessageBox.ButtonRole.NoRole)

        msg.exec()

        if msg.clickedButton() == btn_yes:
            new_value = database.patch_value_chem_element(p_e_id,new_value_text)

            if isinstance(new_value, int):
                self.refresh_list(53)
                self.show_success(f"{new_value_text}")
                self.refresh_list(6)
            else:
                self.show_error(new_value)



    def _on_value_add_clicked(self):
        new_value_text = self.value_input.text().strip()
        if new_value_text == "" or None:
            self.show_error("Введите значение")
            return
        if not self.active_element_inner:
            self.show_error("Выберите элемент")
            return
        if self.active_property_inner:
            p_e_id = self.active_property_inner.property("element_property_id")
            exist = database.get_value_chem_property_id(p_e_id)
            if exist:
                self.show_patch_dialog(exist,p_e_id ,new_value_text)
                return
            new_value = database.add_value_chem_element(p_e_id,new_value_text)

            if isinstance(new_value, int):
                self.refresh_list(53)
                self.show_success(f"Значения {new_value_text}")
                self.refresh_list(6)
            else:
                self.show_error(new_value)
        else:
            self.show_error("Выберите свойство")
        self.value_input.clear()


    def is_word(self,new_value: str) -> bool:
        return bool(re.fullmatch(r"[А-Яа-яЁё\s]+", new_value))

    def is_two_decimal_number(self, value: str) -> bool:
        return bool(re.fullmatch(r"\d+\.\d{2}", str(value)))
            
    def is_numeric_range(self, value: str) -> bool:
        try:
            parts = value.split("-")
            if len(parts) != 2:
                return False

            float(parts[0])
            float(parts[1])
            return True
        except ValueError:
            return False  

    def show_error(self, text):
        msg = QMessageBox(self)
        msg.setWindowTitle("Ошибка")
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()

    def set_active_button(self, button):
        if self.active_button:
            self.active_button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 16px 28px;
                    border: none;
                    border-bottom: 1px solid #e5e7eb;
                    background-color: white;
                    color: #1f2937;
                }
                QPushButton:hover { background-color: #f8fafc; }
                QPushButton:pressed { background-color: #f1f5f9; }
            """)

        button.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 16px 28px;
                border: none;
                border-bottom: 3px solid #3b82f6;
                background-color: white;
                color: #1f2937;
            }
        """)
        self.active_button = button

    def set_active_property_tab_button(self, button):
        if self.active_property_tab:
                try:
                    self.active_property_tab.setStyleSheet("""
                        QPushButton {
                            border: none; background: transparent; color: #64748b; padding-bottom: 6px;
                        }
                        QPushButton:hover {
                            background-color: #f1f5f9;
                        }
                    """)
                except RuntimeError:
                    pass

            # устанавливаем новую активную
        button.setStyleSheet("""
                QPushButton {
                    border: none;
                    background: transparent;
                    color: #1e40af;
                    border-bottom: 3px solid #3b82f6;
                    padding-bottom: 6px;
                }
            """)

        self.active_property_tab = button
        self.refresh_list(3)

    def on_radio_changed(self):
        self.refresh_list(3)
        if self.radio_qualitative.isChecked():
            self.clear_layout(self.from_to_layout)
            self.checkbox_integer.hide()
            

            self.single_input = QLineEdit()
            self.single_input.setFixedWidth(300)
            self.single_input.setPlaceholderText("Введите строку")

            self.single_input.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 2px solid #e5e7eb;
                    font-size: 18px;
                    padding-bottom: 6px;
                    background: transparent;
                }
                QLineEdit:focus {
                    border-bottom: 2px solid #3b82f6;
                }
            """)

            self.from_to_layout.addWidget(self.single_input,alignment=Qt.AlignmentFlag.AlignLeft)
        
        elif self.radio_substance.isChecked():
            self.clear_layout(self.from_to_layout)
            self.checkbox_integer.show()

            
            

            from_label = QLabel("От")
            from_label.setFont(QFont("Helvetica", 18))
            self.from_input = QLineEdit()
            self.from_input.setPlaceholderText("0.00")
            self.from_input.setFixedWidth(140)
            self.from_input.setStyleSheet("""
                QLineEdit {
                    border: none;
                    border-bottom: 2px solid #e5e7eb;
                    font-size: 18px;
                    padding-bottom: 6px;
                    background: transparent;
                }
                QLineEdit:focus {
                    border-bottom: 2px solid #3b82f6;
                }
            """)

            to_label = QLabel("До")
            to_label.setFont(QFont("Helvetica", 18))
            self.to_input = QLineEdit()
            self.to_input.setPlaceholderText("20.00")
            self.to_input.setFixedWidth(140)
            self.to_input.setStyleSheet(self.from_input.styleSheet())

            self.from_to_layout.addWidget(from_label)
            self.from_to_layout.addWidget(self.from_input)
            self.from_to_layout.addWidget(to_label)
            self.from_to_layout.addWidget(self.to_input)
            self.from_to_layout.addStretch(1)


    def on_property_tab_clicked(self):
        button = self.sender()
        self.set_active_property_tab_button(button)

    def on_checkbox_integer_toggle(self, state):
        if self.checkbox_integer.isChecked():
            self.from_input.setPlaceholderText("0")
            self.to_input.setPlaceholderText("20")
        else:
            self.from_input.setPlaceholderText("0.00")
            self.to_input.setPlaceholderText("20.00")

    

    def on_element_property_checkbox_toggle(self,state):
        cb = self.sender()
        print("Нажат")
        if cb.isChecked():
            print("Работает")
            property_id = cb.property("id")
            element_id = self.active_element.property("id")
            new_id = database.add_property_for_element(element_id,property_id)
            if not new_id:
                self.show_error(f"Ошибка при добавлении свойства элементу {element_id}")
                return
            cb.setProperty("id", int(new_id))
            #self.show_success(f"свойства")
        else:
            old_id = cb.property("id")
            element_id = self.active_element.property("id")
            database.delete_property_for_element(old_id)
        self.refresh_list(4)
        self.refresh_list(51)
        self.refresh_list(52)
        self.refresh_list(6)
        
            


    def set_active_element(self,button):
        if self.active_element:
            self.active_element.setStyleSheet("""QPushButton {
                                border: none;
                            background: transparent;
                            color: #1f2937;
                        padding-bottom: 4px;
                        padding-left: 10px;
                        margin-right: 40px;
                        text-align: left;
                        border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                        }
                        QPushButton:hover {
                    background-color: #f1f5f9;
                }
                """)
        button.setStyleSheet("""
                QPushButton {
                                border: none;
                            background: transparent;
                            color: #1f2937;
                        padding-bottom: 4px;
                        padding-left: 10px;
                        margin-right: 40px;
                        text-align: left;
                        border-bottom: 3px solid #3b82f6;
                        }
                        
            """)
        self.active_element = button
        self.refresh_list(4)

    def on_element_clicked(self):
        button = self.sender()
        self.set_active_element(button)


    def on_value_element_clicked(self):
        button = self.sender()
        
        self.set_value_element_active(button)
        

    def on_value_prop_clicked(self):
        button = self.sender()
        self.set_value_prop_active(button)
        

    def set_value_element_active(self, button):
        # сброс предыдущего
        if self.active_element_inner:
            self.active_element_inner.setStyleSheet("""QPushButton {
                border: none; background: transparent; color: #1f2937;
                padding-bottom: 4px; padding-left: 10px; text-align: left;
                border-bottom: 2px solid rgba(148, 163, 184, 0.5);
            }
            QPushButton:hover { background-color: #f1f5f9; }""")
        # новое выделение
        button.setStyleSheet("""QPushButton {
            border: none; background: transparent; color: #1f2937;
            padding-bottom: 4px; padding-left: 10px; text-align: left;
            border-bottom: 3px solid #3b82f6;
        }""")
        self.active_element_inner = button
        self.refresh_list(51)
        self.refresh_list(52)

    def set_value_prop_active(self, button):
        if self.active_property_inner:
                self.active_property_inner.setStyleSheet("""QPushButton {
                    border: none; background: transparent; color: #1f2937;
                    padding-bottom: 4px; padding-left: 10px; text-align: left;
                    border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                }
                QPushButton:hover { background-color: #f1f5f9; }""")
        button.setStyleSheet("""QPushButton {
                border: none; background: transparent; color: #1f2937;
                padding-bottom: 4px; padding-left: 10px; text-align: left;
                border-bottom: 3px solid #3b82f6;
            }""")
        self.active_property_inner = button
        self.refresh_list(52)

    def set_unsigned_prop_active(self, button):
        if self.active_property_unsigned:
            self.active_property_unsigned.setStyleSheet("""QPushButton {
                    border: none;
                    background: transparent;
                    color: #1e40af;
                    padding: 2px 0;
                    
                    border-bottom: 2px solid rgba(148, 163, 184, 0.5);
                }
                QPushButton:hover { background-color: #f1f5f9; }""")
        button.setStyleSheet("""QPushButton {
                    border: none;
                    background: transparent;
                    color: #1e40af;
                    padding: 2px 0;
                    
                    border-bottom: 3px solid #3b82f6;
                }""")
        self.active_property_unsigned = button
        self.refresh_list(61)
        

    def on_unsigned_prop_clicked(self):
        button = self.sender()
        self.set_unsigned_prop_active(button)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Классификация химических элементов")
        self.setMinimumSize(720, 520)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout(self)

        self.stack = QStackedWidget()

        # создаём страницы
        self.login_page = ClassificationLoginWindow(self.stack)
        self.db_page = DataBaseWindow(self.stack)
        self.class_page = ClassWindow(self.stack)
        self.res_page = ResultWindow(self.stack)
        self.spec_page = SpecialWindow(self.stack)

        #сигналы
        self.spec_page.update_table_data_signal.connect(self.db_page.update_scroll)
        self.spec_page.update_class_table_signal.connect(self.class_page.update_class_table)

        # добавляем в стек
        self.stack.addWidget(self.login_page)  # index 0
        self.stack.addWidget(self.db_page) #1
        self.stack.addWidget(self.class_page)      #2
        self.stack.addWidget(self.res_page)#3
        self.stack.addWidget(self.spec_page)#4


        layout.addWidget(self.stack)




if __name__ == "__main__":
    database.start()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    database.stop()
