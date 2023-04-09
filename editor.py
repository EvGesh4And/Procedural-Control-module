from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from properties import *
import csv
"""
Файл editor.py является частью модуля Proc.
Редактор выражений, в котором пользователь может создать математическое выражение, используя доступные переменные,
операторы и функции. 
Содержит 
- окно, отображающее созданное выражение
- кнопки для сохранения изменений(ОК)
- выхода из редактора выражений без сохранения изменений 
- отмены предыдущего действия (Назад)
- кнопку помощи со справочной информацией (Справка)
- кнопку очистки окна выражений
- кнопки математических операторов
- окно, отображающее доступные переменные
- окно, отображающее функции
"""

class Editor(QtWidgets.QWidget):
    def __init__(self):
        """
        Метод определяет окно Редактора выражений
        """
        super().__init__()

        self.line       = QTextEdit(self)
        self.font       = QFont('Times', 14)
        self.ok         = QPushButton("OK", self)


        self.cancel         = QPushButton("Отмена", self)
        self.clear          = QPushButton("Очистить", self)
      #  self.delete     = QPushButton("Удалить", self)
        self.plus           = QPushButton("+", self)
        self.minus          = QPushButton("-", self)
        self.div            = QPushButton("/", self)
        self.mult           = QPushButton("*", self)
        self.equal          = QPushButton("=", self)
        self.greater        = QPushButton(">", self)
        self.less           = QPushButton("<", self)
        self.begbracket     = QPushButton("(", self)
        self.endbracket     = QPushButton(")", self)
        self.whspace        = QPushButton("Пробел", self)
        self.functions      = QTableWidget(7, 1, self)
        self.variables      = QTableWidget(0, 1, self)
        self.item           = ""
        self.filename       = ""
        self.add_var        = QPushButton("Добавить переменную", self)
        self.add_fun        = QPushButton("Добавить функцию", self)
        self.functions.font = QFont('Times', 14)
        self.palette        = QPalette()

        self.setWindowTitle("Редактор выражений")
        self.setGeometry(900, 500, 1170, 780)
        self.setFixedWidth(1170)
        self.setFixedHeight(780)
        self.setFont(self.font)
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("./blue.jpg")))
        self.setPalette(self.palette)
    #   line.setGeometry(100, 354, )
      #  self.ok.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        self.ok.setStyleSheet("background-color : white")
        self.cancel.setStyleSheet("background-color : lightGray")
        self.clear.setStyleSheet("background-color : lightGray")
        self.plus.setStyleSheet("background-color : white")
        self.minus.setStyleSheet("background-color : white")
        self.div.setStyleSheet("background-color : white")
        self.mult.setStyleSheet("background-color : white")
        self.equal.setStyleSheet("background-color : white")
        self.greater.setStyleSheet("background-color : white")
        self.less.setStyleSheet("background-color : white")
        self.begbracket.setStyleSheet("background-color : white")
        self.endbracket.setStyleSheet("background-color : white")
        self.whspace.setStyleSheet("background-color : white")
        self.add_var.setStyleSheet("background-color : white")
        self.add_fun.setStyleSheet("background-color : white")
        self.line.setMinimumWidth(50)
        self.line.setMinimumHeight(30)
        self.line.show()
        self.line.setGeometry(10, 10, 1000, 208)
        self.line.setReadOnly(True)

        self.ok.setGeometry(1030, 10, 130, 62)
        self.ok.clicked.connect(self.save_changes)

        self.cancel.setGeometry(1030, 80, 130, 65)
        self.cancel.clicked.connect(self.cancellation)

        self.clear.setGeometry(1030, 154, 130, 65)
        self.clear.clicked.connect(self.line.clear)

      #  self.delete.setGeometry(1030, 175, 130, 45)
       # self.delete.clicked.connect(self.delete)
      #  self.back = QPushButton("Назад", self)
      #  self.back.setGeometry(1030, 120, 115, 45)
      #  self.help = QPushButton("Справка", self)
      #  self.help.setGeometry(1030, 175, 115, 45)
      #  self.help.clicked.connect(self.helpp)


        self.plus.setGeometry(130, 230, 50, 50)
        self.plus.clicked.connect(self.pluss)

        self.minus.setGeometry(200, 230, 50, 50)
        self.minus.clicked.connect(self.minuss)

        self.div.setGeometry(270, 230, 50, 50)
        self.div.clicked.connect(self.divv)

        self.mult.setGeometry(340, 230, 50, 50)
        self.mult.clicked.connect(self.multt)

        self.equal.setGeometry(410, 230, 50, 50)
        self.equal.clicked.connect(self.equall)

        self.greater.setGeometry(480, 230, 50, 50)
        self.greater.clicked.connect(self.greaterr)

        self.less.setGeometry(550, 230, 50, 50)
        self.less.clicked.connect(self.lesss)

        self.begbracket.setGeometry(620, 230, 50, 50)
        self.begbracket.clicked.connect(self.begbrackett)

        self.endbracket.setGeometry(690, 230, 50, 50)
        self.endbracket.clicked.connect(self.endbrackett)

        self.whspace.setGeometry(760, 230, 120, 50)
        self.whspace.clicked.connect(self.whitespace)

        self.variables.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.hh         = self.variables.horizontalHeader()
        self.vh         = self.variables.verticalHeader()
        self.variables.setHorizontalHeaderLabels(['Переменные'])
        self.variables.setGeometry(15, 310, 565, 370)
        self.vh.setDefaultSectionSize(30)
        self.hh.setDefaultSectionSize(555)

        self.indexes = self.variables.selectionModel().selectedRows()
        for index in sorted(self.indexes):
            print('Row %d is selected' % index.row())

        self.functions.setHorizontalHeaderLabels(['Функции'])
        self.functions.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        rowPosition2 = self.functions.rowCount()
        self.functions.insertRow(rowPosition2)
        self.vh2 = self.functions.verticalHeader()
        self.vh2.setDefaultSectionSize(30)
        self.functions.setGeometry(595, 310, 565, 370)
        self.functions.setItem(0, 0, QTableWidgetItem("pow"))
        self.functions.setItem(1, 0, QTableWidgetItem("sqrt"))
        self.functions.setItem(2, 0, QTableWidgetItem("sin"))
        self.functions.setItem(3, 0, QTableWidgetItem("cos"))
        self.functions.setItem(4, 0, QTableWidgetItem("round"))
        self.hh2 = self.functions.horizontalHeader()
        self.hh2.setDefaultSectionSize(555)
        self.add_var.setGeometry(15, 700, 565, 40)
        self.add_var.clicked.connect(self.slot_add_var_clicked)
        self.add_fun.setGeometry(595, 700, 565, 40)
        self.add_fun.clicked.connect(self.slot_add_fun_clicked)

    def non_editable(self):
        """
        Метод, позволяющий сделать таблицу переменных нередактируемой
        :return:
        """
        print("+")
        rows = self.variables.rowCount()
        for i in range(rows):
            item = self.variables.item(i,0)
            item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
            # item.setFlags(item.flags() != QtCore.Qt.ItemIsEditable)

    def save_changes(self):
        """
        Метод сохранения внесенных пользователем изменений
        :return:
        """
        print("SAVE")
        text = self.line.toPlainText()
        with open('somefile.txt', 'a') as f:
            f.write(text)
        self.item.setText(text)
        print(text)

    def cancellation(self):
        """
        Метод, закрывающий окно Редактора выражений
        :return: закрытие окна
        """
        self.close()


    def helpp(self):
        """
        Метод, вызывающий справочное окно
        :return: открытие справочного окна
        """
        self.help = Help()
        self.help.show()

    def pluss(self):
        a = "+"
        self.line.insertPlainText(a)

    def minuss(self):
        a = "-"
        self.line.insertPlainText(a)

    def divv(self):
        a = "/"
        self.line.insertPlainText(a)

    def multt(self):
        a = "*"
        self.line.insertPlainText(a)

    def equall(self):
        a = "="
        self.line.insertPlainText(a)

    def greaterr(self):
        a = ">"
        self.line.insertPlainText(a)

    def lesss(self):
        a = "<"
        self.line.insertPlainText(a)

    def begbrackett(self):
        a = "("
        self.line.insertPlainText(a)

    def endbrackett(self):
        a = ")"
        self.line.insertPlainText(a)

    def whitespace(self):
        a = " "
        self.line.insertPlainText(a)

    def slot_add_fun_clicked(self):
        """
        Метод перенесения выделенной в таблице функции в окно Выражения
        :param index - выделенная строка (строки) таблицы functions
        :return:
        """
        index = self.functions.selectedItems()
        if(len(index) != 0):
            self.line.insertPlainText(index[0].text())

    def set_var_filename(self, filename):
        """
        Метод для получения имени файла, который пользователь выбрал для получения переменных
        :param filename:
        :return:
        """
        self.filename = filename
        self.fill_var_table()

    def fill_var_table(self):
        """
        Метод для считывания переменных из файла и заполнения ими таблицы переменных
        :return:
        """
        var = []
        with open(self.filename) as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            count = 0
            for row in file_reader:
                if count == 0:
                    print(row[0])
                    var = row
                else:
                    print(f'{row}')

                count += 1
            print(f'Всего в файле {count} строк с данными.')

        for i in range(len(var)):
            rowPosition = self.variables.rowCount()
            self.variables.insertRow(rowPosition)
            self.variables.setItem(i,0,QTableWidgetItem(var[i]))
        self.non_editable()

    def set_item_edit(self, item):
        """
        Метод ...
        :param item:
        :return:
        """
        self.item = item
        self.line.setText(item.text())

    def slot_add_var_clicked(self):
        """
        Метод перенесения выделенной в таблице функции в окно Выражения
        :param index - выделенная строка (строки) таблицы variables
        :return:
        """
        index = self.variables.selectedItems()
        if (len(index) != 0):
            self.line.insertPlainText(index[0].text())

          #  print(index[0].text())

    # def select(self):
    #     indexes = table.selectionModel().selectedRows()
    #     for index in sorted(indexes):
    #         print('Row %d is selected' % index.row())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = Editor()
    myWidget.show()
    sys.exit(app.exec_())
