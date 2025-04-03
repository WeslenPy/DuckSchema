from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtSvg import *
from src.utils.manager.image import ImageManager
from src.app.components.input.widget import InputSearch
from src.app.components.listview.widget import ListView


class SearchPage(QWidget):
    def __init__(self, parent:QStackedWidget = None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent
        
        self.manager = ImageManager()
        
        self.setup()
        
    def setup(self):
        

        self.spacer_h = QSpacerItem(10,10,
                            QSizePolicy.Policy.Expanding,
                            QSizePolicy.Policy.Minimum)
    
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5,10,0,10)
        self.main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        self.search_frame = QFrame()
        
        
        self.search_layout = QVBoxLayout(self.search_frame)
        self.search_layout.setContentsMargins(50,10,60,10)
        self.search_layout.setSpacing(0)
        
                
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(50,10,50,10)
        self.content_layout.setSpacing(0)

        
        self.search_input = InputSearch()
        self.list_search = ListView(relative=self.content_frame)
        
        
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addItem(self.spacer_h)
        self.search_layout.addWidget(self.list_search)
        
        
        self.content_layout.addWidget(self.search_frame)
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
        