from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from diskrecuperar.app.components.grip.widget import (GripTop,
                                                      GripBottom,
                                                      GripRight,
                                                      GripLeft)



from diskrecuperar.app.components.button.page import ButtonPage,ButtonWindow
from diskrecuperar.app.window.stack.manager import PageManager
from diskrecuperar.app.components.window.widget import Window
from PySide6 import QtCore,QtWidgets,QtGui
from diskrecuperar.utils.manager.css import CssManager
from diskrecuperar.utils.manager.image import ImageManager

from diskrecuperar.app.components.message.widget import MessageBox


class Home(Window):
    
    WIDTH =80
    HEIGHT = 40
    
    activeSignal = Signal(str)
    enabledSignal = Signal(bool)
    
    def __init__(self) -> None:
        super().__init__()
        
        # self.app = parent
        
        
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
            
    def expandWindow(self,event:QtGui.QMouseEvent):
        print(event.globalPosition())
        
        
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
        
        
    def expandCollapse(self):
        self.btn_menu_page.setChecked(False)
        self.enabledSignal.emit(False)
        side_width = self.side_frame.width()
        
        max_width = self.WIDTH
        if side_width==max_width:
            self.btn_menu_page.setChecked(True)
            self.enabledSignal.emit(True)
            max_width = 240

        self.animation = QPropertyAnimation(self.side_frame,b"minimumWidth")
        self.animation.setStartValue(side_width)
        self.animation.setEndValue(max_width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.animation.start()
        
   
            
    def setup(self):
        
        #FRAME DO TITLE BAR
        
        self.main_frame = QFrame(self)
        self.main_frame.setProperty("class",["bg-primary","frame-radius"])
        
        
        #FRAME ABAIXO DO TITLE BAR
        self.box_frame = QFrame()
        self.box_frame.setProperty(
            "class",["bg-primary","frame-radius"])  
        # self.box_frame.setMaximumWidth(200)      
        
        
        #FRAME ABAIXO DO TITLE BAR
        self.box_right_frame = QFrame()
        self.box_right_frame.setProperty(
            "class",["bg-primary","frame-radius"])
        
        
        self.box_right_layout = QHBoxLayout(self.box_right_frame)
        self.removeSpacing(self.box_right_layout)
        
          
        self.title_layout = QVBoxLayout(self.main_frame)
        self.removeSpacing(self.title_layout)
        
        # self.title_layout.setProperty("class",["bg-white",])
        
        self.main_layout = QHBoxLayout(self.box_frame)
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
        
        
        #SIDE BAR BUTTONS 
        
        self.side_frame =QFrame()
        self.side_frame.setMaximumWidth(self.WIDTH)
        self.side_frame.setMinimumWidth(self.WIDTH)
        self.side_frame.setProperty("class",["bg-secondary","frame-radius"])
        
        self.pages_button_layout = QVBoxLayout(self.side_frame)
        self.pages_button_layout.setContentsMargins(5,10,5,10)
        self.pages_button_layout.setSpacing(5)
        
           
        self.pages = QStackedWidget()
        self.manager_pages = PageManager(stack=self.pages)
        
        self.pages.setCurrentWidget(self.manager_pages.search_page)
        
        btn_args_constants = dict(signal=self.activeSignal,
                                  enabled=self.enabledSignal,
                                  layout=self.pages_button_layout,
                                  pages=self.pages)
        
        
        #BUTTONS SIDE BAR
        self.btn_menu_page = ButtonPage(self,"menu","Menu",
                                        **btn_args_constants)
        self.btn_menu_page.clicked.connect(self.expandCollapse)
        self.btn_menu_page.setPattern("Menu","menu")
        
        self.btn_home_page = ButtonPage(self,"home","Home",
                                        **btn_args_constants)
        self.btn_home_page.onPage(self.pages,self.manager_pages.home_page)
        self.btn_home_page.setPattern("Home","home")
        
        self.btn_search_page = ButtonPage(self,"search","Pesquisar",
                                        **btn_args_constants)
        
        
        self.btn_search_page.onPage(self.pages,self.manager_pages.search_page)
        self.btn_search_page.setPattern("Pesquisar","search")                
        
        
        
                
        self.btn_store_page = ButtonPage(self,"cart","Comprar",
                                        **btn_args_constants)
        self.btn_store_page.onPage(self.pages,self.manager_pages.store_page)
        self.btn_store_page.setPattern("Comprar","cart")        


        self.spacer_side = QSpacerItem(20,20,
                                       QSizePolicy.Policy.Minimum,
                                       QSizePolicy.Policy.Expanding)

        self.pages_button_layout.addWidget(self.btn_menu_page)
        self.pages_button_layout.addWidget(self.btn_home_page)
        self.pages_button_layout.addWidget(self.btn_store_page)
        self.pages_button_layout.addWidget(self.btn_search_page)
        self.pages_button_layout.addItem(self.spacer_side)
        
        
        #FRAME BOTTOM BAR(ABAIXO DO TITLE BAR E DENTRO DO CONTENT)
        
        # self.bottom_bar = QFrame()
        # self.bottom_bar.setMaximumHeight(30)
        # self.bottom_bar.setMinimumHeight(30)
        # self.bottom_bar.setProperty("class",["bg-secondary",])
        
        
        # self.copy_label = QLabel()
        # self.copy_label.setText("Desenvolvedor: @WeslenPy")
        # self.copy_label.adjustSize()
        
        # self.copy_label.setProperty("class",["fs-robot","text-white","fs-2"])
        
        
        # self.tool_bottom_layout = QHBoxLayout(self.bottom_bar)
        # self.removeSpacing(layout=self.tool_bottom_layout)  
        
        
        # self.tool_bottom_layout.addWidget(self.copy_label,alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        self.content_frame = QFrame()
        # self.content_frame.setProperty("class",["bg-secondary","frame-radius"])
        
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
        
        self.main_layout.addWidget(self.side_frame)
        self.main_layout.addWidget(self.content_frame)
        
        self.content_layout.addWidget(self.pages)        
        # self.content_layout.addWidget(self.bottom_bar)    
        
        self.right_grip.setup(self.main_layout)
        
        self.bottom_grip.setup(self.title_layout)
        
            
        
        self.setFrameLess()
        self.setCentralWidget(self.main_frame)
        
        self.setProperty("class",["bg-primary"])
        
        self.setWindowIcon(self.img_manager.get_ico_by_png("icon"))

        
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