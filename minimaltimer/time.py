class Time:
    def __init__(self, secs: int = 0) -> None:
        self._secs = secs

    def getSeconds(self) -> int:
        return self._secs

    def setSeconds(self, secs: int) -> None:
        self._secs = secs