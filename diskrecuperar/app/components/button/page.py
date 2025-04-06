from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from diskrecuperar.app.components.button.widget import PushButton


class ButtonPage(PushButton):
    
    EXCLUDE = ["menu"]
    
    def __init__(self,parent:QMainWindow,name:str,title:str,
                 signal:Signal,
                 enabled:Signal,
                 layout:QBoxLayout,) -> None:
        
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
        
        
        
    def changePage(self,pages:QStackedWidget,page:QStackedWidget):
        pages.setCurrentWidget(page)
        self.signal.emit(self.name)

    def onPage(self,pages:QStackedWidget,page:QStackedWidget):
        self.clicked.connect(lambda: self.changePage(pages=pages,page=page))
        self.released.connect(self._createAnimation)
        
        
        
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
            
    @Slot()
    def signalDeactivate(self,name:str):
        
        if name==self.name:
            self.setChecked(True)
        else:
            if self.name not in self.EXCLUDE:
                self.setChecked(False)
            
        