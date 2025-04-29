from PySide6.QtCore import QTimer, QObject


class Debounce(QObject):
    def __init__(self, callback, timeout_ms=300):
        super().__init__()
        self._callback = callback
        self._timeout_ms = timeout_ms
        self._timer = QTimer()
        self._timer.setInterval(self._timeout_ms)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._callback)

    def call(self):
        self._timer.stop()
        self._timer.start()

    def cancel(self):
        self._timer.stop()

    def is_active(self):
        return self._timer.isActive()