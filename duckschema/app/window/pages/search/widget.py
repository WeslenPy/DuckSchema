from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *
from duckschema.utils.manager import debouce
from duckschema.utils.manager.image import ImageManager
from duckschema.app.components.input.widget import InputSearch
from duckschema.app.components.listview.widget import ListWidget,ItemView
from duckschema.api.diskapi.api import RequestManager
from duckschema.utils.manager.debouce import Debounce
from duckschema.app.components.message.popup import PopUp

class SearchPage(QWidget):
    def __init__(self, parent:QStackedWidget = None,pages=None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent
        
        
        self.page =1
        self.limit =20
        
        self.page_end = False
        
        self.manager = ImageManager()
        self.request = RequestManager()
        self.request_next_page = RequestManager()
        
        self.request.request_finished.connect(self.responseData)
        self.request_next_page.request_finished.connect(lambda response:self.responseData(response=response,
                                                                                          clear=False
                                                                                          ))
        
        
        
        
        self.pages =pages
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
        
        
        self.debounce = Debounce(callback=self.searchArchive,timeout_ms=800)
        
        self.search_input = InputSearch(
            text="Pesquise o modelo da sua placa aqui"
            )
        
        self.search_input.editingFinished.connect(self.debounce.call)
        
        self.list_search = ListWidget(relative=self.content_frame)
        
        self.list_search.more.connect(self.nextPage)
        
        self.popup = PopUp(self)
        
        self.search_layout.addWidget(self.popup)
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addItem(self.spacer_h)
        self.search_layout.addWidget(self.list_search)
        
        self.content_layout.addWidget(self.search_frame)
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
        
        
    def nextPage(self):
        if not self.page_end:
            filtered = self.search_input.text()
            
            if filtered:
                self.page +=1
                data = {
                    "name":filtered,
                    "limit":20,
                    "page":self.page
                }
                
                self.request_next_page.query(url=self.request_next_page.url.archive_filter,data=data)
            
               
    def showMessage(self,data:dict):
        
        message:dict = data.get("message","Erro ao processar dados!")
        error = data.get("error",True)
        if error:
            return self.popup.showMessageError(
                message=message)      
            
            
        self.popup.showMessageSuccess(
                message=message) 
        
        
    def showMessageDownload(self,data:dict):
        message:dict = data.get("message","Erro ao processar dados!")
        error = data.get("error",True)
        if error:
            return self.popup.showMessageError(
                message=message,
                onclick=self.changePage
                )      

            
            
        self.popup.showMessageSuccess(
                message=message,
                ) 
        
    def changePage(self):
        
        self.stack.setCurrentWidget(self.pages.store_page)
        
    def responseData(self,response:dict,clear:bool=True):
        
        data:dict = response.get("data",{})
        archives:list[dict] = data.get("archives",[])
        
        
        if clear:
            self.list_search.clearItems()
        
        
        if len(archives)>0:
            self.search_layout.removeItem(self.spacer_h)
            
            
        if len(archives)<self.limit:
            self.page_end = True
        
        for archive in archives:
            
            filename= archive.get("name","")
            state_star = archive.get("favorite_children",[])           
            state_like = archive.get("like_children",[])     
            
             
            self.item = QListWidgetItem()
            self.item_widget = ItemView(_id=archive.get("id",""),
                                        filename=filename)
            
            
            if state_star:
                state_star = state_star[-1].get("status",False)
            
            if state_like:
                state_like = state_like[-1].get("status",False)
                
                
            self.item_widget.setText(text=filename)
            self.list_search.addItem(item=self.item)
            self.list_search.setItemWidget(self.item,self.item_widget)
            
            self.item_widget.onLike.connect(self.showMessage)
            self.item_widget.onStar.connect(self.showMessage)
            self.item_widget.onMessage.connect(self.showMessageDownload)
            
            self.item_widget.setStateLike(state_like)
            self.item_widget.setStateStar(state_star)
        
        
    def searchArchive(self):
        
        
        filtered = self.search_input.text()
        
        if filtered:
            
            self.page_end = False
            self.page = 1
            data = {
                "name":filtered,
                "limit":self.limit,
                "page":self.page
            }
            
            self.request.query(url=self.request.url.archive_filter,data=data)
            
