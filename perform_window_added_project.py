
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QAction, QPushButton
from PyQt5.QtCore import Qt , QTimer

import sys
import os



class added_project_widget(QWidget):

    def __init__(self, parent):
        super().__init__()
        
        self.setWindowTitle("Добавление Процедур")
        self.setFont(QFont("Times", 12))
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon("resources/logo_Extremum.png"))

        self.parent = parent

        self.config = "Procedures"
        self.project_names = []
        self.gb = QGroupBox(self) 
        #self.gb.setGeometry(3,3,self.width() - 10, self.height() -10)
        self.main_vbox = QVBoxLayout() 

        self.hbox = QHBoxLayout() 
        self.table      = QTableWidget()
        self.table_hh   = self.table.horizontalHeader()
        self.table_vh   = self.table.verticalHeader()
        self.table_hh.setFont(QFont("Times", 14))
        self.table_vh.setVisible(False)
        self.hbox.addWidget(self.table)

        self.hbox_buttons = QHBoxLayout()
        self.button_accept = QPushButton("Добавить")
        self.button_accept.clicked.connect(self.slot_button_accept)

        self.hbox_buttons.addWidget(self.button_accept, 1)

        self.main_vbox.addLayout(self.hbox,10)
        self.main_vbox.addLayout(self.hbox_buttons,1)

        self.gb.setLayout(self.main_vbox)

        self.project_name = ""

        self.read_project_names()
        self.init_setup_table()
        self.fill_project_names_table()

        self.setFixedSize(400, 450)
        self.move(QDesktopWidget().availableGeometry().center().x() - int(self.width()/2), QDesktopWidget().availableGeometry().center().y() - int(self.height()/2))

    def set_config(self, config_path):
        self.config = config_path
        # self.read_project_names()
        # self.init_setup_table()
        # self.fill_project_names_table()

    def init_setup_table(self):
        self.table.setRowCount(len(self.project_names))
        self.table.setColumnCount(1)
        # self.table.setGeometry(5,10,self.gb.width() - 10 , self.gb.height() - 20 - 55)
        # self.table_hh.setDefaultSectionSize(self.gb.width() - 50)
        self.table.resize(self.gb.width() - 10, self.gb.height() - 10 - 55)
        self.table_hh.setDefaultSectionSize(self.width() - 20)
        self.table_vh.setDefaultSectionSize(50)
        self.table.setHorizontalHeaderLabels(["Выберите процедуры"])
        self.resize(400, 450)

    def read_project_names(self):
        # with open(self.config) as file:
        #     for row in file:
        #         self.project_names.append(row.replace("\n" , ""))
        self.project_names = list()
        for file in os.listdir(self.config):
            self.project_names.append(file.split('.')[0])

    def fill_project_names_table(self):
        for i in range(self.table.rowCount()):
            self.table.setItem(i,0, QTableWidgetItem(self.project_names[i]))
            self.table.item(i,0).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.table.item(i,0).setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)


    def set_tab(self, tab):
        self.tab = tab

    def corrected_project(self, project_name):
        filepath = 'Procedures' + '/' + project_name + '.txt'
        is_corrected = True
        with open(filepath, "r") as f:
            lines = f.readlines()
            line = lines[0]
            ind = 0
            while line != 'tags\n':
                if line == 'begin\n':
                    ind += 3
                elif line == 'operation\n':
                    if 'None' in lines[ind+3][1:-2].split(', '):
                        is_corrected = False
                        break
                    ind += 5
                elif line == 'condition\n':
                    if  'None' in lines[ind+3][1:-2].split(', '):
                        is_corrected = False
                        break
                    ind += 6
                elif line == 'end\n':
                    ind += 3
                line = lines[ind]
        return is_corrected 

    def slot_button_accept(self):
        tabs = self.table.selectedItems()
        if(len(tabs) != 0):
            for tab in tabs:
                if tab.text() not in self.parent.project_list_widget.project_names and tab.text() != '':
                    if self.corrected_project(tab.text()):
                        self.parent.project_list_widget.project_names.append(tab.text().split('.')[0])
                        #tab.setBackground(Qt.green)
                        self.parent.project_list_widget.fill_project_names_table()
                    else:
                        print('некорректная процедура')
                        QMessageBox.critical(self, "Ошибка загрузки", f"Загружаемая процедуры {tab.text()} некорректна для исполнения", QMessageBox.Ok)

    def slot_button_cancel(self):
        self.close()

    def showEvent(self, a0: QtGui.QShowEvent):
        self.table.clear()
        self.read_project_names()
        self.init_setup_table()
        self.fill_project_names_table()


    def resizeEvent(self, a0):
        self.gb.resize(self.width() - 10, self.height() - 10)
        self.table.resize(self.gb.width() - 10, self.gb.height() - 10 - 55)
        self.table_hh.setDefaultSectionSize(self.width() - 20)

        #self.button_cancel.setGeometry(5 , self.table.y() + self.table.height() + 5, 150 , 45)
        self.button_accept.setGeometry(self.gb.width() - 150 - 5, self.table.y() + self.table.height() + 5, 150 ,45)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dl = added_project_widget(1)
    dl.show()
    sys.exit(app.exec_())