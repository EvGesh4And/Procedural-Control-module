
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QAction, QPushButton
from PyQt5.QtCore import Qt , QTimer

import sys

from procedure_widget import Procedure_widget_scroll



class project_list_widget(QWidget):

    def __init__(self, parent):
        super().__init__()
        
        self.setWindowTitle("Открыть проект")
        self.setFont(QFont("Times", 14))

        self.parent = parent
        self.config = "Процедуры"
        self.project_names = []

        #self.setGeometry(0,0,370,115)
        self.gb = QGroupBox(self) 
        #self.gb.setGeometry(3,3,self.width() - 10, self.height() -10)
        self.main_vbox = QVBoxLayout() 

        self.hbox = QHBoxLayout() 
        self.table      = QTableWidget()
        # Единичный выбор
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_hh   = self.table.horizontalHeader()
        self.table_vh   = self.table.verticalHeader()
        self.table_vh.setVisible(False)
        self.hbox.addWidget(self.table)

        self.hbox_buttons = QHBoxLayout()
        self.button_accept = QPushButton("Добавить")
        self.button_cancel = QPushButton("Удалить")
        self.hbox_buttons.addWidget(self.button_accept, 1)
        self.hbox_buttons.addWidget(self.button_cancel, 1)

        self.main_vbox.addLayout(self.hbox,10)
        self.main_vbox.addLayout(self.hbox_buttons,1)

        self.gb.setLayout(self.main_vbox)

        self.project_name = ""
        #self.read_project_names()
        self.init_setup_table()
        self.init_setup_buttons()
        #self.fill_project_names_table()
        self.table.cellDoubleClicked.connect(self.cellDoubleClicked)


    def init_setup_table(self):
        self.table.setRowCount(len(self.project_names))
        self.table.setColumnCount(1)
        self.table.setGeometry(0,0,self.gb.width() - 30 , self.gb.height() - 30 - 55)
        self.table_hh.setDefaultSectionSize(self.gb.width() - 50)
        self.table_vh.setDefaultSectionSize(50)
        self.table.setHorizontalHeaderLabels(["Загруженные процедуры"])

    def init_setup_buttons(self):
        self.button_accept.clicked.connect(self.slot_button_accept)
        self.button_cancel.clicked.connect(self.slot_button_cancel)


    def fill_project_names_table(self):
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        self.table.setItem(rowPosition,0, QTableWidgetItem(self.project_names[-1]))
        self.table.item(rowPosition,0).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.table.item(rowPosition,0).setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)
        self.table.item(rowPosition,0).setFont(QFont('Times', 12))
            
    def slot_button_accept(self):
        print('accept')
        self.parent.added_project_wid.show()

    def slot_button_cancel(self):
        # Итемы процедур слева, которые хотим удалить
        items = self.table.selectedItems()

        # Список процедур, которые будут удалены слева
        del_projects = []

        # Удаление процедур слева
        for item in items:
            position = item.row()
            if item.text() in self.parent.right_window.dict_name_open_procedures.keys():
                print('tuta')
                elem = self.parent.right_window.dict_name_open_procedures[item.text()].widget
                if position != -1 and (elem.status == 0 or elem.status == 3):
                    del_projects.append(item.text())
                    self.project_names.remove(item.text())
                    self.table.removeRow(position)
            else:
                del_projects.append(item.text())
                self.project_names.remove(item.text())
                self.table.removeRow(position)

        # Удаляем вкладки справа
        print(del_projects)

        for proc in del_projects:
            count = self.parent.right_window.tab_main.count()
            for pr in range(count):
                tabname = self.parent.right_window.tab_main.tabText(pr)
                if tabname == proc:
                    self.parent.right_window.dict_name_open_procedures.pop(tabname)
                    self.parent.right_window.tab_main.removeTab(pr)
                    pr = count + 1

    def close_widget(self):
        self.close()

    def resizeEvent(self, a0):
        self.gb.resize(self.width() - 20, self.height() - 20)
        self.table.resize(self.gb.width() - 20, self.gb.height() - 30 - 55)
        self.table_hh.setDefaultSectionSize(self.gb.width() - 20)

    def cellDoubleClicked(self, row, column):
        project_name = self.table.item(row, column).text()
        if project_name not in self.parent.right_window.dict_name_open_procedures.keys():
            scroll = Procedure_widget_scroll(self.parent.right_window, self.table.item(row, column))
            self.parent.right_window.dict_name_open_procedures[project_name] = scroll
            self.parent.right_window.tab_main.addTab(scroll, project_name)
            print('scroll.width(), scroll.height()', scroll.width(), scroll.height() )

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dl = project_list_widget(1)
    dl.show()
    sys.exit(app.exec_())