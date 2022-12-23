"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

from PySide6 import QtWidgets, QtCore
from wheatherUI import Ui_Form
from a_threads import WeatherHandler


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.weatherinfo = WeatherHandler(lat=0, lon=0)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUi()
        self.initSignals()

    def initUi(self):
        self.ui.pushButton.setText("Узнать погоду")
        self.ui.lineEditlat.setText("59")
        self.ui.lineEditlong.setText("30")
        self.ui.spinBox.setValue(5)

    def initSignals(self):
        self.ui.pushButton.clicked.connect(self.pressButton)
        self.weatherinfo.weatherInfoReceived.connect(self.weatherInfoReceive)

    def pressButton(self):
        if self.ui.pushButton.text() == "Узнать погоду":
            self.weatherThreadWorking()
        else:
            self.weatherThreadStoped()

    def weatherThreadWorking(self):
        lat = self.ui.lineEditlat.text()
        lon = self.ui.lineEditlong.text()
        delay = self.ui.spinBox.value()
        self.weatherinfo.setUrl(lat, lon)
        self.weatherinfo.setDelay(delay)
        self.weatherinfo.start()
        self.ui.pushButton.setText("Остановить")
        self.ui.lineEditlat.setEnabled(False)
        self.ui.lineEditlong.setEnabled(False)
        self.ui.spinBox.setEnabled(False)

    def weatherThreadStoped(self):
        self.weatherinfo.stop()
        self.ui.pushButton.setText("Узнать погоду")
        self.ui.spinBox.setEnabled(True)
        self.ui.lineEditlat.setEnabled(True)
        self.ui.lineEditlong.setEnabled(True)

    def weatherInfoReceive(self, data):
        latitude = str(data['latitude'])
        longitude = str(data['longitude'])
        temperature = str(data['current_weather']['temperature'])
        windspeed = str(data['current_weather']['windspeed'])
        time = QtCore.QDateTime.currentDateTime().toString('HH:mm:ss')

        self.ui.plainTextEdit.appendPlainText(f"{time}\n"
                                              f"Широта: {latitude}\n"
                                              f"Долгота: {longitude}\n"
                                              f"Температура: {temperature}\n"
                                              f"Скорость ветра: {windspeed}\n")

    def closeEvent(self, event):
        self.weatherinfo.terminate()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
