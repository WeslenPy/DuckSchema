
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class ToolTip(QLabel):
    
    def __init__(self, parent=None,relative=None):
        super().__init__(parent=parent)
        
        self.hide()
        
        self.relative:QWidget =relative
        
        self.setProperty("class",["tooltip"])
        self.setMinimumHeight(36)
        self.setMinimumWidth(140)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjustSize()

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
        
    def setTitle(self,title:str):
        self.setText(title)
         
    def endAnimation(self,hide:bool):
        self.setHidden(hide)
               
    def callAnimation(self):
        self.timer.timeout.connect(lambda:self.moveToolTip(True,True))
        self.timer.start()
   
    def moveToolTip(self,invert:bool=False,hide:bool=False,duration:int=850):

        pos =   self.relative.pos()
        
        pos_x = pos.x() + self.relative.width() + 12
        pos_y = pos.y() + self.height() +5
        
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
        