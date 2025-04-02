from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSvgWidgets import *
from PyQt6.QtSvg import *
from src.utils.manager.image import ImageManager

class HomePage(QWidget):
    def __init__(self, parent:QStackedWidget = None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent
        
        self.manager = ImageManager()
        
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.setTimerType(Qt.TimerType.CoarseTimer)
        
        self.setup()
        
        
    def resizeLogo(self,event:QResizeEvent):pass
        
        
    def animatedOnEnter(self,event:QEnterEvent):
        
        point_up = QRect(self.logo_svg.x(),self.logo_svg.y()-50,self.logo_svg.width(),self.logo_svg.height())
        point_down = QRect(self.logo_svg.x(),self.logo_svg.y(),self.logo_svg.width(),self.logo_svg.height())
        
        self.animation_up = QPropertyAnimation(self.logo_svg,b"geometry")
        self.animation_up.setStartValue(point_down)
        self.animation_up.setEndValue(point_up)
        self.animation_up.setDuration(1500)
        # self.animation_up.setEasingCurve(QEasingCurve.Type.In)        
        
        self.animation_down = QPropertyAnimation(self.logo_svg,b"geometry")
        self.animation_down.setStartValue(point_up)
        self.animation_down.setEndValue(point_down)
        self.animation_down.setDuration(1000)
        # self.animation_down.setEasingCurve(QEasingCurve.Type.InCurve)
        
        self.anim_group = QParallelAnimationGroup()
        self.anim_group.addAnimation(self.animation_down)
        self.anim_group.addAnimation(self.animation_up)
        # self.anim_group.setLoopCount(20)
        
        self.anim_group.start()
        # self.animation_up.start()
        # self.animation_down.start()
        
    
    
    def animatedOnLeave(self,event:QEvent):
        self.timer.stop()
        

    def setup(self):
        self.spacer_frame = QSpacerItem(10,10,
                                        QSizePolicy.Policy.Expanding,
                                        QSizePolicy.Policy.Minimum)
        
        
        self.spacer_h = QSpacerItem(10,10,
                                    QSizePolicy.Policy.Minimum,
                                    QSizePolicy.Policy.Expanding)
        
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5,10,0,10)
        self.main_layout.setSpacing(0)
        
        self.content_frame = QFrame()
        
        self.content_layout = QHBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(10,10,0,10)
        self.content_layout.setSpacing(0)
        
        
        self.logo_frame = QFrame()
        self.logo_layout = QVBoxLayout(self.logo_frame)
        self.logo_layout.setContentsMargins(0,0,0,0)
        self.logo_layout.setSpacing(0)
        
        
        self.content_frame.setProperty("class",["bg-primary","border-0"])
        

        self.file_path= self.manager.get_svg_logo("logo")
        self.logo_size = QSvgRenderer(self.file_path)
        self.logo_svg = QSvgWidget(self.file_path)
        self.logo_svg.setFixedSize(420,150)
        
        self.logo_svg.leaveEvent = self.animatedOnLeave
        # self.logo_svg.enterEvent = self.animatedOnEnter
        
        self.content_frame.resizeEvent = self.resizeLogo
        # self.logo_svg.setFixedSize(self.logo_size.defaultSize())
                 
        
        self.logo_layout.addItem(self.spacer_h)
        self.logo_layout.addWidget(self.logo_svg,alignment=Qt.AlignmentFlag.AlignCenter)
        self.logo_layout.addItem(self.spacer_h)
        
        self.content_layout.addWidget(self.logo_frame)
      
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
        
        