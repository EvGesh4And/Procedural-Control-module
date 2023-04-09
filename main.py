from comita import *
from Development import *
from perform_window import *
"""
Файл BlockDiagram.py является частью модуля Proc.
Основное окно, в котором пользователь может собрать блок-схему.
Содержит меню, в котором представлены функции программы
"""


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Метод определяет Главное окно
        """
        # Инициализация родительского класса
        super().__init__()

        # Убирает кнопки в правом верхнем углу
        # self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        # Название главного окна
        self.setWindowTitle("ПК «Экстремум». Модуль процедурной автоматизации")

        # Добавление логотипа главному окну
        self.setWindowIcon(QIcon("resources/logo_Extremum.png"))

        # Задание размера окна, который равен размеру допустимой области экрана
        screen = QDesktopWidget().availableGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        # Флаг, который задает окно поверх всех окон
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.tab_main = QTabWidget(self)
        self.tab_main.setObjectName('tab_main')
        self.tab_main.setStyleSheet(qss)
        self.tab_main.move(0, 0)

        self.tab_development = Development(self)
        self.tab_perform = Perform(self)
        self.tab_main.addTab(self.tab_development, "Разработка")
        self.tab_main.addTab(self.tab_perform, "Исполнение")

        self.comita = Comita(self)
        self.setMinimumSize(800, 800)

        self.comita.show()

    def resizeEvent(self, e):
        self.comita.setGeometry(self.width() - 200, self.height() - 80, 160, 50)
        self.tab_main.resize(self.geometry().width(), self.geometry().height())
        self.tab_development.development_workspace.window_size()
        # self.tab_development.Dev.resizeEvent(e)
    
    def closeEvent(self, a0):
        try:
            self.tab_perform.opc_client.disconnect()
        except:
            pass
        try:
            self.tab_perform.added_project_wid.close()
        except:
            pass

qss = """ 
#tab_main::tab-bar {
    alignment: center;
}
#tab_main::pane { /* The tab widget frame */
    border-top: 2px solid #C2C7CB;
}

QTabBar::tab {
    border: 2px solid #C4C4C3;
    min-width: 24ex;
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

if __name__ == "__main__":
    app = QApplication([''])
    window = MainWindow()
    window.show()
    app.exec_()