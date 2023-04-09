

"""
Часть модуля Core аутентификации 
Первый из дочерних файлов аутентификации
"""


import csv
# import matplotlib.pyplot as plt
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QAction, QPushButton

import sys
import os
import hashlib



class Core_widget_auth_enter(QtWidgets.QWidget):
    def __init__(self, parent = None, config_password = "./SUUTP/COMMON/"):
        super().__init__(parent)
        """
        Метод инициализации, содержит в себе настройку параметров и их инициализацию 
        содержит в себе те элементы, которые критически необходимы для работы 
        """
        self.parent = parent
        self.setFont(QFont("Times", 14))

        self.setGeometry(0,0,440,275)
        self.config_password = config_password
        self.gb = QGroupBox(self)
        self.gb.setGeometry(0,0,self.width() - 10, self.height() -10)

        self.gb_name = QGroupBox("Имя пользователя" , self.gb)
        self.gb_name.setGeometry(10,5 , self.gb.width() - 20, 55)

        self.gb_password = QGroupBox("Пароль", self.gb)
        self.gb_password.setGeometry(10 , self.gb_name.y() + self.gb_name.height() + 10 , self.gb.width() - 20, 55)

        self.comboBox_name = QComboBox(self.gb_name)

        self.line_password = QLineEdit(self.gb_password)
        self.line_password.setEchoMode(QLineEdit.Password)

        self.button_enter = QPushButton("Авторизоваться", self.gb)
        self.button_enter.setGeometry(10, self.gb_name.y() + self.gb_name.height() , self.gb.width() - 20 , 55)

        self.button_enter.clicked.connect(self.slot_button_enter)

        self.setFixedSize(445,275)
        self.init_resize()
        self.setup_init_window()

        # self.core = Core()

    def setup_init_window(self):
        """
        Метод начальной настройки окна, если быть конкретнее, то настройки ComboBox
        с выпадающими именами пользователей
        Также в методе считываются пароли этих пользователей и их привилегии 
        """
        self.dict_name_pass = {}
        self.dict_name_priv = {}
        exist_pass_file = self.check_file()
        if(exist_pass_file):
            with open(f"{self.config_password}") as p:
                passwords = csv.DictReader(p , delimiter=":")
                for row in passwords:
                    self.dict_name_pass[row["name"]] = row["password"]
                    self.dict_name_priv[row["name"]] = row["privileges"]
        self.comboBox_name.addItems(self.dict_name_pass.keys())


    def slot_button_enter(self):
        """
        Метод срабатывает при нажатии кнопки Авторизоваться 
        Считывает текущее имя из поля   ComboBox и сверяет введеный пароль с паролем из специального файла 
        (данные предварительно были из файла перенесены в соотвесвующие словари)

        Если пароль был введен верно,то прячем данное окно и открываем основную программу 
        """
        password = self.line_password.text()
        #print(self.comboBox_name.currentText())
        exist_pass_file = self.check_file()

        if(exist_pass_file):
            if(self.dict_name_pass.keys().__contains__(self.comboBox_name.currentText())):

                if(self.dict_name_pass[self.comboBox_name.currentText()] == hashlib.sha512(bytes(password, encoding="utf-8")).hexdigest()):
                    self.parent.set_prev(self.dict_name_priv[self.comboBox_name.currentText()])
                    self.parent.success_enter()
                    print("Access")
                else:
                    QMessageBox.information(self, "Ошибка авторизации", f"Введён неверный пароль.", QMessageBox.Ok)
                    #print(password)

    def check_file(self):
        """
        Метод проверяет существует ли файл с паролями 
        Без него нельзя будет войти в основную программу
        """
        file_exist = os.path.exists(f"{self.config_password}")
        if(not file_exist):
            QMessageBox.critical(self, "Ошибка авторизации", f"Файл учетных данных не найден.", QMessageBox.Ok)
        return file_exist
    
    def is_valid_auth(self):
        return True

    def init_resize(self):
        """
        Метод котороый вызывается во время инициализации, нужен для того чтобы овнои его элементы имели правильную геометрию 
        """
        self.gb.resize(self.width() - 10, self.height() - 20)
        self.gb_name.setGeometry(10,10 , self.gb.width() - 20, 75)
        self.comboBox_name.setGeometry(5, 35 , self.gb_name.width() - 10, self.gb_name.height() - 35 - 5)


        self.gb_password.setGeometry(10 , self.gb_name.y() + self.gb_name.height() + 10 , self.gb.width() - 20, 75)
        self.line_password.setGeometry(5, 35 , self.gb_password.width() - 10, self.gb_password.height() - 35 - 5)

        self.button_enter.setGeometry(10, self.gb_password.y() + self.gb_password.height() + 10 + 10, self.gb.width() - 20 , 40)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dl = Core_widget_auth_enter() 
    dl.show()
    sys.exit(app.exec_())


