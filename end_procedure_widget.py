from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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


class back_end_procedure(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("background-color: rgba(0,0,0,0.8)")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setModal(True)


class end_procedure_widget(QDialog):
    def __init__(self, parent=None):
        # Инициализация родительского класса
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setFixedSize(400, 150)
        self.move()
        self.setWindowTitle('Процедура выполнена')
        self.setStyleSheet("background-color: rgb(176,176,176); border: 5px solid rgb(128,128,128) ;border-radius: 5px;")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setModal(True)
        self.setContentsMargins(10, 0, 10, 0)

        label = QLabel('url OPC UA сервера')
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border: 3px solid rgb(176,176,176); font: 16px")

        self.button_ok = QPushButton(' Принято ')
        self.button_ok.setStyleSheet("background-color: rgb(255,255,255);border: 1px solid rgb(128,128,128); font: 16px")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox_buttons = QHBoxLayout()

        hbox.addWidget(label)
        hbox_buttons.addWidget(self.button_ok)

        vbox.addLayout(hbox, 1)
        vbox.addSpacing(5)
        vbox.addSpacing(5)
        vbox.addLayout(hbox_buttons, 1)

        self.setLayout(vbox)

        self.button_ok.clicked.connect(self.slot_button_ok)

    def slot_button_ok(self):
        self.close()
        self.parent.end_back.close()

