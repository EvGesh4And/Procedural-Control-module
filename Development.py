from development_workspace import *

ms = """ 
QMenuBar {
    spacing: 5px; /* spacing between menu bar items */
    font: 12pt;
}
QMenuBar::item {
    padding: 2px 4px;
    background: transparent;
    border-radius: 4px;
}
QMenuBar::item:selected { /* when selected using mouse or keyboard */
    border: 1px solid #05B8CC;
}
"""

"""
Файл Development.py является частью модуля Proc.
Основное окно, в котором пользователь может собрать блок-схему.
Содержит меню, в котором представлены функции программы
"""

class Development(QMainWindow):
    def __init__(self, parent = None):
        """
        Метод определяет Главное окно
        """
        self.parent = parent
        super().__init__(parent)

        self.setStyleSheet(ms)

        # Создание вложенных списков
        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        # Добавление Скролл
        self.development_workspace = Development_workspace(self, self.parent)
        self.scroll = QScrollArea()
        self.setCentralWidget(self.scroll)
        self.scroll.setWidget(self.development_workspace)
        # self.scroll.setStyleSheet("padding-bottom: 10px;")

        # Настройка менюбара
        self.menubar.setObjectName("menubar")

        self.menu = self.menubar.addMenu("Меню")
        self.get_names_tags = self.menu.addAction("Получить имена тэгов")
        # self.editing = self.menu.addAction('Открыть процедуру')
        self.save = self.menu.addAction("Сохранить процедуру")

        self.get_names_tags.triggered.connect(self.development_workspace.get_tags)
        # self.editing.triggered.connect(self.development_workspace.editing_project)
        self.save.triggered.connect(self.development_workspace.save_project)

        # Создание вложенных списков
        self.add_elem = self.menubar.addMenu("Добавить элемент")
        self.begin_menu = self.add_elem.addAction("Начало")
        self.operation_menu = self.add_elem.addAction("Операция")
        self.condition_menu = self.add_elem.addAction("Условие")
        self.end_menu = self.add_elem.addAction("Конец")

        # Создание вложенных списков
        self.tools = self.menubar.addMenu("Инструменты")
        self.correctness = self.tools.addAction("Проверка корректности")
        self.alignment = self.tools.addAction("Выравнивание")

        self.correctness.triggered.connect(self.development_workspace.correctness_fun)
        self.alignment.triggered.connect(self.development_workspace.alignment_fun)

        # Вызов команд при нажатии на кнопки
        self.begin_menu.triggered.connect(self.development_workspace.add_begin)
        self.operation_menu.triggered.connect(self.development_workspace.add_operation)
        self.condition_menu.triggered.connect(self.development_workspace.add_condition)
        self.end_menu.triggered.connect(self.development_workspace.add_end)

