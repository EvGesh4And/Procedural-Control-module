from indicator import *
from PyQt5.Qt import QPoint

"""
Файл condition.py является частью модуля Proc.
Описание элемента блок-схемы Начало
Отображает название элемента, которое пользователь вводит на вкладке Основное Окна свойств блока
"""


class Begin(QWidget):
    def __init__(self, parent=None):
        """
        Метод определяет блок "Начало", его атрибуты: text - текстовое поле, node_child - для связи с нижеследующим блоком
        """
        super().__init__(parent)
        self.metka_blocka = 'begin'
        # Сын
        self.son = None

        self.active = False
        self.parent = parent

        self.font = QFont('Times', 8)
        self.setWindowTitle("Condition")
        self.setFixedSize(375, 260)
        self.setFont(self.font)
        self.comment = ''
        self.name_block = ''
        self.is_moveable = True
        self.moveable = True
        self.move_x = int((self.parent.parent.width() - self.width())/2)
        self.move_y = int((self.parent.parent.height()-self.height())/2) + int(self.parent.parent.scroll.verticalScrollBar().value())
        self.move(self.move_x, self.move_y)
        self.drawLine = None
        self.initUi()
        # Индикатор
        self.add_indicator()

    def initUi(self):
        ## Фон
        self.pic = QLabel("Begin", self)
        self.pic.setPixmap(QtGui.QPixmap("resources/Begin.png"))

        self.mainBox = QVBoxLayout(self)

        # Layout Названия блока
        self.Name_Label_box = QHBoxLayout()
        self.Name_Label_box.addStretch(1)
        self.Name_label = QLineEdit(self)
        self.Name_label.setPlaceholderText('Введите названия блока')
        self.Name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Name_label_font = QFont('Times', 10)
        self.Name_label.setFont(self.Name_label_font)
        self.Name_Label_box.addWidget(self.Name_label)
        self.Name_Label_box.addStretch(1)
        self.Name_Label_box.setStretch(1, 4)
        self.Name_label.textChanged.connect(self.Name_label_slots)

        # Layout текущего значения
        self.currentValue_box = QHBoxLayout()

        # Layout комментария QLabel
        self.comment_label_box = QHBoxLayout()
        self.comment_label = QLabel('Комментарий к блоку')
        self.comment_label.setAlignment(QtCore.Qt.AlignCenter)
        self.comment_label_font = QFont('Times', 10)
        self.comment_label.setFont(self.comment_label_font)
        self.comment_label_box.addWidget(self.comment_label)

        # Layout комментария
        self.commentLine_box = QHBoxLayout()
        self.commentLine = QTextEdit()
        self.commentLine.setPlaceholderText('Введите ваш комментарий')
        self.commentLine_box.addWidget(self.commentLine)
        self.commentLine.textChanged.connect(self.comment_slots)

        # Помещение всех Layout в главный с коэффициентами растяжения
        self.mainBox.addLayout(self.Name_Label_box)
        self.mainBox.addSpacing(10)
        self.mainBox.addLayout(self.comment_label_box)
        self.mainBox.addLayout(self.commentLine_box)
        self.mainBox.addStretch(1)
        self.mainBox.setContentsMargins(15, 20, 15, 15)

        # Контекстное меню
        self.contextMenu = QtWidgets.QMenu(self)
        self.fix_pos = self.contextMenu.addAction("Зафиксировать положение")
        self.delete_block = self.contextMenu.addAction("Удалить блок")

        self.fix_pos.triggered.connect(self.fix_position)
        self.delete_block.triggered.connect(self.deleted_block)

    def add_indicator(self):
        """
        Метод, описывающий индикатор соединения элемента с другими
        :return:
        """
        self.ind_down = Indicator(self, 'father')
        self.ind_down.show()
        self.ind_down.setGeometry(int((375 - 28) / 2), int(260 - 28), 28, 28)

    def scan_state_node_parents(self):
        if self.node_parents:
            active_parents = True
            for node in self.node_parents:
                if not node.active:
                    active_parents = False
            if active_parents:
                self.set_active_state(True)
                for node in self.node_parents:
                    node.set_active_state(False)
        else:
            self.set_active_state(False)

    def set_active_state(self, bool_state):
        self.active = bool_state

    def get_name(self) -> str:
        return self.real_name

    def set_name(self, name):
        self.name.setText(name)
        self.real_name = name.replace("_begin", "") + "_begin"
        print(f" MY NAME IS {self.real_name}")

    def save_project(self, path):
        name = self.get_name()
        # print(name)

        file_exist = os.path.exists(f"{path}/{name}/{name}")
        if (not file_exist):
            os.mkdir(f"{path}/{name}")

        with open(f"{path}/{name}/{name}", "w") as config:
            # config = csv.reader(config_file, delimiter=",")
            config.write("type,name")
            config.write(f"x,{self.x()}")
            config.write(f"y,{self.y()}")
            config.write(f"indicator1,{self.indicator.get_name()}")


    def set_var_filename(self, filename):
        """
        Метод для получения имени файла, который пользователь выбрал для получения переменных
        :param filename:
        :return:
        """
        self.filename = filename
        print("Opretation")
        self.proper.set_var_filename(filename)

    def ev(self, ev):
        """
        :param ev:
        :return:
        """
        if ev.type() == QtCore.QEvent.KeyPress and ev.key() in (
                QtCore.Qt.Key_Enter,
                QtCore.Qt.Key_Return,
        ):
            self.focusNextPrevChild(True)
        return super().event(ev)

    def resizeEvent(self, a0):
        """
        Метод адаптации размеров элемента
        :param a0:
        :return:
        """
        self.pic.setGeometry(10, 10, self.width() - 20, self.height() - 20)
        print(f" w = {self.width()} | h = {self.height()}")

    def set_child(self):
        """
        Метод добавления связи с нижеследующим элементом
        :param node_child:
        :return:
        """
        #self.node_child = node_child

    def mousePressEvent(self, event):
        """
        Метод, вызываемый при нажатии мыши
        :param event:
        :return:
        """
        self.mouse_x = self.x()
        self.mouse_y = self.y()
        self.xx = event.globalX()
        self.yy = event.globalY()
        self.click_value = event.pos()

    def mouseMoveEvent(self, event):
        """
        Метод перемещения элемента по рабочей области
        :param event:
        :return:
        """
        if (self.click_value.y() < 50):
            if (self.is_moveable):
                if (self.parent != None):
                    x = event.globalX()
                    y = event.globalY()
                    self.move_x = x - (self.xx - self.mouse_x)
                    self.move_y = y - (self.yy - self.mouse_y)
                    if self.move_x > self.parent.width() - self.width():
                        self.move_x = self.parent.width() - self.width()
                    if self.move_x < 0:
                        self.move_x = 0
                        # self.mouse_x = 10
                    if self.move_y < 0:
                        self.move_y = 0
                    if self.move_y > self.parent.height() - self.height():
                        self.move_y = self.parent.height() - self.height()

                    self.move(self.move_x, self.move_y)
                    self.parent.parent.scroll.ensureVisible(self.move_x + self.width(), self.move_y + self.height(), 0, 20)
                    self.parent.parent.scroll.ensureVisible(self.move_x + self.width(), self.move_y, 0, 20)
                else:
                    x = event.globalX()
                    y = event.globalY()
                    self.move_x = x - (self.xx - self.mouse_x)
                    move_y = y - (self.yy - self.mouse_y)
                    if self.move_x > self.main_width - self.width():
                        self.move_x = self.main_width - self.width()
                    if self.move_x < 0:
                        self.move_x = 0
                    if self.move_y < 0:
                        self.move_y = 0
                    if self.move_y > self.main_height - self.height():
                        self.move_y = self.main_height - self.height()
                    self.move(self.move_x, self.move_y)
                    self.parent.parent.scroll.ensureVisible(self.move_x + self.width(), self.move_y + self.height(), 0, 20)
                    self.parent.parent.scroll.ensureVisible(self.move_x + self.width(), self.move_y, 0, 20)

                self.point_line_update()

    def point_line_update(self):
        if self.son:
            self.drawLine.begin = self.ind_down.pos() + self.pos() + QPoint(14, 14)
            self.drawLine.destination = self.son.ind_up.pos() + self.son.pos() + QPoint(14, -1)
            self.parent.update()

    def setMoveable(self, ind):
        self.moveable = ind

    def save_logs(self):
        """
        Метод сохранения настроек элемента
        :return:
        """
        self.settings.setValue("Geometry_X", self.x())
        self.settings.setValue("Geometry_Y", self.y())
        self.settings.setValue("Moveable", str(self.is_moveable))
        print(str(self.x()) + " | " + str(self.y()))

    def contextMenuEvent(self, event):
        """
        По нажатию правой кнопки по элементу появляется контекстное меню
        :param event:
        :return:
        """
        print("Открылось контекстное меню")
        # self.contextMenu.move(self.x(), self.y())
        # self.contextMenu.show()
        action = self.contextMenu.exec_(self.mapToGlobal(event.pos()))

    def fix_position(self):
        """
        Метод фиксации положения элемента
        :return:
        """
        print("Нажали на кнопку Удали")
        self.is_moveable = not self.is_moveable

    def deleted_block(self):
        """
        Метод удаления объекта с главного окна
        :return:
        """
        self.reply = QMessageBox.question(
            self, "Удаление",
            "Вы действительно хотите удалить блок Начало?",
            QMessageBox.Yes | QMessageBox.No)

        if self.reply == QMessageBox.Yes:
            # Удаление уже установленных связей
            if self.son != None:
                self.son.ind_up.set_picture_off_dist()
                self.son.father = None
                self.son = None

            # Удаление из претендентов
            if self.parent.current_father == self:
                self.parent.current_father = None

            # Удаление блока из списка виджетов
            self.parent.widget_list.remove(self)
            # Делаем кнопку добавить блок начало снова активной
            self.parent.parent.begin_menu.setEnabled(True)
            self.close()
            self.parent.begin = None

        else:
            pass

    def comment_slots(self):
        self.comment = self.commentLine.toPlainText()
        print('self.comment', self.comment)

    def Name_label_slots(self):

        self.name_block = self.Name_label.text()
        print('self.name_block', self.name_block)


if __name__ == "__main__":
    # QtCore.QCoreApplication.addLibraryPath("./")
    app = QtWidgets.QApplication(sys.argv)
    window = Begin()
    window.show()
    app.exec_()
