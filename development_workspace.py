from begin import *
from condition import *
from operation import *
from end import *
from tags_list_widget import *
from Draw_arrow import DrawingProcess
from editing_procedure_widget import *

bs_plus = """ 
QPushButton::hover { /* when selected using mouse or keyboard */
    background-image : url(resources/plus.png);
    border-radius : 20;
    border: 2px solid #05B8CC;
}

QPushButton{
    background-image : url(resources/plus.png);
    border-radius : 20;
    border: 2px solid #f0f0f0;
}
"""

bs_minus = """ 
QPushButton::hover { /* when selected using mouse or keyboard */
    background-image : url(resources/minus.png);
    border-radius : 20;
    border: 2px solid #05B8CC;
}

QPushButton{
    background-image : url(resources/minus.png);
    border-radius : 20;
    border: 2px solid #f0f0f0;
}
"""

class Development_workspace(QMainWindow):
    def __init__(self, parent = None, progenitor = None):
        """
        Метод определяет Главное окно
        """
        self.parent = parent
        self.progenitor = progenitor
        super().__init__(parent)
        super().__init__(progenitor)

        # Имена тегов
        self.tag_names = []

        # Пути в OPC каждого тега
        self.tag_paths = []

        # Сын
        self.current_son = None
        # Отец
        self.current_father = None

        # Список блоков
        self.widget_list = []

        # Размеры окна
        self.actual_width = self.progenitor.width() - 30
        self.actual_height = self.progenitor.height() - 100
        self.resize(self.actual_width, self.actual_height)

        # Размер окна актуальная
        self.actual_progenitor_width = self.progenitor.width()
        self.actual_progenitor_height = self.progenitor.height()

        # Размер окна актуальная
        self.old_progenitor_width = self.progenitor.width()
        self.old_progenitor_height = self.progenitor.height()

        # Переменные блоков
        self.begin = None
        self.operation = None
        self.condition = None
        self.end = None

        self.plus_button = QPushButton(self)
        self.minus_button = QPushButton(self)
        self.plus_button.setStyleSheet(bs_plus)
        self.minus_button.setStyleSheet(bs_minus)
        self.plus_button.clicked.connect(self.add_space)
        self.minus_button.clicked.connect(self.delete_space)

    def add_space(self):
        self.actual_height += 500
        self.setFixedHeight(self.actual_height)

    def delete_space(self):
        ln = len(self.widget_list)
        wh = 0
        if ln > 0:
            for i in range(ln):
                if self.widget_list[i].pos().y() + 260 > wh:
                    wh = self.widget_list[i].pos().y() + 260

        if self.actual_height >= self.progenitor.height() - 100 + 500 and wh + 500 < self.actual_height:
            self.actual_height -= 500
            self.setFixedHeight(self.actual_height)

    def get_tags(self):
        """
        Метод получения названий переменных из файла, который выбрал пользователь
        :return:
        """

        # Имена тэгов
        self.tag_names = []
        # Пути в OPC каждого тэга
        self.tag_paths = []

        self.a = tags_list_widget(self)
        self.a.show()

    def save_project(self):
        if len(self.tag_names) == 0:
            QMessageBox.critical(self.progenitor, "Ошибка в тэгах", "Не загружен файл с тэгами или файл некорректен", QMessageBox.Ok)
            return 0
        if self.correctness_fun(1) == 0:
            input_dialog = QInputDialog(self.progenitor)
            input_dialog.setInputMode(QInputDialog.TextInput)
            input_dialog.setWindowTitle('Новый проект')
            input_dialog.setLabelText('Название проекта:')

            input_dialog.setFixedSize(220, 100)  # Set the input dialog size
            input_dialog.show()
            if input_dialog.exec_() != input_dialog.Accepted:
                print("canceled")
            else:
                self.save_name = input_dialog.textValue()  # After clicking OK, get the input dialog content
                print("ok")

                self.save_filename = "Procedures/" + self.save_name + '.txt'
                f = open(self.save_filename, 'w')

                ind_end_save = 0
                save_work_widget = self.begin

                while ind_end_save == 0:
                    f.write(save_work_widget.metka_blocka)
                    f.write('\n')
                    print(save_work_widget.metka_blocka)
                    if save_work_widget.metka_blocka == 'begin':
                        f.write(save_work_widget.name_block)
                        f.write('\n')
                        f.write(save_work_widget.comment.replace('\n', ' '))
                        f.write('\n')

                    if save_work_widget.metka_blocka == 'condition':
                        f.write(save_work_widget.name_block)
                        f.write('\n')
                        f.write(save_work_widget.comment.replace('\n', ' '))
                        f.write('\n')
                        f.write(str(save_work_widget.condition_values))
                        f.write('\n')
                        f.write(str(save_work_widget.condition_signs))
                        f.write('\n')
                        f.write(str(save_work_widget.condition_tags))
                        f.write('\n')

                    if save_work_widget.metka_blocka == 'operation':
                        f.write(save_work_widget.name_block)
                        f.write('\n')
                        f.write(save_work_widget.comment.replace('\n', ' '))
                        f.write('\n')
                        f.write(str(save_work_widget.condition_values))
                        f.write('\n')
                        f.write(str(save_work_widget.condition_tags))
                        f.write('\n')

                    if save_work_widget.metka_blocka == 'end':
                        f.write(save_work_widget.name_block)
                        f.write('\n')
                        f.write(save_work_widget.comment.replace('\n', ' '))
                        f.write('\n')
                        ind_end_save = 1
                        f.write('tags')
                        f.write('\n')
                        f.write(str(self.tag_names))
                        f.write('\n')
                        f.write(str(self.tag_paths))
                    else:
                        save_work_widget = save_work_widget.son

                QMessageBox.information(self.progenitor, "Сохранение файла", "Файл успешно сохранен", QMessageBox.Ok)

    def add_begin(self):
        """
        Метод создания элемента класса Начало
        :return: виджет на главном окне
        """
        self.begin = Begin(self)
        self.begin.drawLine = DrawingProcess(self)
        self.begin.show()
        self.widget_list.append(self.begin)
        # Делаем кнопку добавить блок начало  неактивной
        self.parent.begin_menu.setEnabled(False)

    def add_operation(self):
        """
        Метод создания элемента класса Начало
        :return: виджет на главном окне
        """
        self.operation = Operation(self)
        self.operation.drawLine = DrawingProcess(self)
        self.widget_list.append(self.operation)
        self.operation.show()

    def add_condition(self):
        """
        Метод создания элемента класса Начало
        :return: виджет на главном окне
        """
        self.condition = Condition(self)
        self.condition.drawLine = DrawingProcess(self)
        self.widget_list.append(self.condition)
        self.condition.show()

    def add_end(self):
        """
        Метод создания элемента класса Начало
        :return: виджет на главном окне
        """
        self.end = End(self)
        print(type(self.end))
        # Делаем кнопку добавить блок конец неактивной
        self.parent.end_menu.setEnabled(False)
        self.end.show()
        self.widget_list.append(self.end)

        print(self.widget_list)

    def son_father_on(self, block=None, role=None):
        if role == 'son':
            if self.current_son != None:
                self.current_son.ind_up.set_picture_off_dist()
            self.current_son = block
        if role == 'father':
            if self.current_father != None:
                self.current_father.ind_down.set_picture_off_dist()
            self.current_father = block

        if self.current_son != None and self.current_father != None and self.current_son != self.current_father:
            self.current_son.father = self.current_father
            self.current_father.son = self.current_son
            self.current_father.drawLine.begin = self.current_father.ind_down.pos() + self.current_father.pos() + QPoint(14, 14)
            self.current_father.drawLine.destination = self.current_son.ind_up.pos() + self.current_son.pos() + QPoint(14, -1)
            self.update()
            self.current_father = None
            self.current_son = None

        print('Сын:')
        print(self.current_son)
        print('Отец:')
        print(self.current_father)

    def son_father_off(self, block=None, role=None):
        # Удаление уже установленных связей
        if role == 'son' and self.current_son != block:
            block.father.drawLine.begin = QPoint()
            block.father.drawLine.destination = QPoint()
            self.update()
            block.father.ind_down.set_picture_off_dist()
            block.ind_up.set_picture_off_dist()
            block.father.son = None
            block.father = None

        if role == 'father' and self.current_father != block:
            block.drawLine.begin = QPoint()
            block.drawLine.destination = QPoint()
            self.update()
            block.son.ind_up.set_picture_off_dist()
            block.ind_down.set_picture_off_dist()
            block.son.father = None
            block.son = None

        # Удаление из претендентов
        if role == 'son' and self.current_son == block:
            self.current_son.ind_up.set_picture_off_dist()
            self.current_son = None
        if role == 'father' and self.current_father == block:
            self.current_father.ind_down.set_picture_off_dist()
            self.current_father = None

        print('Сын:')
        print(self.current_son)
        print('Отец:')
        print(self.current_father)

    def paintEvent(self, event):
        painter = QPainter(self)
        for widget in self.widget_list:
            if widget.son:
                widget.drawLine.draw(self)

    def correctness_fun(self, flag_corr = 0):
        if self.begin == None:
            QMessageBox.critical(self.progenitor, "Ошибка", "Нет блока 'Начало'", QMessageBox.Ok)
            return 1
        if self.end == None:
            QMessageBox.critical(self.progenitor, "Ошибка", "Нет блока 'Конец'", QMessageBox.Ok)
            return 1

        ind_alignment = 0
        alignment_work_widget = self.begin
        kol = 0
        while ind_alignment == 0:
            kol += 1
            if alignment_work_widget.metka_blocka != 'end' and alignment_work_widget.son == None:
                QMessageBox.critical(self.progenitor, "Ошибка", "Некорректные связи между блоками", QMessageBox.Ok)
                return 1
            if alignment_work_widget.metka_blocka != 'end':
                alignment_work_widget = alignment_work_widget.son
            else:
                ind_alignment = 1

        if kol != len(self.widget_list):
            QMessageBox.critical(self.progenitor, "Ошибка", "Некорректные связи между блоками", QMessageBox.Ok)
            return 1
        if flag_corr == 0:
            QMessageBox.information(self.progenitor, "Все корректно", "Связи заданы корректно", QMessageBox.Ok)
        return 0

    def alignment_fun(self):
        if self.correctness_fun(1) == 0:
            delta_y = self.begin.height()
            delta_yy = 40
            y = delta_yy
            ind_alignment = 0
            alignment_work_widget = self.begin

            while ind_alignment == 0:
                alignment_work_widget.move_x = int((self.width() - alignment_work_widget.width()) / 2)
                alignment_work_widget.move_y = y
                alignment_work_widget.move(alignment_work_widget.move_x, alignment_work_widget.move_y)
                y = y + delta_y + delta_yy
                if alignment_work_widget.metka_blocka != 'end':
                    alignment_work_widget = alignment_work_widget.son
                else:
                    ind_alignment = 1

            ind_alignment = 0
            alignment_work_widget = self.begin

            while ind_alignment == 0:
                if alignment_work_widget.metka_blocka != 'end':
                    alignment_work_widget.drawLine.begin = alignment_work_widget.ind_down.pos() + alignment_work_widget.pos() + QPoint(14, 14)
                    alignment_work_widget.drawLine.destination = alignment_work_widget.son.ind_up.pos() + alignment_work_widget.son.pos() + QPoint(14, -1)
                    alignment_work_widget = alignment_work_widget.son
                else:
                    ind_alignment = 1
            self.update()
    def calculation_new_position(self):
        ln = len(self.widget_list)
        wh = 0
        if ln > 0:
            for i in range(ln):
                width_block = self.widget_list[i].width()

                w = int(round((self.widget_list[i].move_x + width_block) * (self.actual_progenitor_width - 30) / ( self.old_progenitor_width - 30) - width_block))
                if w > 0:
                    self.widget_list[i].move_x = w
                else:
                    self.widget_list[i].move_x = 0

                height_block = self.widget_list[i].height()
                h = int(round((self.widget_list[i].move_y + height_block) * self.actual_height / (self.actual_height + self.old_progenitor_height - self.actual_progenitor_height) - height_block))
                if h > 0:
                    self.widget_list[i].move_y = h
                else:
                    self.widget_list[i].move_y = 0

                self.widget_list[i].move(self.widget_list[i].move_x, self.widget_list[i].move_y)

            for i in range(ln):
                self.widget_list[i].point_line_update()

    def window_size(self):
        # Размер окна актуальная
        self.actual_progenitor_width = self.progenitor.width()
        self.actual_progenitor_height = self.progenitor.height()

        # Обновление размеров окна
        self.actual_width = self.actual_width - self.old_progenitor_width + self.actual_progenitor_width
        self.actual_height = self.actual_height - self.old_progenitor_height + self.actual_progenitor_height

        # Пересчет положения блоков
        self.calculation_new_position()

        # Новые размеры становятся старыми
        self.old_progenitor_width = self.actual_progenitor_width
        self.old_progenitor_height = self.actual_progenitor_height

        self.setFixedWidth(self.actual_width)
        self.setFixedHeight(self.actual_height)

    def editing_project(self):
        self.editing_procedure_widget = editing_procedure_widget(self)
        self.editing_procedure_widget.show()

    def resizeEvent(self, e):
        self.minus_button.setGeometry(int(self.actual_width / 2 + 20), int(self.actual_height - 63), 43, 43)
        self.plus_button.setGeometry(int(self.actual_width / 2 - 60), int(self.actual_height - 63), 43, 43)

        # self.window_size()
        # self.setFixedWidth(self.actual_width)
        # self.setFixedHeight(self.actual_height)