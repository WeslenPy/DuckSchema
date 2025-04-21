
from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget
from diskrecuperar.app.components.button.widget import PushAction

from diskrecuperar.utils.manager.path import BasePath
from diskrecuperar.utils.manager.download import DownloadTask

from PySide6.QtCore import QThreadPool



class ListWidget(QFrame):
    
    def __init__(self, parent=None,relative:QWidget=None):
        
        super().__init__(parent=parent)
        
        self.relative:QWidget = relative

        self.setHidden(True)
        self.setup()
        
        
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
        
        self.list_layout.addWidget(self.top_frame_list)
        self.list_layout.addWidget(self.list_search)
        
        self.setLayout(self.list_layout)
        
        
        
    def clearItems(self):
        self.list_search.clear()
        
        
    def setItemWidget(self,item,widget):
        self.list_search.setItemWidget(item,widget)
        
    def addItem(self,item):
        
        self.setHidden(False)
        self.list_search.addItem(item)
         
        
        
class ItemView(QWidget):
    
    
    
    def __init__(self, parent=None,url:str=None,
                 _id:int=None,directory:str=None,**kwargs):
        
        
        super().__init__(parent=parent,**kwargs)
        
        self.url = url or  "https://nbg1-speed.hetzner.com/100MB.bin"
        self.directory =directory
        
        self.id = _id
        self.pool = QThreadPool()
        
        self.tasks:list[DownloadTask] = []
        self._setup()
        
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
        
        self.label_title.setText("teste")
        self.label_title.setProperty("class",["text-white","fs-2","fs-w-400"])
        
        self.button_download = PushAction(icon="download")
        self.button_download.clicked.connect(self.onclickDownload)         
        
        self.button_cancel = PushAction(icon="cancel")
        # self.button_cancel.clicked.connect(self.onclickCancel) 
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
        
    def setText(self,text:str):
        self.label_title.setText(text)
        

    def setURLDownload(self,url:str):
        self.url = url
        
    def onclickOpenFolder(self):
        if self.directory:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.directory)))
        
    def onclickCancel(self,task:DownloadTask):
        task.setCancel()
        
        self.button_cancel.hide()
        self.button_download.show()
        self.progress_bar_download.hide()
        
    def onclickDownload(self):
        
        self.directory = str(QFileDialog.getExistingDirectory(self,
                                                    "Selecione o diretorio.",
                                                    BasePath.get_download_dir()
                                                    ))
        
        if self.directory:
            self.progress_bar_download.show()
            self.button_download.hide()
            self.button_cancel.show()
            
            task = DownloadTask(self.url,self.directory)
            
            self.progress_bar_download.setValue(0)
            
            task.signals.progress.connect(self.progress_bar_download.setValue)
            task.signals.finished.connect(self.progressFinish)
            task.signals.velocity.connect(lambda msg: print(msg))
            task.signals.error.connect(lambda msg: print(msg))
            
            # task.signals.cancel.connect()
            self.button_cancel.clicked.connect(
                lambda:self.onclickCancel(task))


            self.tasks.append(task)
            self.pool.start(task)
        
    
    def onclickLike(self):
        self.button_like._setIconItem("like_fill")    
        
        
    def onclickStar(self):
        self.button_star._setIconItem("star_fill")
        
        
        
    def progressFinish(self):


        self.progress_bar_download.hide()
        
        self.button_download.show()
        self.button_open_folder.show()
        self.button_cancel.hide()


        
            
    def stopTasks(self):
        print("🛑 Cancelando todas as tarefas...")
        for task in self.tasks:
            task.setCancel()

        self.pool.waitForDone(3000)  
        