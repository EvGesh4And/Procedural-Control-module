from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from editor import *

"""
Файл properties.py является частью модуля Proc.
Окно Свойства блока имеет две вкладки: Основное и Прочее
используя данное окно, пользователь может менять настройки (свойства) блоков
Вызывается по двойному нажатию кнопки мыши на блок
"""

class Properties(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.element    = "element"
        self.font       = QFont('Times', 11)
        self.tab_widget = QTabWidget(self)
        self.tab1       = Basic()
        self.tab2       = Other()
        self.save       = QPushButton("Сохранить настройки", self)
        self.filename   = ""


        self.save.clicked.connect(self.save_settings)

        self.tab_widget.resize(800, 800)
        self.tab_widget.addTab(self.tab1, "Основное")
        self.tab_widget.addTab(self.tab2, "Прочее")
        # self.tab_widget.setStyleSheet('''
        #      QTabWidget {
        #          background: grey;
        #      }
        #  ''')
        self.setWindowTitle("Свойства блока")
        self.setGeometry(2100, 400, 760, 645)
        self.save.setGeometry(30, 580, 700, 40)
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setFont(self.font)
        self.tab1.setObjectName("Basic")
        self.tab1.setStyleSheet("#Basic{border-image:url(grey.jpg)}")
        self.tab1.palette = QPalette()
        self.tab1.palette.setBrush(QPalette.Background, QBrush(QPixmap("./grey.jpg")))
        self.tab1.setPalette(self.tab1.palette)
       # self.read_geometry()
        self.setFixedHeight(645)
        self.setFixedWidth(760)
        self.save.setStyleSheet("background-color : rgb(205,209,209)")


    def set_var_filename(self, filename):
        """
        Метод для получения имени файла, выбранного пользователем для выгрузки переменных из него
        :param filename: имя файла
        :return:
        """
        self.filename = filename
        print("-???-")
        self.tab1.set_var_filename(filename)

    def set_element(self, element):
        """
        Метод для назначения элемента
        :param element:
        :return:
        """
        self.element = element

    def save_element_table(self):
         rowcount = self.tab1.table_expression.rowCount()
         self.element.table.setRowCount(rowcount)

         for i in range(rowcount):
             text = self.tab1.table_expression.item(i, 0).text()
             self.element.table.setItem(i, 0, QTableWidgetItem(text))

    def save_settings(self):
        self.save_element_table()
        self.fill_name()
        self.read_geometry()

    def fill_name(self):
        name = self.tab1.line.text()
        self.element.name.setText(name)

    def read_geometry(self):
        number  = self.tab2.line1.text()
        number2 = self.tab2.line2.text()
        number3 = self.tab2.line3.text()
        number4 = self.tab2.line4.text()
        try:
            number  = int(number)
            number2 = int(number2)
            number3 = int(number3)
            number4 = int(number4)
        except Exception:
            QMessageBox.critical(self, 'Ошибка', 'Заполните все поля числовыми данными')
            pass
        if number > 3300:
            QMessageBox.warning(self, 'Предупреждение', 'Элемент будет находиться за пределами рабочей области')
        elif number2 > 1700:
            QMessageBox.warning(self, 'Предупреждение', 'Элемент будет находиться за пределами рабочей области')
        else:
            pass

        self.element.setGeometry(number, number2, number3, number4)

class Basic(QtWidgets.QWidget):
    def __init__(self, parent = None):
        """
        Описание вкладки Основное, где пользователь может добавить название блока,
        видеть в таблице выражений уже существующие выражения, добавить новое или удалить ненужное,
        нажав соответствующие кнопки
        :param parent:родительский виджет - Properties
        """
        super().__init__(parent)

        self.parent     = parent
        self.font       = QFont('Times', 11)
        self.line       = QLineEdit(self)
        self.label_name = QLabel("Название блока:", self)
        self.editor     = Editor()
        self.item       = ""


        self.setFont(self.font)
        self.setGeometry(1100, 600, 760, 1000)
        self.label_name.setGeometry(20, 5, 200, 50)
        self.line.setGeometry(205, 15, 525, 35)
      #  self.line.setReadOnly(True)

     #   self.label_table = QLabel("Таблица выражений", self)
     #   self.label_table.setGeometry(270, 80, 300, 50)

   #     self.table_expression = QTextEdit(self)
    #    self.table_expression.setReadOnly(True)
   #     self.table_expression.setGeometry(30, 140, 700, 300)

        self.table_expression = QTableWidget(0, 1, self)
        self.rowcount         = self.table_expression.rowCount
        self.vh               = self.table_expression.verticalHeader()
        self.hh               = self.table_expression.horizontalHeader()
        self.add_expr         = QPushButton("Добавить выражение", self)
        self.ed_expr          = QPushButton("Редактировать выражение", self)
        self.del_expr         = QPushButton("Удалить выражение", self)
        self.filename         = ""

       # self.add_expr.setStyleSheet("background-color : rgb(225,234,235)")
        self.table_expression.setGeometry(30, 80, 700, 300)
        self.table_expression.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.vh.setDefaultSectionSize(30)
        self.table_expression.setHorizontalHeaderLabels(['Таблица выражений'])
        self.hh.setDefaultSectionSize(700)
        self.add_expr.setGeometry(30, 395, 700, 40)
        self.add_expr.clicked.connect(self.Add_Expr)
        self.ed_expr.clicked.connect(self.slot_button_editor_show)
        self.ed_expr.setGeometry(30, 445, 700, 40)
        self.del_expr.setGeometry(30, 495, 700, 40)
        self.del_expr.clicked.connect(self.Del_Expr)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(QPixmap("./grey.jpg")))
        self.setPalette(self.palette)


    def set_var_filename(self, filename):
        """
        Метод для получения имени файла, который пользователь выбрал для получения переменных
        :param filename:
        :return:
        """
        print("-??-")
        self.filename = filename
        self.editor.set_var_filename(filename)

    def Add_Expr(self):
        """
        Метод, который создает новую строку в редакторе выражений
        вызывается по кнопке "Добавить выражение"
        :return:
        """
        rowPosition = self.table_expression.rowCount()
        self.table_expression.insertRow(rowPosition)
        self.table_expression.setItem(0,rowPosition,QTableWidgetItem(""))
        # self.table_expression.setItem(rowPosition)
     #   self.editor.show()

    # def Ed_Expr(self):
    #     """
    #     Метод открывает редактор выражений, чтобы пользователь мог внести изменения
    #     вызывается по кнопке "Редактировать выражение"
    #     :return:
    #     """
    #     self.editor.show()

    def slot_button_editor_show(self):
        """
        Метод выделения строки в таблице

        :return:
        """
        buff = self.table_expression.selectedItems()
        if(len(buff) != 0):
            self.item = buff[0]
            print("-?-")

        self.editor.show()
        self.editor.set_item_edit(self.item)

    def Del_Expr(self):
        """
        Метод удаления строки в таблице Выражений
        :return:
        """
        buff = self.table_expression.selectedIndexes()
        if(len(buff) != 0):
            self.item = buff[0]
        self.table_expression.removeRow(buff[0].row())

class Other(QtWidgets.QWidget):
    """
    Метод определяет класс Прочее, который используется как одна из вкладок, где пользователь может задать
    геометрические параметры блока: положение блока по осям X и Y,
    а также ширину и высоту блока
    """
    def __init__(self):
        super().__init__()
        self.font = QFont('Times', 11)
        self.setFont(self.font)
        self.font1 = QFont('Times', 11)
        self.setGeometry(1100, 600, 800, 1000)
        self.label1  = QLabel("Геометрические параметры блока:", self)
        self.label_x = QLabel("Положение блока (ось X):", self)
        self.label_y = QLabel("Положение блока (ось Y):", self)
        self.line1   = QLineEdit(self)
        self.line2   = QLineEdit(self)
        self.label_w = QLabel("Ширина блока:", self)
        self.label_h = QLabel("Высота блока:", self)
        self.line3   = QLineEdit(self)
        self.line4   = QLineEdit(self)

        self.label1.setGeometry(20, -8, 500, 50)
        self.label_x.setGeometry(20, 35, 400, 50)
        self.label_y.setGeometry(20, 95, 400, 50)
        self.line1.setGeometry(295, 45, 300, 35)
        self.line2.setGeometry(295, 105, 300, 35)
        self.label_w.setGeometry(20, 150, 400, 50)
        self.label_h.setGeometry(20, 210, 400, 50)
        self.line3.setGeometry(295, 160, 300, 35)
        self.line4.setGeometry(295, 220, 300, 35)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = Properties()
    myWidget.show()
    myWidget2 = Basic()
    myWidget2.show()
    # myWidget2 = Basic()
    # myWidget2.show()
    # myWidget3 = Other()
    # myWidget3.show()
    sys.exit(app.exec_())
