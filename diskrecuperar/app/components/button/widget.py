
from PySide6.QtWidgets import QMainWindow
from diskrecuperar.utils.manager.image import ImageManager

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from diskrecuperar.app.components.tooltip.widget import ToolTip
from diskrecuperar.app.components.icon.widget import Icon

class PushButton(QPushButton,Icon):
    
    def __init__(self,parent:QMainWindow=None,
                 name:str="",title:str="") -> None:
        super().__init__(parent=parent)
        
        
        self.parentWindow = parent
        
        self.manager  =ImageManager()
        
        self.name= name
        self.title= title
        
        self.min_width = 20
        self.min_height = 20
        
        self.size_btn = (self.min_width,self.min_height)
        
        
        self.tooltip = ToolTip(parent=parent,relative=self)
        self.tooltip.setTitle(title=title)
        
        
        self.setText(self.name)
       
        self.tooltip_enable = False
        
    def setToolTipMode(self,mode:bool):
        self.tooltip_enable = mode
    
    
    def enterEvent(self,event:QEnterEvent):
        if self.tooltip_enable:
            self.tooltip.show()
            self.tooltip.moveToolTip()
        
    def leaveEvent(self, event:QEvent):
        if self.tooltip_enable:
            
            self.tooltip.callAnimation()


    def _setIcon(self,filename:str):
        path = self.get_menu_svg_icon(filename=filename)
        self.addIcon(path)
        
        
    def _setIconItem(self,filename:str):
        path = self.get_ico(filename=filename)
        self.addIcon(path)
     
    def addIcon(self,icon:QIcon):
        self.setIcon(icon)
        self.setIconSize(QSize(*self.size_btn))

    def _createAnimation(self):
        
        self.animation = QPropertyAnimation(self,b"minimumHeight")
        
        self.animation.setStartValue(self.min_height)
        self.animation.setEndValue(self.min_height+25)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.animation.start()
        
        self.animation.setStartValue(self.min_height+25)
        self.animation.setEndValue(self.min_height)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.animation.start()
        
        self.setMinimumWidth(self.min_width)
        
  
  
  
class PushAction(PushButton):
    def __init__(self, parent: QMainWindow = None,  icon: str = "",) -> None:
        super().__init__(parent, name='', title="")
        
        
        self.icon_find = icon
        self.setup()
        
        
    def setup(self):
        
        self.setMinimumHeight(30)
        self.setMaximumWidth(40)
        self._setIconItem(self.icon_find)
        self.setProperty("class",["btn-view"])