from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *
from diskrecuperar.utils.manager import debouce
from diskrecuperar.utils.manager.image import ImageManager
from diskrecuperar.app.components.card.widget import Card
from diskrecuperar.app.components.input.widget import InputSearch
from diskrecuperar.app.components.listview.widget import ListWidget,ItemView
from diskrecuperar.api.diskapi.api import RequestManager
from diskrecuperar.utils.manager.debouce import Debounce
from diskrecuperar.app.components.message.popup import PopUp


class StorePage(QWidget):
    def __init__(self, parent:QStackedWidget = None,pages=None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent
        
        self.manager = ImageManager()
        self.data = {}

        self.setup()

        self.stack.currentChanged.connect(self.getState)
            
        
    def getState(self,state:int):
        
        if state==2:
            self.getProduct()
        
    def setup(self):

        self.spacer_h = QSpacerItem(10,10,
                            QSizePolicy.Policy.Minimum,
                            QSizePolicy.Policy.Expanding)
    
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,0,0,0)
        self.main_layout.setSpacing(0)
        
        
        
        self.content_frame = QFrame()
        self.box_frame = QFrame()
 
        
        self.box_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.content_frame.setFrameShape(QFrame.Shape.NoFrame)
        
                
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(10,0,0,0)
        self.content_layout.setSpacing(0)
        
                        
        self.box_layout = QVBoxLayout(self.box_frame)
        self.box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.box_layout.setContentsMargins(0,0,10,0)
        self.box_layout.setSpacing(10)
        
        
        self.label_title = QLabel()
        self.label_title.setText("Compre sua licença")
        self.label_title.setProperty("class",["fs-title","mt-2"])
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        
        self.popup = PopUp(self)

        self.scroll_card = QScrollArea()
        self.scroll_card.setWidgetResizable(True) 
        # self.scroll_card
        
        self.scroll_card.setProperty("class",["border-around","bg-primary"])
        self.box_frame.setProperty("class",["bg-primary"])
       
        
        self.content_layout.addWidget(self.popup)
        self.content_layout.addWidget(self.label_title)
        self.content_layout.addWidget(self.box_frame)
        self.main_layout.addWidget(self.content_frame)
        
        
        self.scroll_card.setWidget(self.box_frame)
        self.main_layout.addWidget(self.scroll_card)
        
        self.stack.addWidget(self)  
        
        
    def responseData(self,response:dict):
        
        self.data:dict = response.get("data",{})
        products:list[dict]= self.data.get("products",[])
        
        for product in products:
            product_id =product.get("id","")
            
            self.card = Card(_id=product_id)
            self.box_layout.addWidget(self.card)
            self.card.setTitle(product.get("name"))
            self.card.setMoney(text=product.get("price"))
            
            self.card.clicked.connect( self.newPayment)
            
            
    def responsePayment(self,response:dict):
        data:dict = response.get("data",{})
        
        message:dict = data.get("message","Erro ao processar dados!")
        error = data.get("error",True)
        if error:
            return self.popup.showMessageError(
                message=message)      
            
            
        self.popup.showMessageSuccess(message=message)
        
        url=data.get("url","")
        
        url = QUrl(url)
        QDesktopServices.openUrl(url)
            
            
    def newPayment(self,product_id:int):
        print(product_id)
        
        self.popup.showMessageSuccess(message="Gerando link de pagamento....")
        
        self.request = RequestManager()
        
        self.request.query(
                        url=self.request.url.purchased_new,
                        data={"id":product_id})

        self.request.request_finished.connect(self.responsePayment)
        
            
    def getProduct(self):
        
        if not self.data:
            self.request = RequestManager()
            
            self.request.get(
                            url=self.request.url.product_list)

            self.request.request_finished.connect(self.responseData)