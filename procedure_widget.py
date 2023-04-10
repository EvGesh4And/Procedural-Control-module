from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint

from Blocks_for_widget import *
from Draw_arrow import DrawingProcess
import threading

class Procedure_widget_scroll(QWidget):
    def __init__(self, parent = None, item = None):
        super().__init__(parent)
        self.parent = parent
        self.widget = Procedure_widget(self.parent, item)
        scroll = QScrollArea()
        scroll.setWidget(self.widget)
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(Qt.white))
        scroll.setPalette(self.palette)
        self.widgetbox = QVBoxLayout()
        self.widgetbox.addWidget(scroll)
        self.setLayout(self.widgetbox)

    def resizeEvent(self, a0):
        self.widget.setFixedWidth(self.parent.size().width()-50)


class Procedure_widget(QWidget):
    def __init__(self, parent = None, item = None):
        # Инициализация родительского класса
        super().__init__(parent)
        # Родитель
        self.parent = parent

        # Статус процедуры
        # 0 - не активна
        # 1 - выполняется
        # 2 - на паузе
        # 3 - выполнен
        self.status = 0

        # Элемент в левом виджете
        self.item = item

        # Имя процедуры
        self.project_name = item.text()

        # Список всех блоков, входящих в процедуру
        self.widgets = []

        # Очередь блоков на выполнение
        self.execution_queue = []

        # Список тегов и путей
        self.name_tags = []
        self.ways_tags = []
        self.nodes = []

        # Индикатор словаря нодов
        self.indicator_nods = 0

        # Словарь нодов
        self.dict_nods = {}

        # События "Пауза" и "Стоп"
        self.pause = threading.Event()
        # Событие паузы активно (вот такая вот обратная логика, если активна, то паузы нет)
        self.pause.set()
        self.stop = threading.Event()
        # Для аналогичности
        self.stop.set()

        self.load_blocks()
        self.initUI()


    def load_blocks(self):
        filepath = 'Procedures' + '/' + self.project_name + '.txt'
        with open(filepath, "r") as f:
            lines = f.readlines()
            line = lines[0]
            ind = 0
            while line != 'tags\n':
                if line == 'begin\n':
                    begin = Begin(self)
                    begin.name_block = lines[ind+1]
                    begin.comment = lines[ind+2].replace('\n', '')
                    begin.initUi()
                    self.widgets.append(begin)
                    ind += 3
                elif line == 'operation\n':
                    operation = Operation(self)
                    operation.name_block = lines[ind+1]
                    operation.comment = lines[ind+2].replace('\n', '')
                    #print([float(x) for x in lines[ind+3][2:-3].split("', '")])
                    operation.condition_values = [float(x) for x in lines[ind+3][1:-2].split(', ')]
                    operation.condition_tags = lines[ind+4][2:-3].split("', '")
                    operation.initUi()
                    self.widgets.append(operation)
                    ind += 5
                elif line == 'condition\n':
                    condition = Condition(self)
                    condition.name_block = lines[ind+1]
                    condition.comment = lines[ind+2].replace('\n', '')
                    condition.condition_values = [float(x) for x in lines[ind+3][1:-2].split(', ')]
                    condition.condition_signs = lines[ind+4][2:-3].split("', '")
                    condition.condition_tags = lines[ind+5][2:-3].split("', '")
                    condition.initUi()
                    self.widgets.append(condition)
                    ind += 6
                elif line == 'end\n':
                    end = End(self)
                    end.name_block = lines[ind+1]
                    end.comment = lines[ind+2].replace('\n', '')
                    end.initUi()
                    self.widgets.append(end)
                    ind += 3
                line = lines[ind]

            self.name_tags = lines[ind + 1][2:-3].split("', '")
            self.ways_tags = lines[ind + 2][2:-2].split("', '")

    def defining_nodes(self):
        try:
            self.nodes = self.parent.parent.opc_client.get_nodes_from_tags(self.ways_tags)
        except:
            pass

        for i in range(len(self.name_tags)):
            self.dict_nods[self.name_tags[i]] = self.nodes[i]
        self.indicator_nods = 1

    def initUI(self):
        
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background, QBrush(Qt.white))
        self.setPalette(self.palette)
        
        self.mainbox = QVBoxLayout()
        # self.begin = Begin(self)
        # self.operation = Operation(self)
        # self.condition = Condition(self)
        # self.end = End(self)
        # self.widgets = [self.begin, self.operation, self.condition, Operation(self), Operation(self), Operation(self),self.end]
        for block in self.widgets:
            self.mainbox.addWidget(block)
            self.mainbox.setSpacing(50)
            block.drawLine = DrawingProcess(self)
            
        # self.widgets[0].recolor_border('green')
        # self.widgets[1].recolor_border('green')
        # self.widgets[2].recolor_border('yellow')
        # self.widgets[2].recolor_border('red')
        # self.widgets[-1].recolor_border('red')


        self.Hmainbox = QHBoxLayout(self)
        self.Hmainbox.addStretch(1)
        self.Hmainbox.addLayout(self.mainbox, 1)
        self.Hmainbox.addStretch(1)

        self.setLayout(self.Hmainbox)

    # def resizeEvent(self, a0):
    #     """
    #     Метод адаптации размеров элемента
    #     :param a0:
    #     :return:
    #     """
    #     print('event Perform_widget')
    #     self.setFixedWidth(self.parent.size().width()-50)

    def paintEvent(self, event):
        #painter = QPainter(self)
        for i in range(len(self.widgets)-1):
            block = self.widgets[i]
            block.drawLine.begin = block.pos() + QPoint(190, 130)
            block.drawLine.destination = self.widgets[i+1].pos() + QPoint(190, 10)
            block.drawLine.draw(self)

    def execute_procedure(self):
        print('(◕‿◕)')
        # Добавление фона иконке в левом виджете (зеленый цвет)
        self.item.setBackground(QColor(0, 255, 0))
        # Список блоков на выполнение
        self.execution_queue = self.widgets[:]
        # Вывод сообщения о запуске
        self.parent.action_widget.addAction(f'Запуск процедуры "{self.project_name}"')

        for block in self.execution_queue:
            # if not self.stop.is_set():
            #     self.parent.action_widget.addAction(f'Процедура "{self.project_name}" полностью остановлена')
            #     self.remove_all_borders()
            #     # Добавление фона иконке в левому виджете (красный цвет)
            #     self.item.setBackground(QColor(255, 0, 0))
            #     self.pause.set()
            #     self.stop.set()
            #     return
            if not self.pause.is_set():
                # Добавление фона иконке в левому виджете (красный цвет)
                self.item.setBackground(QColor(255, 255, 0))
                block.recolor_border(4, 'yellow')
                self.pause.wait()

            block.recolor_border(4, 'green')
            block.execute_block()

        # elif self.status == 2:
        #     self.parent.action_widget.addAction(f'Процедура "{self.project_name}" снята с паузы')
        #
        # elif self.status == 3:
        #     self.remove_all_borders()
        #     # Список блоков на выполнение
        #     self.execution_queue = self.widgets[:]
        #     # Вывод сообщения о запуске
        #     self.parent.action_widget.addAction(f'Повторный запуск процедуры "{self.project_name}"')
        #
        # self.status = 1
        # self.execution_queue[0].execute_block()

    def pause_procedure(self):
        print("\(★ω★)/")

    def stop_procedure(self):
        print("＼(￣▽￣)／")
        if self.status == 1 or self.status == 2:
            self.parent.action_widget.addAction(f'Процедура "{self.project_name}" полностью остановлена')
            # Добавление фона иконке в левому виджете (желтый цвет)
            self.item.setBackground(QColor(255, 0, 0))
            self.status = 0
            self.remove_all_borders()

    def remove_all_borders(self):
        for w in self.widgets:
            w.recolor_border(0, 'white')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Perform_widget()
    window.showMaximized()
    app.exec_()