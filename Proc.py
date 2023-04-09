
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QAction, QPushButton
from PyQt5.QtCore import Qt , QTimer


from main import MainWindow
from Core_widget_auth_enter import *
from Core_widget_auth_change_password import *


class Proc_auth(QtWidgets.QWidget):

    def __init__(self, parent = None):
        """
        Метод инициализации, содержит начальную настройку окна
        """
        super().__init__(parent)


        self.setWindowIcon(QIcon("resources/logo_Extremum.png"))
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setFont(QFont("Times", 14))
        self.setFixedSize(460,305)
        self.move(QDesktopWidget().availableGeometry().center().x() - int(self.width()/2), QDesktopWidget().availableGeometry().center().y() - int(self.height()/2))
        self.setWindowTitle("Окно авторизации")
        self.config_password = "../SUUTP/COMMON/.passwords"

        self.tabs = QTabWidget(self)
        self.tabs.setGeometry(10,0,440,300)
        self.previliege = ""
        self.tab1 = Core_widget_auth_enter(self, config_password = self.config_password)
        self.tab2 = Core_widget_auth_change_password(self, config_password = self.config_password)


        self.setup_init_tabs() 

        self.core = MainWindow()


    def set_prev(self, prev):
        self.previliege = prev


    def setup_init_tabs(self):
        """
        Метод начальной настройки закладок, методя для разгрузки метода инициализации
        """
        self.tabs.addTab(self.tab1, "Вход")
        self.tabs.addTab(self.tab2, "Смена пароля")
        self.tabs.setObjectName('tab_main')
        self.tabs.setStyleSheet(qss)

    def check_file(self):
        """
        Метод проверки существования файла с паролями
        без этого файла допуск к программе невозможен
        """
        file_exist = os.path.exists(f"{self.config_password}")
        if(not file_exist):
            QMessageBox.critical(self, "Ошибка авторизации", f"Файл учетных данных не найден.", QMessageBox.Ok)
        return file_exist

    def success_enter(self):
        """
        Метод, который вызывается из дочернего окна, если аутентификация прошла успешно
        """

        self.hide()
        #self.core.setGeometry(0, 0, 1024, 768)
        self.core.setMinimumSize(1024,768)
        self.core.show()


    def update_password(self, name, password):
        """
        Метод, котоорый вызывается из дочернего окна, если успешно прошло изменение пароля, его обновление
        записывается в словари окна аутентификации
        """
        self.tab1.dict_name_pass[name] = password
        print('self.tab1.dict_name_pass', self.tab1.dict_name_pass)
        self.tabs.setCurrentIndex(0)
        with open(f"{self.config_password}" , 'w') as password_file:
            print('смена паролей')
            password_file.write("name:privileges:password\n")
            for name in self.tab1.dict_name_pass.keys():
                password_file.write(f"{name}:{self.tab1.dict_name_priv[name]}:{self.tab1.dict_name_pass[name]}\n")
        

    def is_valid_auth(self):
        return True
    
    def keyPressEvent(self, e):
        print('event')
        if e.key()==16777220:
            if self.tabs.currentIndex() == 0:
                self.tab1.slot_button_enter()
            elif self.tabs.currentIndex() == 1:
                self.tab2.slot_button_next()

qss = """ 
#tab_main::tab-bar {
    alignment: center;
}
#tab_main::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabBar::tab {
    border: 2px solid #C4C4C3;
    min-width: 205px;
    min-height: 10px;
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dl = Proc_auth() 
    dl.show()
    sys.exit(app.exec_())