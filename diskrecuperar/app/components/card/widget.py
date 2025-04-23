

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QEnterEvent, QFocusEvent, QKeyEvent, QWheelEvent
from PySide6.QtWidgets import *
from diskrecuperar.utils.manager.money import MoneyManager
from diskrecuperar.app.components.icon.widget import Icon
from diskrecuperar.app.components.button.widget import PushAction

from diskrecuperar.utils.manager.image import ImageManager


class Card(QFrame):
    
    clicked = Signal(str)
    
    def __init__(self,parent=None,_id=None):
        super().__init__(parent=parent)
        
        self.id=_id
        self.manager = ImageManager()
        
        self.setup()
        
        
    def setup(self):
    
        self.spacer_h = QSpacerItem(10,10,
                        QSizePolicy.Policy.Expanding,
                        QSizePolicy.Policy.Minimum)
        
         
        self.frame_content = QFrame()
        self.text_frame = QFrame()
        
        self.setFrameShape(QFrame.Shape.NoFrame)
        
        self.setProperty("class",["card"])
        
  
        
        self.frame_layout = QHBoxLayout(self.frame_content)
        self.frame_layout.setContentsMargins(15,10,15,5)
        self.frame_layout.setSpacing(0)
        
        
        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.manager.get_svg("passkey"))
        self.icon_label.setMaximumWidth(40)
        
        
        self.text_layout = QVBoxLayout(self.text_frame)
        self.text_layout.setContentsMargins(15,10,15,5)
        self.text_layout.setSpacing(0)
        
        
        self.title_label = QLabel()
        self.title_label.setProperty("class",["fs-card"])
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                
        
        self.price_label = QLabel()
        self.price_label.setProperty("class",["fs-money"])
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        
        self.text_layout.addWidget(self.title_label)
        self.text_layout.addWidget(self.price_label)
        
        
        self.btn_redirect = PushAction(icon="redirect")
        self.btn_redirect.clicked.connect(self.clickedCard)
        
        self.mouseDoubleClickEvent = self.mouseDoubleClick
        
        
        self.frame_layout.addWidget(self.icon_label)
        self.frame_layout.addWidget(self.text_frame)
        self.frame_layout.addWidget(self.btn_redirect)
        
        
        self.setMaximumHeight(80)
        
        self.setLayout(self.frame_layout)
        
    def clickedCard(self):
        self.clicked.emit(str(self.id))
        
        
    def mouseDoubleClick(self,event:QMouseEvent):
        self.clicked.emit(str(self.id))
        
    
    def setTitle(self,text:str):
        self.title_label.setText(text)
        
    def setMoney(self,text:str):
        self.price_label.setText('R$ '+ f"{text:0.2f}".replace(".",","))
    
    def closeMessage(self):
        self.setHidden(True)