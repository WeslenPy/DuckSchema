from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *
from diskrecuperar.utils.manager.image import ImageManager
from diskrecuperar.app.components.input.widget import InputButton
from diskrecuperar.app.components.listview.widget import ListWidget,ItemView


class LoginPage(QWidget):
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
        
        self.list_frame = QFrame()
        
        self.list_layout = QVBoxLayout(self.list_frame)
        self.list_layout.setContentsMargins(0,0,0,0)
        self.list_layout.setSpacing(0)
                
        self.search_layout = QVBoxLayout(self.search_frame)
        self.search_layout.setContentsMargins(10,10,10,10)
        self.search_layout.setSpacing(0)
        
                
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(10,10,10,10)
        self.content_layout.setSpacing(0)
        
     
        self.search_layout.addItem(self.spacer_h)
        self.search_layout.addWidget(self.list_frame)
        
        
        self.content_layout.addWidget(self.search_frame)
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
        