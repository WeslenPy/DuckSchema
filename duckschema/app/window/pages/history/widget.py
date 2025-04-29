from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *
from duckschema.utils.manager.image import ImageManager

class HistoryPage(QWidget):
    def __init__(self, parent:QStackedWidget = None,pages=None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent