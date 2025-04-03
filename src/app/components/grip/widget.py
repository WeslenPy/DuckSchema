
from PyQt6.QtCore import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QWidget


class Grip(QWidget):
    def __init__(self, parent:QWidget=None) -> None:
        super().__init__(parent=parent)
        
        self._setup()
        
    def gripFrame(self)->QFrame:
        grip_frame = QFrame()
        grip_frame.setMinimumSize(QSize(10, 10))
        grip_frame.setMaximumSize(QSize(10, 10))
        grip_frame.setCursor(QCursor(Qt.CursorShape.SizeBDiagCursor))
        
        # grip_frame.setStyleSheet(u"background-color: transparent;")
        
        
        return grip_frame
    
    def addMinimun(self):
        self.center_grip.setMinimumSize(QSize(10, 0))
        
    def addCenterGrip(self):
        self.grip_layout.addWidget(self.center_grip)
    
    def addLeftGrip(self):
        self.grip_left = self.gripFrame()
        self.grip_left.setStyleSheet("background-color: rgba(250, 250, 250, 0.843);border-radius:5px;")
        
        
        self.grip_layout.addWidget(self.grip_left)
        
    def addRigthGrip(self):
        self.grip_right = self.gripFrame()
        self.grip_right.setStyleSheet("background-color: rgb(250, 250, 250);border-radius:5px;")
        
        
        # self.grip_right.setStyleSheet(u"background-color: transparent;")
        
        
        self.grip_layout.addWidget(self.grip_right)
        
    def _setup(self):
        
        self.container_grip = QFrame()
        self.container_grip.setMinimumSize(QSize(0, 10))
        # self.container_grip.setMaximumSize(QSize(16777215, 10))
        
        self.container_grip.setProperty("class",["bg-primary","br-5"])
        
        self.grip_layout = QHBoxLayout(self.container_grip)
        self.grip_layout.setContentsMargins(0, 0, 0, 0)
        self.grip_layout.setSpacing(0)
        
        self.center_grip = QFrame()
        self.center_grip.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
        self.center_grip.setProperty("class",["bg-primary","br-5"])
        
        self.setProperty("class",["bg-primary","br-5"])
        
        
        
            
    def geometryAnimated(self,new_size,window:QMainWindow,):

        self.animation = QPropertyAnimation(window,b"geometry")
        self.animation.setStartValue(window.geometry())
        self.animation.setEndValue(new_size)
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.OutElastic)
        self.animation.start()
                    
        
    def resizeTop(self,event:QMouseEvent,window:QMainWindow,):
        
        delta = event.pos()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)
        event.accept()
                
    def resizeLeft(self,event:QMouseEvent,window:QMainWindow,):
        
        
        delta = event.pos()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        
        # self.geometryAnimated(geo,window)
        window.setGeometry(geo)
        event.accept()
        
    def resizeBottom(self,event:QMouseEvent,window:QMainWindow,):
        delta = event.pos()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)
        event.accept()
        
        
    def resizeRight(self,event:QMouseEvent,window:QMainWindow,):
        
        delta = event.pos()
        width = max(window.minimumWidth(), window.width() + delta.x())
        # self.resizeAnimated(width,window)
        window.resize(width,window.height())
        event.accept()



class GripTop(Grip):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent=parent)
        
        self.parentWindow = parent
        
    def resizeWindow(self,event:QMouseEvent):
        return self.resizeTop(event=event,window=self.parentWindow)
        
        
    def hide(self):
        self.center_grip.hide()
        self.top_right.hide()
        self.top_left.hide()
        super().hide()
        
    def show(self):
        self.center_grip.show()
        self.top_right.show()
        self.top_left.show()
        
        
        super().show()
        
        
    def setup(self,layout:QBoxLayout):
        
        self.addLeftGrip()
        self.addCenterGrip()
        self.addRigthGrip()
        
        self.top_left = QSizeGrip(self.grip_left)
        self.top_right = QSizeGrip(self.grip_right)
                
        self.center_grip.mouseMoveEvent = self.resizeWindow
        
        # self.top_left.setStyleSheet("background: transparent")
        # self.top_right.setStyleSheet("background: transparent")
        
        # self.center_grip.setProperty("class",["bg-primary"])
        # self.top_right.setProperty("class",["bg-primary"])
        # self.top_left.setProperty("class",["bg-primary"])

        
        layout.addWidget(self.container_grip)
        
class GripBottom(Grip):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent=parent)
        
        self.parentWindow = parent
        
        # self.setProperty("class",["bg-primary"])
        
        
    def resizeWindow(self,event:QMouseEvent):
        return self.resizeBottom(event=event,window=self.parentWindow)
        
    
             
        
    def hide(self):
        self.center_grip.hide()
        self.top_right.hide()
        self.top_left.hide()
        
        super().hide()
        
           
    
    def show(self):
        self.center_grip.show()
        self.top_right.show()
        self.top_left.show()
        super().show()
        
    def setup(self,layout:QBoxLayout):
        
        self.addLeftGrip()
        self.addCenterGrip()
        self.addRigthGrip()
        
        self.top_left = QSizeGrip(self.grip_left)
        self.top_right = QSizeGrip(self.grip_right)
        
        self.center_grip.mouseMoveEvent = self.resizeWindow
        
        # self.top_left.setStyleSheet("background: transparent")
        # self.top_right.setStyleSheet("background: transparent")
        
        
        
        layout.addWidget(self.container_grip)
        
        
class GripLeft(Grip):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent=parent)
        
        self.parentWindow = parent
            

    def resizeWindow(self,event:QMouseEvent):
        return self.resizeLeft(event=event,window=self.parentWindow)
        
        
    def setup(self,layout:QBoxLayout):
        
        self.addCenterGrip()
        
        self.center_grip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.center_grip.mouseMoveEvent = self.resizeWindow
        layout.addWidget(self.container_grip)
        
        
        
        self.addMinimun()
        
    
    def show(self):
        self.center_grip.show()
        super().show()
        
        
    def hide(self):
        self.center_grip.setMinimumHeight(0)
        self.center_grip.hide()
        super().hide()
        

        
        
class GripRight(Grip):
    def __init__(self, parent:QWidget=None):
        super().__init__(parent=parent)
        
        self.parentWindow = parent
        
        
    def resizeWindow(self,event:QMouseEvent):
        return self.resizeRight(event=event,window=self.parentWindow)
        
        
    def setup(self,layout:QBoxLayout):
        
        self.addCenterGrip()
        self.center_grip.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.center_grip.mouseMoveEvent = self.resizeWindow
        layout.addWidget(self.container_grip)
        
        
        self.addMinimun()

        
    def hide(self):
        self.center_grip.hide()
        super().hide()
        
    
    def show(self):
        self.center_grip.show()
        super().show()
        
        