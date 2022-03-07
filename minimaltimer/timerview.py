from cmath import cos, pi, sin, sqrt
from math import atan2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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
            self._engine.timeout.connect(self.onEngineTimeout)
            self.handleTimeChanged(self._engine.getTime())

    def handleTimeChanged(self, time: Time) -> None:
        pass

    def handleTimeout(self) -> None:
        pass

    def getEngineTime(self) -> Time:
        if not self._engine:
            return Time()
        return self._engine.getTime()

    def setEngineTime(self, time: Time) -> None:
        if not self._engine:
            print("Error: A timer engine is not exist.")
            return
        self._engine.setTime(time)

    @pyqtSlot()
    def onEngineTimeChanged(self) -> None:
        if not self._engine:
            return
        self.handleTimeChanged(self._engine.getTime())

    @pyqtSlot()
    def onEngineTimeout(self) -> None:
        if not self._engine:
            return
        self.handleTimeout()


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

    def handleTimeChanged(self, time: Time) -> None:
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
    WINDOW_SIDE = 1000
    CIRCLE_RADIUS = 400
    TEXT_RADIUS = 450

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self._dragging = False

    def getRadius(self) -> int:
        side = min(self.width(), self.height())
        return side // 2

    def isPosInClock(self, pos: QPoint) -> bool:
        center = self.rect().center()

        def distance(p1: QPoint, p2: QPoint) -> float:
            return sqrt((p1.x() - p2.x())**2 + (p1.y() - p2.y())**2).real

        return distance(pos, center) <= self.getRadius()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        side = min(self.width(), self.height())
        painter.setViewport((self.width() - side) // 2, 
                            (self.height() - side) // 2,
                            side, side)
        painter.setWindow(-self.WINDOW_SIDE // 2, -self.WINDOW_SIDE // 2,
                          self.WINDOW_SIDE, self.WINDOW_SIDE)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.drawClockScale(painter)
        self.drawClockHand(painter)

    def drawClockScale(self, painter: QPainter) -> None:
        painter.save()

        def getX(secs: int) -> float:
            rad = self.secondsToRadian(secs)
            return sin(rad).real

        def getY(secs: int) -> float:
            rad = self.secondsToRadian(secs)
            return -cos(rad).real

        # Draw small ticks
        smallPen = QPen()
        smallPen.setWidth(0)
        painter.setPen(smallPen)
        for min in range(0, 60):
            secs = min * 60
            rad = self.secondsToRadian(secs)
            x1 = (self.CIRCLE_RADIUS - 10) * getX(secs)
            y1 = (self.CIRCLE_RADIUS - 10) * getY(secs)
            x2 = (self.CIRCLE_RADIUS + 10) * getX(secs)
            y2 = (self.CIRCLE_RADIUS + 10) * getY(secs)
            painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw big ticks
        bigPen = QPen()
        bigPen.setWidth(5)
        painter.setPen(bigPen)
        for min in range(0, 60, 5):
            secs = min * 60
            rad = self.secondsToRadian(secs)
            x1 = (self.CIRCLE_RADIUS - 12) * getX(secs)
            y1 = (self.CIRCLE_RADIUS - 12) * getY(secs)
            x2 = (self.CIRCLE_RADIUS + 12) * getX(secs)
            y2 = (self.CIRCLE_RADIUS + 12) * getY(secs)
            painter.drawLine(QLineF(x1, y1, x2, y2))

        # Draw text
        font = painter.font()
        font.setPointSize(30)

        textPen = QPen()
        textPen.setWidth(0)

        painter.setPen(textPen)
        painter.setBrush(Qt.GlobalColor.black)
        fontMetrics = QFontMetrics(font)

        textPath = QPainterPath()
        for min in range(0, 60, 5):
            secs = min * 60
            rad = self.secondsToRadian(secs)
            x = int(self.TEXT_RADIUS * getX(secs))
            y = int(self.TEXT_RADIUS * getY(secs))
            textWidth = fontMetrics.width(str(min))
            textHeight = fontMetrics.height()
            textPath.addText(x - textWidth // 2, y + textHeight // 2, font, str(min))
        painter.drawPath(textPath)
        painter.restore()

    def drawClockHand(self, painter: QPainter) -> None:
        secs = self.getEngineTime().getSeconds()

        painter.save()
        pen = QPen()
        pen.setWidth(0)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 0, 0))
    
        path = QPainterPath()
        path.moveTo(0, 0)
        path.arcTo(-self.CIRCLE_RADIUS, -self.CIRCLE_RADIUS, 
                   2*self.CIRCLE_RADIUS, 2*self.CIRCLE_RADIUS, 
                   90, -self.secondsToRadian(secs) * 180 / pi)
        path.lineTo(0, 0)
        painter.drawPath(path)
        painter.restore()

    def handleTimeChanged(self, time: Time) -> None:
        self.repaint()

    def handleTimeout(self) -> None:
        QMessageBox.information(self, "Timeout", "Timeout")

    def secondsToRadian(self, secs: int) -> float:
        return secs * pi / 1800

    def radianToSeconds(self, rad: float) -> int:
        return int((rad + pi) / pi * 1800)

    def posToSeconds(self, pos: QPoint) -> int:
        pos_from_center = pos - self.rect().center()
        theta = atan2(-pos_from_center.x(), +pos_from_center.y())
        #print('theta:', theta)
        return self.radianToSeconds(theta)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self.isPosInClock(event.pos()):
                if not self._dragging:
                    self._dragging = True
                    self._engine.pause()
                secs = self.posToSeconds(event.pos())
                #print(secs)
                self.setEngineTime(Time(secs))

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.isPosInClock(event.pos()):
                if not self._dragging:
                    self._dragging = True
                    self._engine.pause()

            if self._dragging:
                secs = self.posToSeconds(event.pos())
                prevTime = self.getEngineTime()

                if prevTime.getSeconds() > 3600 - 300 and secs < 300:
                    self.setEngineTime(Time(3600))
                elif prevTime.getSeconds() < 300 and secs > 3600 - 300:
                    self.setEngineTime(Time(0))
                else:
                    self.setEngineTime(Time(secs))

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            if self._dragging:
                self._dragging = False
                self._engine.resume()

        return super().mouseReleaseEvent(event)