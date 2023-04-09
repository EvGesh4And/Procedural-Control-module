from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint

class Comita(QWidget):
    def __init__(self, parent=None):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        # Задание логотипа Комиты
        self.com = QLabel(self)
        self.com.setScaledContents(True)
        self.com.setPixmap(QPixmap("resources/comita.png"))
        self.com.setGeometry(0, 0, 160, 50)
        self.raise_()