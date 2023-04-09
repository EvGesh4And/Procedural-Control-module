from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
import sys

"""
Файл indicator.py является частью модуля Proc.
Класс Indicator создан для отображения наличия связей блока с другими блоками
"""


class Indicator(QWidget):
    def __init__(self, parent=None, role=None):
        """
        Описание класса
        :param parent: родительским окном является MainWindow
        """
        super().__init__(parent)
        self.parent = parent
        self.role = role
        self.ongoing = False
        self.setGeometry(0, 0, 28, 28)
        self.active = False

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.active == False:
            painter.setPen(QPen(QColor(0, 136, 217), 1, Qt.SolidLine))
            painter.setBrush(QBrush(QColor(0, 136, 217), Qt.SolidPattern))
        else:
            painter.setPen(QPen(QColor(34, 176, 45), 1, Qt.SolidLine))
            painter.setBrush(QBrush(QColor(34, 176, 45), Qt.SolidPattern))

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawEllipse(1, 1, 24, 24)

    def mousePressEvent(self, event):
        self.parent.click_value = QPoint(0, 100)
        if (not self.active):
            self.set_picture_on()
        else:
            self.set_picture_off()

    def set_picture_on(self):
        self.active = True
        self.parent.parent.son_father_on(self.parent, self.role)
        self.update()

    def set_picture_off(self):
        self.active = False
        self.parent.parent.son_father_off(self.parent, self.role)
        self.update()

    def set_picture_off_dist(self):
        self.active = False
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWidget = Indicator()
    myWidget.show()
    sys.exit(app.exec_())

