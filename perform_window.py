from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import time
from datetime import datetime
from perform_project_list_widget import *
from perform_window_added_project import *
from procedure_widget import Procedure_widget_scroll
from Client_OPC import ClientApp
import threading


class Perform(QWidget):
    def __init__(self, parent = None):
        # Инициализация родительского класса
        super().__init__(parent)
        self.parent = parent
        self.move(0, 0)
        self.opc_client = None
        self.initUI()


    def initUI(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 5, 0, 0)
        self.project_list_widget = project_list_widget(self)
        self.project_list_widget.setFont(QFont("Times", 16))
        self.right_window = right_widget(self)
        hbox.addWidget(self.project_list_widget, 1)
        #hbox.setSpacing(0)
        hbox.addWidget(self.right_window, 5)
        self.setLayout(hbox)
        self.back = back(self)
        self.back.setGeometry(self.frameGeometry())
        self.opc_widget = Input_OPC_url_widget(self)
        self.added_project_wid = added_project_widget(self)


    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.back.move(0,0)
        self.back.resize(a0.size())
        pos = self.geometry().center() - self.opc_widget.rect().center()
        self.opc_widget.move(pos)


class right_widget(QWidget):
    def __init__(self, parent = None):
        # Инициализация родительского класса
        super().__init__()

        # Словарь открытых вкладок справа
        self.dict_name_open_procedures = {}

        # Словарь потоков
        self.dict_streams = {}

        # Родитель
        self.parent = parent

        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 5, 5, 5)
        self.hbox_buttons = QHBoxLayout()
        self.button_start = QPushButton('Пуск')
        self.button_start.setFont(QFont("Times", 16))
        self.button_pause = QPushButton('Пауза')
        self.button_pause.setFont(QFont("Times", 16))
        self.button_stop = QPushButton('Стоп')
        self.button_stop.setFont(QFont("Times", 16))
        self.hbox_buttons.addStretch(1)
        self.hbox_buttons.addWidget(self.button_start, 1)
        self.hbox_buttons.addStretch(1)
        self.hbox_buttons.addWidget(self.button_pause, 1)
        self.hbox_buttons.addStretch(1)
        self.hbox_buttons.addWidget(self.button_stop, 1)
        self.hbox_buttons.addStretch(1)
        # self.vbox.addLayout(self.hbox_buttons, 1)

        self.tab_main = QTabWidget(self)
        self.tab_main.setObjectName('tab_main')
        self.tab_main.setStyleSheet(qss)
        self.vbox.addWidget(self.tab_main, 10)

        self.vbox.addLayout(self.hbox_buttons, 1)
        
        self.action_widget = action_widget()
        self.vbox.addWidget(self.action_widget, 4)
        self.setLayout(self.vbox)

        self.button_start.clicked.connect(self.slot_button_start)
        self.button_pause.clicked.connect(self.slot_button_pause)
        self.button_stop.clicked.connect(self.slot_button_stop)

    def slot_button_start(self):
        if self.parent.opc_client:
            try:
                items = self.parent.project_list_widget.table.selectedItems()
                if(len(items) != 0):
                    for item in items:
                        name_item = item.text()
                        # Добавление в правый виджет, если это не было уже сделано двойным кликом
                        if name_item not in self.dict_name_open_procedures.keys():
                            scroll = Procedure_widget_scroll(self, item)
                            self.dict_name_open_procedures[name_item] = scroll
                            self.tab_main.addTab(scroll, name_item)

                            # Поток для выполнения
                            stream = threading.Thread(target=scroll.widget.execute_procedure)
                            self.dict_streams[name_item] = stream

                        procedure = self.dict_name_open_procedures[name_item].widget
                        if procedure.indicator_nods == 0:
                            procedure.defining_nodes()

                        if not self.dict_streams[name_item].is_alive():
                            # Запуск
                            self.dict_streams[name_item].start()


                        # elif self.dict_name_open_procedures[name_item].widget.status == 3:
                        #     t = QMessageBox.question(self, "Повторное выполнение", f'Запустить процедуру "{self.dict_name_open_procedures[name_item ].widget.project_name}" снова?')
                        #     if t == 16384:
                        #         # Повторный запуск
                        #         self.dict_name_open_procedures[name_item ].widget.start_procedure()
            except:
                pass
        else:
            self.parent.back.setGeometry(self.parent.frameGeometry())
            self.parent.back.show()
            self.parent.opc_widget.show()

    def slot_button_pause(self):
        if self.parent.opc_client:
            try:
                items = self.parent.project_list_widget.table.selectedItems()
                if (len(items) != 0):
                    for item in items:
                        name_item = item.text()
                        if name_item in self.dict_name_open_procedures.keys():

                            procedure = self.dict_name_open_procedures[name_item].widget
                            if self.dict_streams[name_item].is_alive():

                                if procedure.pause.is_set():
                                    # Ставим на паузу
                                    procedure.pause.clear()
                                    self.action_widget.addAction(f'Процедура "{procedure.project_name}" поставлена на паузу')
                                    # Добавление фона иконке в левому виджете (желтый цвет)
                                    item.setBackground(QColor(255, 255, 0))
                                else:
                                    self.action_widget.addAction(f'Процедура "{procedure.project_name}" снята с паузы')
                                    # Отпускаем паузу
                                    procedure.pause.set()
            except:
                pass
        else:
            self.parent.back.setGeometry(self.parent.frameGeometry())
            self.parent.back.show()
            self.parent.opc_widget.show()
    
    def slot_button_stop(self):
        if self.parent.opc_client:
            try:
                items = self.parent.project_list_widget.table.selectedItems()
                if (len(items) != 0):
                    for item in items:
                        name_item = item.text()

                        if name_item in self.dict_name_open_procedures.keys():
                            procedure = self.dict_name_open_procedures[name_item].widget

                            if self.dict_streams[name_item].is_alive():
                                # Останавливаем выполнение
                                procedure.stop.clear()
                                self.action_widget.addAction(f'Процедура "{self.project_name}" полностью остановлена')
                                procedure.remove_all_borders()
                                # Добавление фона иконке в левому виджете (красный цвет)
                                item.setBackground(QColor(255, 0, 0))
            except:
                pass
        else:
            self.parent.back.setGeometry(self.parent.frameGeometry())
            self.parent.back.show()
            self.parent.opc_widget.show()

qss = """ 
#tab_main::tab-bar {
    alignment: center;
}
#tab_main::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabBar::tab {
    border: 2px solid #C4C4C3;
    min-width: 50ex;
    min-height: 5ex;
    padding: 5px;
}
QTabBar::tab:selected  {
    border-color: #1dacd6;
    font: 14pt;
}  
QTabBar::tab:!selected {
    border-color:rgb(220, 220, 220);
    font: 14pt;
}

"""


        
class back(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setStyleSheet("background-color: rgba(0,0,0,0.8)")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setModal(True)


class Input_OPC_url_widget(QDialog):
    def __init__(self, parent = None):
        # Инициализация родительского класса
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 150)
        self.setWindowTitle('Подключение к OPC')
        self.setStyleSheet("background-color: rgb(176,176,176); border: 5px solid rgb(128,128,128) ;border-radius: 5px;")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.setContentsMargins(10,0,10,0)
        
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        #hbox1.addStretch(1)
        label = QLabel('url OPC UA сервера')
        hbox1.addWidget(label)
        #label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border: 3px solid rgb(176,176,176); font: 16px")
        self.line_url = QLineEdit()
        self.line_url.setStyleSheet("background-color: rgb(255,255,255);border: 1px solid rgb(128,128,128); font: 16px")
        hbox1.addWidget(self.line_url)

        self.hbox_buttons = QHBoxLayout()
        self.button_connect = QPushButton(' Подключиться ')
        self.button_close = QPushButton(' Закрыть ')
        self.button_connect.setStyleSheet("background-color: rgb(255,255,255);border: 1px solid rgb(128,128,128); font: 16px")
        self.button_close.setStyleSheet("background-color: rgb(255,255,255);border: 1px solid rgb(128,128,128); font: 16px")
        self.hbox_buttons.addStretch(1)
        self.hbox_buttons.addWidget(self.button_connect)
        self.hbox_buttons.addStretch(2)
        self.hbox_buttons.addWidget(self.button_close)
        self.hbox_buttons.addStretch(1)

        #vbox.addSpacing(10)
        vbox.addLayout(hbox1, 1)
        vbox.addSpacing(5)
        vbox.addSpacing(5)
        vbox.addLayout(self.hbox_buttons, 1)
        #vbox.addSpacing(10)

        self.setLayout(vbox)

        self.button_connect.clicked.connect(self.slot_button_connect)
        self.button_close.clicked.connect(self.slot_button_close)

    def slot_button_connect(self):

        self.url_ocp = self.line_url.text()
        print(self.url_ocp)
        if self.url_ocp or self.url_ocp == '':
            try:
                self.parent.opc_client = ClientApp(self.url_ocp)
                self.parent.opc_client.connect()
                self.parent.right_window.action_widget.addAction(f'Выполнено подключение к OPC UA серверу {self.url_ocp}')
                self.close()
                self.parent.back.close()
            except:
                self.parent.opc_client = None
                QMessageBox.critical(self.parent, "Ошибка подключения к OPC", "Не удалось подключиться к OPC серверу. Попробуйте ввести url заново", QMessageBox.Ok)


    def slot_button_close(self):
        if self.parent.opc_client:
            try:
                self.parent.opc_client.disconnect()
            except:
                pass
        self.close()
        self.parent.back.close()

class action_widget(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setFont(QFont("Times", 12))
        self.gb =  QGroupBox(self)
        self.main_vbox = QVBoxLayout() 
        self.table      = QTableWidget()
        self.table_hh   = self.table.horizontalHeader()
        self.table_vh   = self.table.verticalHeader()
        self.table_hh.setFont(QFont("Times", 14))
        #self.table.setRowCount(0)
        self.table.setColumnCount(2)

        self.table_hh.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_hh.setSectionResizeMode(0, 5)
        self.table_hh.setSectionResizeMode(1, 1)
        self.table_vh.setDefaultSectionSize(2)
        self.table.setHorizontalHeaderLabels(['Время', 'Событие'])

        self.main_vbox.addWidget(self.table)
        self.gb.setLayout(self.main_vbox)

    def addAction(self, message):
        rowPosition = 0
        self.table.insertRow(rowPosition)
        # print(rowPosition)
        # print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        self.table.setItem(rowPosition,0, QTableWidgetItem(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        self.table.setItem(rowPosition,1, QTableWidgetItem(message))
        self.table.item(rowPosition,0).setTextAlignment(QtCore.Qt.AlignVCenter)
        self.table.item(rowPosition,1).setTextAlignment(QtCore.Qt.AlignVCenter)
        self.table.item(rowPosition,0).setFlags(QtCore.Qt.ItemIsEnabled)
        self.table.item(rowPosition,1).setFlags(QtCore.Qt.ItemIsEnabled)

    def resizeEvent(self, a0):
        self.gb.resize(self.width() -20, self.height()-10)
        self.table.resize(self.gb.width()-25, self.gb.height()-20)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Perform()
    window.showMaximized()
    app.exec_()
