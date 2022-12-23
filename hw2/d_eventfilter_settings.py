"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""
from PySide6.QtCore import Qt

from ui.d_eventfilter_settings import Ui_Form
from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initSignals()
        self.initUi()

    def initUi(self):
        self.ui.comboBox.addItems(["oct", "hex", "bin", "dec"])
        self.ui.comboBox.setCurrentText("dec")
        self.ui.comboBox.currentIndexChanged.connect(self.comboBoxChanged)

        settings = QtCore.QSettings("Eventfilter")
        self.ui.comboBox.setCurrentText(settings.value("comboBoxValue", "dec"))
        self.ui.horizontalSlider.setValue(settings.value("value"))

    def initSignals(self):
        self.ui.dial.valueChanged.connect(self.DialChange)
        self.ui.horizontalSlider.valueChanged.connect(self.SliderChange)

    def SliderChange(self):
        self.ui.lcdNumber.display(self.ui.horizontalSlider.value())
        self.ui.dial.setValue(self.ui.horizontalSlider.value())

    def DialChange(self):
        self.ui.lcdNumber.display(self.ui.dial.value())
        self.ui.horizontalSlider.setValue(self.ui.dial.value())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            self.ui.dial.setValue(self.ui.dial.value() + 1)
        elif event.key() == Qt.Key_Minus:
            self.ui.dial.setValue(self.ui.dial.value() - 1)

    def comboBoxChanged(self):
        if self.ui.comboBox.currentText() == 'dec':
            self.ui.lcdNumber.setDecMode()
        elif self.ui.comboBox.currentText() == 'oct':
            self.ui.lcdNumber.setOctMode()
        elif self.ui.comboBox.currentText() == 'bin':
            self.ui.lcdNumber.setBinMode()
        else:
            self.ui.lcdNumber.setHexMode()

    def closeEvent(self, event):
        settings = QtCore.QSettings("Eventfilter")
        settings.setValue("value", self.ui.horizontalSlider.value())
        settings.setValue("comboBoxValue", self.ui.comboBox.currentText())

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()