from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from duckschema.app.components.button.widget import PushButton


class ButtonPage(PushButton):
    
    EXCLUDE = ["menu"]
    
    def __init__(self,parent:QMainWindow,name:str,title:str,
                 signal:Signal,
                 enabled:Signal,
                 layout:QBoxLayout,
                 pages:QStackedWidget,
                 ) -> None:
        
        super().__init__(parent=parent,name=name,title=title)
        
        self.setToolTipMode(True)
        self.setText(None)
        
        self.parentWindow = parent
        
        self.signal:SignalInstance = signal
        self.enabled:SignalInstance = enabled
        self.layoutBox =layout
        
        self.setProperty("class",["btn-side","text-white"])
        
        self.min_width = 30
        self.min_height = 30
        self.size_btn = (self.min_width,self.min_height)
        
        self.pages =pages
        
    def changePage(self,pages:QStackedWidget,page:QStackedWidget):
        pages.setCurrentWidget(page)
        self.signal.emit(self.name)

    def onPage(self,pages:QStackedWidget,page:QStackedWidget):
        self.clicked.connect(lambda: self.changePage(pages=pages,page=page))
        self.released.connect(self._createAnimation)
        
        self.pages.currentChanged.connect(lambda:self.signalChange(toPage=page))
        
        
    def addSignal(self):
        self.enabled.connect(lambda mode: self.enableText(mode=mode))
        self.signal.connect(lambda name: self.signalDeactivate(name=name))
        
      
      
    def setPattern(self,tooltip:str,filename:str):
        
        self.setCheckable(True)
        self.setMinimumWidth(self.min_width)
        self._setIcon(filename)
        self.addSignal()
        
        
    @Slot()
    def enableText(self,mode:bool):
        self.setText("")
        if mode:  self.setText(self.title)
        
    def signalChange(self,toPage):
        
        if self.pages.currentWidget()==toPage:
            self.setChecked(True)
        else:
            if self.name not in self.EXCLUDE:
                self.setChecked(False)
            
    @Slot()
    def signalDeactivate(self,name:str):
        
        if name==self.name:
            self.setChecked(True)
        else:
            if self.name not in self.EXCLUDE:
                self.setChecked(False)
            
        
        
        
        
class ButtonWindow(QWidget):
    
    
        
    @property
    def maxBtn(cls):
        return cls.max_btn.clicked
            
    @property
    def minBtn(cls):
        return cls.min_btn.clicked
               
    @property
    def closeBtn(cls):
        return cls.close_btn.clicked
    
    
    def __init__(self):
        super().__init__()
        
        self.setup()
            
            
    def setup(self):
        
        
        self.close_btn = QToolButton()
        self.min_btn = QToolButton()
        self.max_btn = QToolButton()
        
        
        self.close_btn.setProperty("class",["btn-radius","bg-red"])
        self.min_btn.setProperty("class",["btn-radius","bg-green"])
        self.max_btn.setProperty("class",["btn-radius","bg-orange"])