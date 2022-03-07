from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSizePolicy

from minimaltimer.timerengine import TimerEngine
from minimaltimer.timerview import SpinboxTimerView, TimerView
from minimaltimer.optionsbar import OptionsBar


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._timerview = TimerView(self)
        self._timerengine = TimerEngine(self)
        self._timerview.setEngine(self._timerengine)

        self._optionsbar = OptionsBar(self)

        self._centralwidget = QWidget()
        self.setCentralWidget(self._centralwidget)
        self.setupCentralWidget()
        self.resize(640, 640)

    def setupCentralWidget(self) -> None:
        self._centralwidget.setLayout(QVBoxLayout())
        self._centralwidget.layout().addWidget(self._timerview)
        self._timerview.setSizePolicy(QSizePolicy.Policy.Expanding, 
                                      QSizePolicy.Policy.Expanding)
        self._centralwidget.layout().addWidget(self._optionsbar)


