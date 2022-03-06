from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPaintEvent, QPainter, QBrush, QColor
from minimaltimer.timerengine import TimerEngine
from minimaltimer.time import Time

class AbstractTimerView(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._engine = None

    def setEngine(self, engine: TimerEngine) -> None:
        self._engine = engine
        if self._engine:
            self._engine.timeChanged.connect(self.onEngineTimeChanged)

    def displayTime(self, time: Time) -> None:
        pass

    def setEngineTime(self, time: Time) -> None:
        if not self._engine:
            print("Error: A timer engine is not exist.")
            return
        self._engine.setTime(time)

    @pyqtSlot()
    def onEngineTimeChanged(self) -> None:
        if not self._engine:
            return
        self.displayTime(self._engine.getTime())

class SpinboxTimerView(AbstractTimerView):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._spinbox = QSpinBox()
        self._startButton = QPushButton("Start")
        self._editing = False
        self.initUi()

        self._spinbox.valueChanged.connect(self.onSpinboxValueChanged)
        self._startButton.clicked.connect(self.onStartButtonClicked)

    def initUi(self) -> None:
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._spinbox)
        self.layout().addWidget(self._startButton)

    def displayTime(self, time: Time) -> None:
        if self._editing == True:
            # ignore 
            return

        wasBlocked = self._spinbox.blockSignals(True)
        self._spinbox.setValue(time.getSeconds())
        self._spinbox.blockSignals(wasBlocked)

    @pyqtSlot()
    def onSpinboxValueChanged(self) -> None:
        self._editing = True

    @pyqtSlot()
    def onStartButtonClicked(self) -> None:
        self._editing = False
        self.setEngineTime(Time(self._spinbox.value()))

class TimerView(AbstractTimerView):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)

        side = min(self.width(), self.height())

        painter.setViewport((self.width() - side) // 2, 
                            (self.height() - side) // 2,
                            side, side)
        painter.setWindow(-50, -50, 100, 100)

        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(-50, -50, 100, 100)

    def displayTime(self, time: Time) -> None:
        pass