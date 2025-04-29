
from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget
from duckschema.app.components.button.widget import PushAction

from duckschema.utils.manager.path import BasePath
from duckschema.utils.manager.download import DownloadTask,semaphore,tasking

from PySide6.QtCore import QThreadPool

from duckschema.api.diskapi.api import RequestManager


class ListWidget(QFrame):
    
    more = Signal(bool)
    
    
    def __init__(self, parent=None,relative:QWidget=None):
        
        super().__init__(parent=parent)

        self.relative:QWidget = relative

        self.setHidden(True)
        self.setup()
        
    def setPage(self,page:int):
        self.page=page
        
    def setup(self):
            
        self.list_frame = QFrame(self)
        
        self.list_layout = QVBoxLayout(self.list_frame)
        self.list_layout.setContentsMargins(10,0,10,0)
        self.list_layout.setSpacing(0)
                

        self.top_frame_list = QFrame()
        self.top_frame_list.setProperty("class",["bg-secondary","top-frame"])
        self.top_frame_list.setMinimumHeight(55)
        
        
        self.top_frame_layout =QVBoxLayout(self.top_frame_list)
        self.top_frame_layout.setContentsMargins(0,0,0,0)
        self.top_frame_layout.setSpacing(0)
        
        
        self.top_label_list = QLabel()
        self.top_label_list.setText("Resultado da sua busca".upper())
        self.top_label_list.setProperty("class",["text-white",
                                                 "fs-2",
                                                 "fs-wg-8"])
        
        
        self.top_label_list.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.top_frame_layout.addWidget(self.top_label_list)
        
        self.list_search = QListWidget()
        
        self.list_search.setProperty("class",["list-view"])
        
        self.scroll_search = self.list_search.verticalScrollBar()
        
        self.scroll_search.valueChanged.connect(self.moreItems)
        
        self.list_layout.addWidget(self.top_frame_list)
        self.list_layout.addWidget(self.list_search)
        
        self.setLayout(self.list_layout)
        
        
    def moreItems(self,currentIndex):
        
        if currentIndex>=self.scroll_search.maximum():
            self.more.emit(True)
        
        
    def clearItems(self):
        self.list_search.clear()
        
        
    def setItemWidget(self,item,widget):
        self.list_search.setItemWidget(item,widget)
        
    def addItem(self,item):
        
        self.setHidden(False)
        self.list_search.addItem(item)
         
        
        
class ItemView(QWidget):
    
    
    onLike = Signal(dict)
    onStar = Signal(dict)
    onMessage = Signal(dict)
    onCancel = Signal(dict)
    
    
    _liked = False
    _stared = False
    
    
    def __init__(self, parent=None, _id:int=None,filename=None,
                 directory:str=None,**kwargs):
        
        
        super().__init__(parent=parent,**kwargs)
        
        self.directory =directory
        
        self.filename=filename
        
        self.id = _id
        
        self._setup()
        
        self.pool = QThreadPool()
     
        self.request_like= RequestManager()
        self.request_star= RequestManager()
        self.request_download= RequestManager()
        
                 
        self.task = DownloadTask(
                            filename=self.filename
                            )
    
    
        self.task.signals.ondownload.connect(self.checkOnDownload)
        
        self.task.signals.progress.connect(self.progress_bar_download.setValue)
        self.task.signals.finished.connect(self.progressFinish)
        
        self.request_like.request_finished.connect(
            self.onResponseLike)
        
        
        self.request_download.request_finished.connect(
            self.onResponseURL)
        
        self.request_star.request_finished.connect(
            self.onResponseStar)
        
        
    def resetLayout(self,layout:QLayout):
        
        layout.setContentsMargins(5,5,5,5)
        layout.setSpacing(0)
        
    def _setup(self):
        
        container_frame = QFrame()
        actions_frame = QFrame()
        
        
        container_layout = QVBoxLayout(container_frame)
        actions_layout = QHBoxLayout(actions_frame)
        
        self.resetLayout(container_layout)
        self.resetLayout(actions_layout)
        
        
        self.progress_bar_download = QProgressBar()
        self.progress_bar_download.setMaximumHeight(10)
        self.progress_bar_download.setRange(0, 100)
        self.progress_bar_download.hide()
        
        self.label_title = QLabel()
        self.label_title.setStyleSheet("")
        
        self.label_title.setProperty("class",["text-white","fs-2","fs-w-400"])
        
        
        self.button_download = PushAction(icon="download")
        self.button_download.clicked.connect(self.getURLDownload)         
        
        self.button_cancel = PushAction(icon="cancel")
        self.button_cancel.clicked.connect(self.onclickCancel)
        self.button_cancel.setProperty("class",["btn-download-cancel"])
        self.button_cancel.hide()
        
        self.button_like = PushAction(icon="like")
        self.button_like.clicked.connect(self.onclickLike)
        
        self.button_star = PushAction(icon="star")
        self.button_star.clicked.connect(self.onclickStar)        
        
        self.button_open_folder = PushAction(icon="folder_open")
        self.button_open_folder.clicked.connect(self.onclickOpenFolder)
        self.button_open_folder.hide()
        
        
        actions_layout.addWidget(self.label_title)
        actions_layout.addWidget(self.button_star)
        actions_layout.addWidget(self.button_like)
        actions_layout.addWidget(self.button_download)
        actions_layout.addWidget(self.button_cancel)
        actions_layout.addWidget(self.button_open_folder)
        
        
        
        container_layout.addWidget(actions_frame)
        container_layout.addWidget(self.progress_bar_download)
        
        
        
        self.setLayout(container_layout)
        
        
    def setStateStar(self,state:bool):
        
        
        if state:
            self.button_star._setIconItem("star_fill")
        else:
            self.button_star._setIconItem("star")    
            
    def setStateLike(self,state:bool):
        
        if state:
            self.button_like._setIconItem("like_fill")    
        
        else:
            self.button_like._setIconItem("like")    
            

        
    def setText(self,text:str):
        self.label_title.setText(text)
        # self.label_title.setToolTip(text)
        

    def setURLDownload(self,url:str):
        self.url = url
        
    def onclickOpenFolder(self):
        if self.directory:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.directory)))
        
    def onclickCancel(self):
        global tasking
        
        
        self.task.setCancel()
        
        self.button_cancel.hide()
        self.button_download.show()
        self.progress_bar_download.hide()
        
        tasking=False
        
    def onResponseURL(self,response:dict):
        data:dict = response.get("data",{})
        error = data.get("error",True)
        
        
        if not error:
            url = data.get("url","")
            self.onclickDownload(url=url)
        
        self.onMessage.emit(data)        
        
        
        
    def getURLDownload(self):
        global tasking
        
        if not semaphore.available() or tasking:
            return self.checkOnDownload(
                available=semaphore.available() or not tasking)
        
        tasking = True

        self.onStar.emit(
                {
                    "message":"Verificando se o arquivo esta disponivel, aguarde....",
                    "error":False
                })
            
        self.request_download.query(
                        url=self.request_download.url.archive_download,
                        data={"id":self.id},
                        )
        
    def onclickDownload(self,url:str):
        
        self.directory = str(QFileDialog.getExistingDirectory(self,
                                                    "Selecione o diretorio.",
                                                    BasePath.get_download_dir()
                                                    ))
        
        if self.directory:
            self.progress_bar_download.show()
            self.button_download.hide()
            self.button_cancel.show()
            self.progress_bar_download.setValue(0)
   
            self.task.setFolder(folder=self.directory)
            self.task.setURL(url=url)
     
            # task.signals.velocity.connect(lambda msg: print(msg))
            # task.signals.error.connect(lambda msg: print(msg))
            
            # task.signals.cancel.connect()
       
            self.pool.start(self.task)
            
    def checkOnDownload(self,available:int):
        if not available:
            self.onStar.emit(
                {"message":"Aguarde o download anterior finalizar!",
                "error":True})
            
            
    def onResponseStar(self,response:dict):
        data:dict = response.get("data",{})
        error = data.get("error",True)
        
        favorite:dict = data.get("favorite",{})
        
        
        self._stared = favorite.get("status",False)
        
        if self._stared:
            self.button_star._setIconItem("star_fill")
        else:
            self.button_star._setIconItem("star")    
    
        self.onStar.emit(data)        
    
        
        
    def onResponseLike(self,response:dict):
        data:dict = response.get("data",{})
        error = data.get("error",True)
        
        like:dict = data.get("like",{})
        
        self._liked = like.get("status",False)
        
        if self._liked:
            self.button_like._setIconItem("like_fill")    
        
        else:
            self.button_like._setIconItem("like")    
            
                
        self.onLike.emit(data)        
    
    def onclickLike(self):
        
        self.request_like.query(url=self.request_like.url.archive_like,
                          data={"id":self.id})
        
        
    def onclickStar(self):
        self.request_star.query(url=self.request_star.url.archive_favorite,
                          data={"id":self.id})
        

        
    def progressFinish(self):
        global tasking


        self.progress_bar_download.hide()
        
        self.button_download.show()
        self.button_open_folder.show()
        self.button_cancel.hide()
        tasking=False
        
        
        self.onStar.emit(
                {"message":"Download finalizado com sucesso!",
                "error":False})
            
        
            
    def stopTasks(self):
        self.task.setCancel()

        # self.pool.waitForDone(3000)  
        