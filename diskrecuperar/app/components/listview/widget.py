
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from diskrecuperar.app.components.button.widget import PushAction

from diskrecuperar.utils.manager.path import BasePath
from diskrecuperar.utils.manager.download import DownloadTask

from PyQt6.QtCore import QThreadPool
class ListWidget(QListWidget):
    
    def __init__(self, parent=None,relative:QWidget=None):
        
        super().__init__(parent=parent)
        
        # self.hide()
        
        self.parentWindow:QMainWindow =parent
        
        self.relative:QWidget = relative
        

        self.setProperty("class",["list-view"])

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(self.shadow)

        self.opacity = QGraphicsOpacityEffect(self)
        self.opacity.setOpacity(0.85)
        self.setGraphicsEffect(self.opacity)
        
 
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.setTimerType(Qt.TimerType.CoarseTimer)
        
         
         
    def endAnimation(self,hide:bool):
        self.setHidden(hide)
               
    def callAnimation(self):
        self.timer.timeout.connect(lambda:self.moveToolTip(True,True))
        self.timer.start()
   
    def moveToolTip(self,invert:bool=False,hide:bool=False,duration:int=850):
        gp = self.relative.mapToGlobal(QPoint(0, 0))

        pos = self.parentWindow.mapFromGlobal(gp)
        
        pos_x = pos.x() + self.relative.width() + 12
        pos_y = pos.y()-15 + (self.height()// 2)
        
        old_point =  QRect(pos.x()+self.width()+self.relative.width(),pos.y(),self.width(),self.height())
        point = QRect(pos_x,pos_y,self.width(),self.height())
        
        self.animation = QPropertyAnimation(self,b"geometry")
        self.animation.setStartValue(old_point if not invert else point)
        self.animation.setEndValue(point if not invert else old_point)
        self.animation.setDuration(duration)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        
        self.animation_opacity = QPropertyAnimation(self.opacity, b"opacity")
        self.animation_opacity.setStartValue(0 if not invert else 1 )
        self.animation_opacity.setEndValue(1 if not invert else 0)
        self.animation_opacity.setDuration(duration)
        
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.animation)
        self.anim_group.addAnimation(self.animation_opacity)
        
        self.anim_group.finished.connect(lambda:self.endAnimation(hide=hide))
        self.anim_group.start()
        
        self.timer.stop()
        
        
        
        
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
        
        label_title = QLabel()
        
        label_title.setText("teste")
        label_title.setProperty("class",["text-white","fs-2","fs-w-400"])
        
        self.button_download = PushAction(icon="download")
        self.button_download.clicked.connect(self.onclickDownload)         
        
        self.button_cancel = PushAction(icon="cancel")
        # self.button_cancel.clicked.connect(self.onclickCancel) 
        self.button_cancel.setProperty("class",["btn-cancel"])
        self.button_cancel.hide()
        
        self.button_like = PushAction(icon="like")
        self.button_like.clicked.connect(self.onclickLike)
        
        self.button_star = PushAction(icon="star")
        self.button_star.clicked.connect(self.onclickStar)        
        
        self.button_open_folder = PushAction(icon="folder_open")
        self.button_open_folder.clicked.connect(self.onclickOpenFolder)
        self.button_open_folder.hide()
        
        
        actions_layout.addWidget(label_title)
        actions_layout.addWidget(self.button_star)
        actions_layout.addWidget(self.button_like)
        actions_layout.addWidget(self.button_download)
        actions_layout.addWidget(self.button_cancel)
        actions_layout.addWidget(self.button_open_folder)
        
        
        
        container_layout.addWidget(actions_frame)
        container_layout.addWidget(self.progress_bar_download)
        
        
        
        self.setLayout(container_layout)
        

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


        
            
    def closeEvent(self, event: QCloseEvent):
        print("🛑 Cancelando todas as tarefas...")
        for task in self.tasks:
            task.setCancel()
            

        self.pool.waitForDone(3000)  
        
        return super().closeEvent(event)
