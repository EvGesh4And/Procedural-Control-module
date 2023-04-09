
"""
Часть модуля Core аутентификации 
Первый из дочерних файлов аутентификации
"""


# from xmlrpc.client import Boolean
import csv
# import matplotlib.pyplot as plt
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets , uic
from PyQt5.QtWidgets import QFileDialog, QMenuBar, QAction, QPushButton

import sys
import os

import hashlib



class Core_widget_auth_change_password(QtWidgets.QWidget):
    def __init__(self, parent = None, config_password = "./SUUTP/COMMON/"):
        """
        Метод инициализации, в нем прописаны основные параметры и вызовы функций 
        без которых ничего работать не будет
        """
        super().__init__(parent)
  
        self.config_password = config_password
        self.parent = parent
        self.setFont(QFont("Times", 14))

        self.setGeometry(0,0,445,250)

        self.init_1st_step()
        self.init_2nd_step()
        self.setup_init_window()
        self.gb_2nd.close()
        self.last_step = False


        self.button_previous    = QPushButton("Назад", self)
        self.button_next        = QPushButton("Авторизоваться", self)

        self.button_previous.clicked.connect(self.slot_button_previous)
        self.button_next.clicked.connect(self.slot_button_next)

        self.button_previous.setGeometry(0,self.height() - 60, int((self.width() - 20)/2) , 40)
        self.button_next.setGeometry(self.button_previous.width() + 10, self.height() - 60, int((self.width() - 20)/2), 40)

        self.button_previous.hide()

    def slot_button_previous(self):
        """
        Слот отвечающий за кнопку предыдущий шаг, переключается на окно ввода пароля для его смены 
        """
        self.button_previous.hide()
        self.set_empty_lines()
        self.button_next.setText("Авторизоваться")
        self.gb_1st.show()
        self.gb_2nd.close()
        self.last_step = False

    def slot_button_next(self):
        """
        Слот отвечающий за кнопку следующий шаг, в методе прописано несколько условий 

        Часть смены пароля 2
        self.last_step - булевская переменная, если она True -> на предыдущем шаге пароль был введен верно 
        и включено окно смены пароля (ввести новый пароль и его копию)

        далее идет проверка на то, что пароли совпадают, если они совпадают значит пароль можно менять
        вызывается метод из головного окна по смене пароля и в окне аутентификации
        соотвествующий вывод в консоль

        Часть смены пароля 1
        Проверка на то, что введенный пароль действительно принадлежит выбранному пользователю
        Если это так, значит можно переключиться на окно смены пароля (ввести пароль и его копию)
        и поставить флаг последний шаг (self.last_step = True)

        Также есть проверка, на то что этот флаг уже взведен 
        (если память не изменяет это было добавлено, чтобы после одной смены пароля, можно было бы успешно второй раз его менять за одну сессию)
        """
        k = False
        if(self.last_step):
            password = ''
            if(self.line_password_new1.text() == self.line_password_new2.text()):
                password = self.line_password_new1.text()
                if(len(password) > 3):
                    name = self.comboBox_name.currentText()
                    self.dict_name_pass[name] = hashlib.sha512(bytes(password, encoding="utf-8")).hexdigest()

                    self.parent.update_password(name,hashlib.sha512(bytes(password, encoding = "utf-8")).hexdigest())
                    self.password_succesfuly_changed()
                    QMessageBox.information(self, "Изменение учётной записи", f"Пароль для пользователя {name} успешно изменён.", QMessageBox.Ok)
                    self.last_step = False
                    k = True
                else:
                    QMessageBox.information(self, "Изменение учётной записи", f"Длина пароля должна составлять не менее 4-х символов.", QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Ошибка изменения учетной записи", "Пароли не совпадают. Повторите ввод.", QMessageBox.Ok)
        else:
            password = self.line_password.text()

        if(self.valid_password(password) and not self.last_step and not k):
            self.line_password.setText("")
            self.button_previous.show()
            self.gb_2nd.show()    
            self.gb_1st.close()
            self.last_step = True
            self.button_next.setText('Изменить')

    def password_succesfuly_changed(self):
        """
        Название метода говорит само за себя
        Пароль был успешно изменен: все стадии были пройдены успешно, а значит надо очистить все поля ввода
        и переключиться на окно аутентификации
        """
        self.button_next.setText("Авторизоваться")
        self.button_previous.hide()
        self.set_empty_lines()
        self.gb_1st.show()
        self.gb_2nd.close()

    def set_empty_lines(self):
        """
        Метод, который чистит поля ввода паролей, как на смене пароля, так и на вводе пароля
        метод вызывается только при успешной смене пароля 
        """
        self.line_password.setText("")
        self.line_password_new1.setText("")
        self.line_password_new2.setText("")

    def setup_init_window(self):
        """
        Метод начальной настройки окна, вызывается из метода инициализации
        нужен для его разгрузки, здесь по суди считываются из файла имена пользователей, их привилегии и пароли,
        чтобы после использовать для смены последних и для аутентификации
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

    def init_1st_step(self):
        """
        Метод настройки первого окна смены пароля (шаг на котором просят имя пользователя и его пароль)
        """
        self.gb_1st = QGroupBox(self)
        self.gb_1st.setGeometry(0,0,self.width() - 10, self.height() - 10 - 60)

        self.gb_name = QGroupBox("Имя пользователя" , self.gb_1st)
        self.gb_name.setGeometry(10,10 , self.gb_1st.width() - 20, 75)

        self.comboBox_name = QComboBox(self.gb_name)
        self.comboBox_name.setGeometry(5, 35 , self.gb_name.width() - 10, self.gb_name.height() - 35 - 5)

        self.gb_password = QGroupBox("Пароль", self.gb_1st)
        self.gb_password.setGeometry(10 , self.gb_name.y() + self.gb_name.height() + 10 , self.gb_1st.width() - 20, 75)

        self.line_password = QLineEdit(self.gb_password)
        self.line_password.setEchoMode(QLineEdit.Password)
        self.line_password.setGeometry(5, 35 , self.gb_password.width() - 10, self.gb_password.height() - 35 - 5)

    def valid_password(self, password):
        #password = self.line_password.text()      
        exist_pass_file = self.check_file()

        if(exist_pass_file):
            if(self.dict_name_pass.keys().__contains__(self.comboBox_name.currentText())):
                if(self.dict_name_pass[self.comboBox_name.currentText()] == hashlib.sha512(bytes(password, encoding="utf-8")).hexdigest()):
                    return True
                else:
                    if password != '':
                        QMessageBox.information(self, "Ошибка изменения учетной записи", "Неверный пароль", QMessageBox.Ok)
                    return False
                    print("Access denied: Password Incorrect")
        
        return False


    def init_2nd_step(self):
        """
        Метод настройки второго окна смены пароля (шаг на котором нужно ввести новый пароль и его копию/подтверждение)

        """
        self.gb_2nd = QGroupBox(self)
        self.gb_2nd.setGeometry(0,0,self.width() - 10, self.height() - 10 - 60)

        self.gb_password_new1   = QGroupBox("Введите новый пароль", self.gb_2nd)
        self.line_password_new1 = QLineEdit(self.gb_password_new1)
        self.gb_password_new2   = QGroupBox("Повторите новый пароль", self.gb_2nd)
        self.line_password_new2 = QLineEdit(self.gb_password_new2)


        self.line_password_new1.setEchoMode(QLineEdit.Password)
        self.line_password_new2.setEchoMode(QLineEdit.Password)


        self.gb_password_new1.setGeometry(10,10,self.gb_2nd.width() - 20,75)
        self.line_password_new1.setGeometry(5,35,self.gb_password_new1.width() - 10,35)

        self.gb_password_new2.setGeometry(10,self.gb_password_new1.y() + self.gb_password_new1.height() + 10, self.gb_2nd.width() - 20, 75)
        self.line_password_new2.setGeometry(5,35, self.gb_password_new2.width() - 10, 35)
    
    def check_file(self):
        """
        Метод проверки существования файла паролей без которого доступа к основной программе ни у кого не будет
        в файле хранятся имена пользователей, их привелегии и пароли
        """
        file_exist = os.path.exists(f"{self.config_password}")
        if(not file_exist):
            QMessageBox.critical(self, "Ошибка авторизации", f"Файл учетных данных не найден.", QMessageBox.Ok)
        return file_exist

    def init_resize(self):
        print("Resize")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dl = Core_widget_auth_change_password() 
    dl.show()
    sys.exit(app.exec_())
