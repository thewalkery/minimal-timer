from PyQt5.QtCore import QObject, QTimerEvent
from PyQt5.QtCore import pyqtSignal
from minimaltimer.time import Time


class TimerEngine(QObject):
    timeChanged = pyqtSignal()
    timeout = pyqtSignal()

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)
        self._time = Time()
        self._timerId = self.startTimer(1000)
        
    def timerEvent(self, event: QTimerEvent) -> None:
        if self._time.getSeconds() == 0:
            return
        self._time.setSeconds(self._time.getSeconds() - 1)
        self.timeChanged.emit()
        print(self._time.getSeconds())
        if self._time.getSeconds() == 0:
            self.timeout.emit()

    def setTime(self, time: Time) -> None:
        if time.getSeconds() < 0:
            # Invalid time
            return
        if self._time == time:
            return
        self._time = time
        self.timeChanged.emit()

    def getTime(self) -> Time:
        return self._time