from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from diskrecuperar.app.components.grip.widget import (GripTop,
                                                      GripBottom,
                                                      GripRight,
                                                      GripLeft)



from diskrecuperar.app.components.button.page import ButtonWindow
from diskrecuperar.app.window.stack.manager import PageLogin
from diskrecuperar.app.components.window.widget import Window
from PySide6 import QtCore,QtGui
from diskrecuperar.utils.manager.css import CssManager
from diskrecuperar.utils.manager.image import ImageManager

from diskrecuperar.app.window.layout.home.window import Home




class Login(Window):
    
    WIDTH =80
    HEIGHT = 40
    
    activeSignal = Signal(str)
    enabledSignal = Signal(bool)
    
    
    def __init__(self):
        super().__init__()
        
        self.setMinimumSize(500,720)
        self.point_step = QtCore.QPoint()
        self.point_step.setX(-100)
        self.point_step.setY(-10)
        
        self.css_manager = CssManager()
        self.img_manager = ImageManager()
        
        self.setup()
        
        self.show()
     
        
    def setMarginsLayout(self):
        self.title_layout.setContentsMargins(0,0,0,0) 
        
        
    def showMax(self):
        self.setMarginsLayout()
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
            
    def doubleClickEvent(self,event:QtGui.QMouseEvent):
        self.showMax()
        
    def moveWindow(self,event:QtGui.QMouseEvent):

        if  self.isMaximized():
            self.setMarginsLayout()
            self.showNormal()
            self.move(event.pos()+self.point_step)
            
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            position = event.globalPosition().toPoint() 
            
            self.move(self.pos() + position- self.dragPos)
            self.dragPos =  event.globalPosition().toPoint()
            event.accept()     
            
            if position.y()==0:
                self.setMarginsLayout()
                self.showMaximized()
                
                
        super().mouseMoveEvent(event)
        event.accept()
        
    def mousePressEvent(self, event:QtGui.QMouseEvent) -> None:
        self.dragPos =  event.globalPosition().toPoint()
        super().mouseMoveEvent(event)
        event.accept()
        
        
   
            
    def setup(self):
        
        
        
        #FRAME DO TITLE BAR
        
        self.main_frame = QFrame(self)
        self.main_frame.setProperty("class",["bg-primary","frame-radius"])
        
        
        #FRAME ABAIXO DO TITLE BAR
        self.box_frame = QFrame()
        self.box_frame.setProperty(
            "class",["bg-primary","frame-radius"])  
        
        
        # self.box_frame.setMaximumWidth(200)      
        
        self.title_layout = QVBoxLayout(self.main_frame) # TOP LAYOUT
        self.removeSpacing(self.title_layout)
        self.setMarginsLayout()
        
        
        self.main_layout = QHBoxLayout(self.box_frame)# BOX LAYOUT
        self.removeSpacing(layout=self.main_layout)  

        
        self.btn_window = ButtonWindow()
        
        
        #FRAME DO TITLE BAR
        self.title_frame = QFrame()
        self.title_frame.setMaximumHeight(30)
        self.title_frame.setMinimumHeight(30)
        self.title_frame.setProperty(
            "class",["bg-primary","frame-radius-top"])
        
        self.title_frame.mouseMoveEvent = self.moveWindow
        self.title_frame.mouseDoubleClickEvent = self.doubleClickEvent
        
        self.tool_layout = QHBoxLayout(self.title_frame)
        self.removeSpacing(self.tool_layout)
        
        self.spacer = QSpacerItem(20,20,
                                  QSizePolicy.Policy.Expanding,
                                  QSizePolicy.Policy.Minimum)

        # CUSTOM BUTTONS DO TITLE BAR
        
        self.btn_window.closeBtn.connect(lambda:self.close())
        self.btn_window.minBtn.connect(lambda:self.showMinimized())
        self.btn_window.maxBtn.connect(self.showMax)
        
        self.tool_layout.addItem(self.spacer)
        self.tool_layout.addWidget(self.btn_window.min_btn)
        self.tool_layout.addWidget(self.btn_window.max_btn)
        self.tool_layout.addWidget(self.btn_window.close_btn)
        
        
           
        self.pages = QStackedWidget()
        self.manager_pages = PageLogin(stack=self.pages)
        
        # DEFINE A PRIMEIRA PAGE
        self.pages.setCurrentWidget(self.manager_pages.login_page) 
        
        
        self.manager_pages.login_page.change_window.connect(self.changeToHome)
        
        
        self.content_frame = QFrame()
        
        self.content_layout = QVBoxLayout(self.content_frame)
        self.removeSpacing(layout=self.content_layout)
        
        self.top_grip = GripTop(self)
        self.left_grip = GripLeft(self)
        self.right_grip = GripRight(self)
        self.bottom_grip = GripBottom(self)
        
        
        self.top_grip.setup(self.title_layout)
     
        self.title_layout.addWidget(self.title_frame)
        self.title_layout.addWidget(self.box_frame)
        
        self.left_grip.setup(self.main_layout)
        
        # self.main_layout.addWidget(self.side_frame)
        self.main_layout.addWidget(self.content_frame)
        
        self.content_layout.addWidget(self.pages)        
        
        self.right_grip.setup(self.main_layout)
        
        self.bottom_grip.setup(self.title_layout)
        
        self.setFrameLess()
        self.setCentralWidget(self.main_frame)
        
        self.setProperty("class",["bg-primary"])
        
        self.setWindowIcon(self.img_manager.get_ico_by_png("icon"))



    def changeToHome(self):
        Home().show()
        self.close()
        
    def resizeEvent(self, event:QResizeEvent):
    #    print(event.size())
    #    print(self.isFullScreen(),self.isMaximized())
        if self.isMaximized() or self.isFullScreen():
            self.bottom_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            
        else:
            
            self.bottom_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()