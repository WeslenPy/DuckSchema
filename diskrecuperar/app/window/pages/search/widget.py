from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtSvg import *
from diskrecuperar.utils.manager.image import ImageManager
from diskrecuperar.app.components.input.widget import InputButton
from diskrecuperar.app.components.listview.widget import ListWidget,ItemView


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
        
        

        self.top_frame_list = QFrame()
        self.top_frame_list.setProperty("class",["bg-secondary","top-frame"])
        self.top_frame_list.setMinimumHeight(55)
        
        
        self.top_frame_layout =QVBoxLayout(self.top_frame_list)
        self.top_frame_layout.setContentsMargins(10,10,10,10)
        self.top_frame_layout.setSpacing(0)
        
        
        self.top_label_list = QLabel()
        self.top_label_list.setText("Resultado da sua busca".upper())
        self.top_label_list.setProperty("class",["text-white",
                                                 "fs-2",
                                                 "fs-wg-8"])
        
        
        self.top_label_list.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.top_frame_layout.addWidget(self.top_label_list)
        
        
        self.search_input = InputButton(
            text="Pesquise o modelo da sua placa aqui"
            
            )
        
        
        self.list_search = ListWidget(relative=self.content_frame)
        
        
        for _ in range(24):
            self.item = QListWidgetItem()
            self.item_widget = ItemView()
            # self.item.setText("Tesete")
            self.list_search.addItem(self.item)
            self.list_search.setItemWidget(self.item,self.item_widget)
        
        
        self.list_layout.addWidget(self.top_frame_list)
        self.list_layout.addWidget(self.list_search)
        
        
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addItem(self.spacer_h)
        self.search_layout.addWidget(self.list_frame)
        
        
        self.content_layout.addWidget(self.search_frame)
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
        