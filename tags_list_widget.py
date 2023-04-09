from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton
import sys
import os
import csv


class tags_list_widget(QWidget):
    def __init__(self, Development):
        super().__init__()

        self.setWindowTitle("Выбор файла с именами тэгов")
        self.setFont(QFont("Times", 18))

        # Добавление логотипа главному окну
        self.setWindowIcon(QIcon("resources/logo_Extremum.png"))

        # Флаг, который задает окно поверх всех окон
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.Development = Development

        self.config = "Tags"
        self.project_names = []

        self.gb = QGroupBox(self)
        self.gb.setGeometry(3, 3, self.width() - 10, self.height() - 10)

        self.table = QTableWidget(self.gb)
        self.table_hh = self.table.horizontalHeader()
        self.table_vh = self.table.verticalHeader()

        self.button_accept = QPushButton("Открыть", self.gb)
        self.button_cancel = QPushButton("Отмена", self.gb)

        self.project_name = ""

        self.read_project_names()
        self.init_setup_table()
        self.init_setup_buttons()
        self.fill_project_names_table()

        self.setGeometry(int((self.Development.width()-400)/2), int((self.Development.height()-450)/2), 400, 450)

    def set_config(self, config_path):
        self.config = config_path

    def init_setup_table(self):
        self.table.setRowCount(len(self.project_names))
        self.table.setColumnCount(1)
        self.table.setGeometry(5, 10, self.gb.width() - 10, self.gb.height() - 20 - 55)
        self.table_hh.setDefaultSectionSize(self.gb.width() - 50)
        self.table_vh.setDefaultSectionSize(50)
        self.table.setHorizontalHeaderLabels(["Выберите файл"])

    def init_setup_buttons(self):
        self.button_accept.clicked.connect(self.slot_button_accept)
        self.button_cancel.clicked.connect(self.slot_button_cancel)

    def read_project_names(self):
        for file in os.listdir(self.config):
            self.project_names.append(file)

    def fill_project_names_table(self):
        for i in range(self.table.rowCount()):
            self.table.setItem(i, 0, QTableWidgetItem(self.project_names[i]))
            self.table.item(i, 0).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

    def set_tab(self, tab):
        self.tab = tab

    def slot_button_accept(self):
        tab = self.table.selectedItems()

        if (len(tab) != 0):
            self.filename = tab[0].text()

            # Имена тэгов
            self.Development.tag_names = []
            # Пути в OPC каждого тэга
            self.Development.tag_paths = []

            self.filename = "Tags/" + self.filename

            with open(self.filename) as r_file:
                file_reader = csv.reader(r_file, delimiter=",")
                count = 0
                for row in file_reader:
                    self.Development.tag_names.append(row[0])
                    self.Development.tag_paths.append(row[1])
                    count += 1
                for widget in self.Development.widget_list:
                    try:
                        for comBox in widget.qcomboBoxList:
                            comBox.clear()
                            comBox.addItems(self.Development.tag_names)
                    except:
                        pass
                print(f'Всего в файле {count} строк с данными.')
                print(self.Development.tag_paths)

            self.close()

    def slot_button_cancel(self):
        self.close_widget()

    def close_widget(self):
        self.close()

    def resizeEvent(self, a0):
        self.gb.resize(self.width() - 10, self.height() - 10)
        self.table.resize(self.gb.width() - 10, self.gb.height() - 10 - 55)
        self.table_hh.setDefaultSectionSize(self.width() - 20)

        self.button_cancel.setGeometry(5, self.table.y() + self.table.height() + 5, 150, 45)
        self.button_accept.setGeometry(self.gb.width() - 150 - 5, self.table.y() + self.table.height() + 5, 150, 45)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dl = tags_list_widget(1)
    dl.show()
    sys.exit(app.exec_())