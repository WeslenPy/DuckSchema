
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget
from diskrecuperar.app.components.button.widget import PushAction



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
    def __init__(self, parent=None,**kwargs):
        super().__init__(parent=parent,**kwargs)
        
        self.url = None
        
        self._setup()
        
    def _setup(self):
        
        container_frame = QFrame()
        # container_frame.setMinimumHeight(100)
        
        container_layout = QHBoxLayout(container_frame)
        
        label_title = QLabel()
        
        label_title.setText("teste")
        label_title.setProperty("class",["text-white","fs-2","fs-w-400"])
        
        self.button_download = PushAction(icon="download")
        
        self.button_like = PushAction(icon="like")
        self.button_like.clicked.connect(self.onclick_like)
        
        self.button_star = PushAction(icon="star")
        self.button_star.clicked.connect(self.onclick_star)
        
        
        container_layout.addWidget(label_title)
        container_layout.addWidget(self.button_star)
        container_layout.addWidget(self.button_like)
        container_layout.addWidget(self.button_download)
        
        self.setLayout(container_layout)
        

    def setURLDownload(self,url:str):
        self.url = url
        
    def onclick_like(self):
        self.button_like._setIconItem("like_fill")    
        
        
    def onclick_star(self):
        self.button_star._setIconItem("star_fill")
        
        
        