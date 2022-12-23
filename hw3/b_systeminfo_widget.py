"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets
from sysinfowidget import Ui_Form
from a_threads import SystemInfo


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.sysinfo = SystemInfo()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUi()
        self.initThread()
        self.initSignals()

    def initUi(self):
        self.ui.spinBox.setValue(5)
        self.sysinfo.delay = self.ui.spinBox.value()

    def initThread(self):
        self.sysinfo.start()

    def initSignals(self):
        self.ui.spinBox.valueChanged.connect(self.onspinBoxChanged)
        self.sysinfo.systemInfoReceived.connect(self.getInfo)

    def onspinBoxChanged(self):
        self.sysinfo.delay = self.ui.spinBox.value()

    def getInfo(self, value):
        cpu_value = value[0]
        ram_value = value[1]
        self.ui.lcdNumber.display(cpu_value)
        self.ui.lcdNumber_2.display(ram_value)

    def closeEvent(self, event):
        self.sysinfo.terminate()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
