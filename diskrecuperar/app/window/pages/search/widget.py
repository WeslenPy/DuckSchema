from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *
from diskrecuperar.utils.manager.image import ImageManager
from diskrecuperar.app.components.input.widget import InputSearch
from diskrecuperar.app.components.listview.widget import ListWidget,ItemView


class SearchPage(QWidget):
    def __init__(self, parent:QStackedWidget = None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent
        
        self.manager = ImageManager()
        
        self.setup()
        
    def setup(self):
        

        self.spacer_h = QSpacerItem(10,10,
                            QSizePolicy.Policy.Minimum,
                            QSizePolicy.Policy.Expanding)
    
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5,0,0,0)
        self.main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        self.search_frame = QFrame()
        
        
      
        self.search_layout = QVBoxLayout(self.search_frame)
        self.search_layout.setContentsMargins(0,0,0,0)
        self.search_layout.setSpacing(0)
        
                
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)
        
        
        
        
        self.search_input = InputSearch(
            text="Pesquise o modelo da sua placa aqui"
            )
        
        self.list_search = ListWidget(relative=self.content_frame)
        
        
        # for _ in range(24):
        #     self.item = QListWidgetItem()
        #     self.item_widget = ItemView()
        #     # self.item.setText("Tesete")
        #     self.list_search.addItem(self.item)
        #     self.list_search.setItemWidget(self.item,self.item_widget)
        
        
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addItem(self.spacer_h)
        self.search_layout.addWidget(self.list_search)
        
        
        self.content_layout.addWidget(self.search_frame)
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
        