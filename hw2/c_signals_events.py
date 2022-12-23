"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

from PySide6 import QtWidgets, QtCore, QtGui
from hw2.ui.c_signals_event import Ui_Form


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initSignals()

    def initSignals(self):
        self.ui.pushButtonLT.clicked.connect(lambda: self.move(0, 0))
        self.ui.pushButtonRT.clicked.connect(self.moveRightTop)
        self.ui.pushButtonLB.clicked.connect(self.moveLeftBottom)
        self.ui.pushButtonRB.clicked.connect(self.moveRightBottom)
        self.ui.pushButtonCenter.clicked.connect(self.moveCenter)
        self.ui.pushButtonMoveCoords.clicked.connect(self.moveToCoordinates)
        self.ui.pushButtonGetData.clicked.connect(self.getData)
        # self.screenResolution()
        # self.num_screns()

    def moveRightTop(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_width = current_screen.size().width()
        pos_x = screen_width - self.width()

        self.move(pos_x, 0)

    def moveLeftBottom(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_height = current_screen.size().height()
        pos_y = screen_height - self.height()

        self.move(0, pos_y)

    def moveRightBottom(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        screen_width = current_screen.size().width()
        pos_x = screen_width - self.width()
        screen_height = current_screen.size().height()
        pos_y = screen_height - self.height()

        self.move(pos_x, pos_y)

    def moveCenter(self):
        current_screen = QtWidgets.QApplication.screenAt(self.pos())
        app_size = QtWidgets.QWidget.size(self)
        pos_x = current_screen.size().width() / 2 - app_size.width() / 2
        pos_y = current_screen.size().height() / 2 - app_size.height() / 2

        self.move(pos_x, pos_y)

    def moveToCoordinates(self):
        pos_x = int(self.ui.spinBoxX.text())
        pos_y = int(self.ui.spinBoxY.text())

        self.move(pos_x, pos_y)

    def getData(self):
        self.ui.plainTextEdit.setPlainText(
            f"Кол-во экранов: {len(QtGui.QGuiApplication.screens())}\n"
            f"Текущее основное окно: {QtGui.QGuiApplication.applicationDisplayName()}\n"
            f"Разрешение экрана: {self.screen().size().width()} x"
            f" {self.screen().size().height()}\n"
            f"Окно находится на экране {self.screen().name()}\n"
            f"Размеры окна: {self.width()} x {self.height()}\n"
            f"Минимальные размеры окна: {self.minimumWidth()} x {self.minimumHeight()}\n"
            f"Текущее координаты окна: {self.geometry().getCoords()}\n"
            f"Координаты центра приложения: {self.geometry().center().toTuple()}\n")

    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        """
        Событие изменения размера окна

        :param event: QtGui.QResizeEvent
        :return: None
        """
        self.ui.plainTextEdit.setPlainText(
            f"{QtCore.QDateTime.currentDateTime().toString('HH:mm:ss')}: "
            f"Старая позиция: {event.oldPos().toTuple()} Новая позиция: {event.pos().toTuple()}"
        )

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        Событие изменения размера окна

        :param event: QtGui.QResizeEvent
        :return: None
        """
        self.ui.plainTextEdit.setPlainText(
            f"{QtCore.QDateTime.currentDateTime().toString('HH:mm:ss')}: Размер окна изменен, новый размер: "
            f"{event.size().width()} x {event.size().height()}"
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
