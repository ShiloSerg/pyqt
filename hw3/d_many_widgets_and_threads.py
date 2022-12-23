"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
from PySide6 import QtWidgets
from c_weatherapi_widget import Window as Weather
from b_systeminfo_widget import Window as Sysinfo


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        self.weather = Weather()
        self.sysinfo = Sysinfo()

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.sysinfo)
        layout.addWidget(self.weather)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
