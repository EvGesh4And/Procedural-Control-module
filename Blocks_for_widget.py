from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui, QtTest
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QObject
import sys

"""
Файл condition.py является частью модуля Proc.
Описание элемента блок-схемы Начало
Отображает название элемента, которое пользователь вводит на вкладке Основное Окна свойств блока
"""


class Condition(QWidget):
    def __init__(self, parent=None):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        # Сын
        self.son = None

        # Отец
        self.father = None

        # Индикатор выполнения всех условий
        self.indicator_condition = False

        self.active = False
        self.parent = parent

        self.font = QFont('Times', 12)
        self.setWindowTitle("Condition")
        self.setFixedSize(375, 260)
        self.setFont(self.font)
        self.condition_values = []
        self.condition_signs = []
        self.condition_tags = []
        self.comment = ''
        self.name_block = ''

        self.drawLine = None

        #self.initUi()


    def initUi(self):
        ## Фон
        self.pic = QLabel("Condition", self)
        self.pic.setPixmap(QtGui.QPixmap("resources/Condition.png"))
        self.pic.setObjectName('Pic')

        self.mainBox = QVBoxLayout(self)

        # Layout Названия блока
        self.Name_Label_box = QHBoxLayout()
        self.Name_Label_box.addStretch(1)
        self.Name_label = QLabel(self)
        self.Name_label.setText(self.name_block)
        self.Name_label.setAlignment(Qt.AlignCenter)
        self.Name_label_font = QFont('Times', 10)
        self.Name_label.setFont(self.Name_label_font)
        self.Name_Label_box.addWidget(self.Name_label)
        self.Name_Label_box.addStretch(1)
        self.Name_Label_box.setStretch(1, 4)

        # Layout Таблицы задания значений
        self.table_box = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table_hh = self.table.horizontalHeader()
        self.table_vh = self.table.verticalHeader()
        self.table_vh.setDefaultSectionSize(8)
        self.table_vh.setVisible(False)
        #self.table_hh.hide()
        self.table_hh.setSectionResizeMode(QHeaderView.Stretch)
        self.table_hh.setSectionResizeMode(0, 1)
        self.table_hh.setSectionResizeMode(1, 1)
        self.table_hh.setSectionResizeMode(2, 4)
        self.table_hh.setSectionResizeMode(3, 1)
        self.table.setHorizontalHeaderLabels(['Тег', 'Тек. знач.', '', 'Условие'])
        
        for i in range(len(self.condition_tags)):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)

            self.table.setItem(i, 0, QTableWidgetItem(self.condition_tags[i]))

            self.table.setItem(i, 1, QTableWidgetItem())

            self.table.setItem(i, 2, QTableWidgetItem())

            self.equally_label = QLabel(self.condition_signs[i])
            self.equally_label.setAlignment(Qt.AlignCenter)
            # self.equally_label.setFont(QFont('Times', 10))
            self.table.setCellWidget(i, 2, self.equally_label)

            self.table.setItem(i, 3, QTableWidgetItem(str(self.condition_values[i])))

            self.table.item(i,0).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.table.item(i,1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.table.item(i,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.table.item(i,3).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

            self.table.item(i,0).setFlags(Qt.ItemIsEnabled)
            self.table.item(i,1).setFlags(Qt.ItemIsEnabled)
            self.table.item(i,2).setFlags(Qt.ItemIsEnabled)
            self.table.item(i,3).setFlags(Qt.ItemIsEnabled)

        self.table_box.addWidget(self.table)

        # Помещение всех Layout в главный с коэффициентами растяжения
        self.mainBox.addLayout(self.Name_Label_box)
        self.mainBox.addLayout(self.table_box)

        self.mainBox.addStretch(1)
        self.mainBox.setContentsMargins(15, 25, 15, 15)

    def recolor_border(self, size, color):
        self.setStyleSheet(" #Pic {" + f"border: {size}px solid;" + f" border-color:{color};" + "} ")

    def execute_block(self):
        print('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

        if self.comment != '':
            self.parent.parent.action_widget.addAction(f'Процедура "{self.parent.project_name}": '+f'{self.comment}')

        self.indicator_condition = False

        while not self.indicator_condition:
            self.actual_value()
            QtTest.QTest.qWait(500)


    def actual_value(self):
        # Предполагаем, что все верны, если какое-то условие неверно - то будет изменение
        self.indicator_condition = True
        for i in range(len(self.condition_tags)):
            if not self.parent.pause.is_set():
                self.recolor_border(4, 'yellow')
                self.parent.pause.wait()
                self.recolor_border(4, 'green')

            value = float(self.parent.parent.parent.opc_client.get_values([self.parent.dict_nods[self.condition_tags[i]]])[0])
            self.table.setItem(i, 1, QTableWidgetItem(str(value)))
            self.table.item(i, 1).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.table.item(i, 1).setFlags(Qt.ItemIsEnabled)

            if self.condition_signs[i] == '>':
                if value <= float(self.condition_values[i]):
                    self.indicator_condition = False
            elif self.condition_signs[i] == '<':
                if value >= float(self.condition_values[i]):
                    self.indicator_condition = False
            elif self.condition_signs[i] == 'равно':
                if value != float(self.condition_values[i]):
                    self.indicator_condition = False

    def resizeEvent(self, a0):
        """
        Метод адаптации размеров элемента
        :param a0:
        :return:
        """
        self.pic.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        print(f" w = {self.width()} | h = {self.height()}")


class Operation(QWidget):
    def __init__(self, parent=None):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        # Сын
        self.son = None
        # Отец
        self.father = None

        self.active = False
        self.parent = parent

        self.font = QFont('Times', 12)
        self.setWindowTitle("Operation")
        self.setFixedSize(375, 260)
        self.setFont(self.font)
        self.condition_values = []
        self.condition_tags = []
        self.comment = ''
        self.name_block = ''

        self.drawLine = None

        #self.initUi()

    def initUi(self):
        ## Фон
        self.pic = QLabel("Operation", self)
        self.pic.setPixmap(QtGui.QPixmap("resources/Operation.png"))
        self.pic.setObjectName('Pic')
        #self.pic.setPixmap(PyQt5.QtGui.QPixmap("Operation.png"))

        self.mainBox = QVBoxLayout(self)

        # Layout Названия блока
        self.Name_Label_box = QHBoxLayout()
        self.Name_Label_box.addStretch(1)
        self.Name_label = QLabel(self)
        self.Name_label.setText(self.name_block)
        self.Name_label.setAlignment(Qt.AlignCenter)
        self.Name_label_font = QFont('Times', 10)
        self.Name_label.setFont(self.Name_label_font)
        self.Name_Label_box.addWidget(self.Name_label)
        self.Name_Label_box.addStretch(1)
        self.Name_Label_box.setStretch(1, 4)

        # Layout Таблицы задания значений
        self.table_box = QHBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table_hh = self.table.horizontalHeader()
        self.table_vh = self.table.verticalHeader()
        self.table_vh.setDefaultSectionSize(8)
        self.table_vh.setVisible(False)
        #self.table_hh.hide()
        self.table_hh.setSectionResizeMode(QHeaderView.Stretch)
        self.table_hh.setSectionResizeMode(0, 1)
        self.table_hh.setSectionResizeMode(1, 4)
        self.table_hh.setSectionResizeMode(2, 1)
        self.table.setHorizontalHeaderLabels(['Тег', '', 'Уставка'])
        
        for i in range(len(self.condition_tags)):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)

            self.table.setItem(i, 0, QTableWidgetItem(self.condition_tags[i]))

            self.table.setItem(i, 1, QTableWidgetItem())
            self.equally_label = QLabel('=')
            self.equally_label.setAlignment(Qt.AlignCenter)
            self.equally_label.setFont(QFont('Times', 14))
            self.table.setCellWidget(i, 1, self.equally_label)

            self.table.setItem(i, 2, QTableWidgetItem(str(self.condition_values[i])))

            self.table.item(i,0).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.table.item(i,2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.table.item(i,0).setFlags(Qt.ItemIsEnabled)
            self.table.item(i,2).setFlags(Qt.ItemIsEnabled)
        self.table_box.addWidget(self.table)

        # Помещение всех Layout в главный с коэффициентами растяжения
        self.mainBox.addLayout(self.Name_Label_box)
        self.mainBox.addLayout(self.table_box)

        self.mainBox.addStretch(1)
        self.mainBox.setContentsMargins(15, 25, 15, 15)

    def recolor_border(self, size, color):
        self.setStyleSheet(" #Pic {" + f"border: {size}px solid;" + f" border-color:{color};" + "} ")

    def execute_block(self):
        print('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

        if self.comment != '':
            self.parent.parent.action_widget.addAction(f'Процедура "{self.parent.project_name}": '+f'{self.comment}')

        self.actual_value()
        QtTest.QTest.qWait(3000)

    def actual_value(self):
        try:
            for i in range(len(self.condition_tags)):
                if not self.parent.pause.is_set():
                    self.recolor_border(4, 'yellow')
                    self.parent.pause.wait()
                    self.recolor_border(4, 'green')
                self.parent.parent.parent.opc_client.set_values([self.parent.dict_nods[self.condition_tags[i]]], [float(self.condition_values[i])])
        except:
            QMessageBox.critical(self, "Ошибка команды", f"В процедуре {tab.text()} произошла ошибка при подаче команды по OPC", QMessageBox.Ok)

    def resizeEvent(self, a0):
        """
        Метод адаптации размеров элемента
        :param a0:
        :return:
        """
        self.pic.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        print(f" w = {self.width()} | h = {self.height()}")


class Begin(QWidget):
    def __init__(self, parent=None):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        # Сын
        self.son = None

        self.active = False
        self.parent = parent

        self.font = QFont('Times', 12)
        self.setWindowTitle("Begin")
        self.setFixedSize(375, 260)
        self.setFont(self.font)
        self.comment = ''
        self.name_block = ''

        self.drawLine = None
        #self.initUi()


    def initUi(self):
        ## Фон
        self.pic = QLabel("Begin", self)
        self.pic.setPixmap(QtGui.QPixmap("resources/Begin.png"))
        self.pic.setObjectName('Pic')

        self.mainBox = QVBoxLayout(self)

        # Layout Названия блока
        self.Name_Label_box = QHBoxLayout()
        self.Name_Label_box.addStretch(1)
        self.Name_label = QLabel(self)
        self.Name_label.setText(self.name_block)
        self.Name_label.setAlignment(Qt.AlignCenter)
        self.Name_label.setFont(QFont('Times', 10))
        self.Name_Label_box.addWidget(self.Name_label)
        self.Name_Label_box.addStretch(1)
        self.Name_Label_box.setStretch(1, 4)

        # Layout комментария QLabel
        self.comment_label_box = QHBoxLayout()
        self.comment_label = QLabel(self) 
        self.comment_label.setText(self.comment)
        self.comment_label.setWordWrap(True)
        self.comment_label.setAlignment(Qt.AlignCenter)
        self.comment_label_font = QFont('Times', 10)
        self.comment_label.setFont(self.comment_label_font)
        self.comment_label_box.addWidget(self.comment_label)

        # Помещение всех Layout в главный с коэффициентами растяжения
        self.mainBox.addLayout(self.Name_Label_box)
        self.mainBox.addStretch(1)
        self.mainBox.addLayout(self.comment_label_box)
        self.mainBox.addStretch(1)
        self.mainBox.setContentsMargins(15, 25, 15, 15)

    def recolor_border(self, size, color):
        self.setStyleSheet(" #Pic {" + f"border: {size}px solid;" + f" border-color:{color};" + "} ")

    def execute_block(self):
        print('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
        if self.comment != '':
            self.parent.parent.action_widget.addAction(f'Процедура "{self.parent.project_name}": '+f'{self.comment}')
        QtTest.QTest.qWait(5000)

    def resizeEvent(self, a0):
        """
        Метод адаптации размеров элемента
        :param a0:
        :return:
        """
        self.pic.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        print(f" w = {self.width()} | h = {self.height()}")

class Communicate(QObject):
    c = pyqtSignal()

class End(QWidget):
    def __init__(self, parent=None):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        # Сын
        self.son = None

        # Сигнал
        self.signal = Communicate()
        self.signal.c.connect(self.accept)

        self.active = False
        self.parent = parent

        self.font = QFont('Times', 12)
        self.setWindowTitle("End")
        self.setFixedSize(375, 260)
        self.setFont(self.font)
        self.comment = ''
        self.name_block = ''

        self.drawLine = None
        #self.initUi()


    def initUi(self):
        ## Фон
        self.pic = QLabel("End", self)
        self.pic.setPixmap(QtGui.QPixmap("resources/End.png"))
        self.pic.setObjectName('Pic')

        self.mainBox = QVBoxLayout(self)

        # Layout Названия блока
        self.Name_Label_box = QHBoxLayout()
        self.Name_Label_box.addStretch(1)
        self.Name_label = QLabel(self)
        self.Name_label.setText(self.name_block)
        self.Name_label.setAlignment(Qt.AlignCenter)
        self.Name_label.setFont(QFont('Times', 10))
        self.Name_Label_box.addWidget(self.Name_label)
        self.Name_Label_box.addStretch(1)
        self.Name_Label_box.setStretch(1, 4)


        # Layout комментария QLabel
        self.comment_label_box = QHBoxLayout()
        self.comment_label = QLabel(self) 
        self.comment_label.setText(self.comment)
        self.comment_label.setWordWrap(True)
        self.comment_label.setAlignment(Qt.AlignCenter)
        self.comment_label_font = QFont('Times', 10)
        self.comment_label.setFont(self.comment_label_font)
        self.comment_label_box.addWidget(self.comment_label)


        # Помещение всех Layout в главный с коэффициентами растяжения
        self.mainBox.addLayout(self.Name_Label_box)
        self.mainBox.addStretch(1)
        self.mainBox.addLayout(self.comment_label_box)
        self.mainBox.addStretch(1)
        self.mainBox.setContentsMargins(15, 25, 15, 15)

    def recolor_border(self, size, color):
        self.setStyleSheet(" #Pic {" + f"border: {size}px solid;" + f" border-color:{color};" + "} ")

    def execute_block(self):
        print('(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')

        if self.comment != '':
            self.parent.parent.action_widget.addAction(f'Процедура "{self.parent.project_name}": ' + f'{self.comment}')

        self.parent.parent.action_widget.addAction(f'Процедура "{self.parent.project_name}" успешно завершена')
        self.parent.item.setBackground(QColor(0, 255, 255))

    def accept(self):
        msg = QMessageBox()
        msg.setWindowTitle("Выполнение процедуры")
        msg.setText(f'Процедура "{self.parent.project_name}" успешно завершена')
        msg.setWindowModality(QtCore.Qt.NonModal)
        # msg.exec()

    def resizeEvent(self, a0):
        """
        Метод адаптации размеров элемента
        :param a0:
        :return:
        """
        self.pic.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        print(f" w = {self.width()} | h = {self.height()}")

if __name__ == "__main__":
    # QtCore.QCoreApplication.addLibraryPath("./")
    app = QApplication(sys.argv)
    window = Condition()
    window.show()
    app.exec_()

