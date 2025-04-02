
from PyQt6 import QtWidgets,QtCore
from src.utils.manager.image import ImageManager



class LabelIcon(QtWidgets.QLabel):
    
    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.manager  =ImageManager()
        
        self.setProperty("cssClass","label-home")
        
    
    def createLabel(self,text:str,ico:str,layout:QtWidgets.QBoxLayout,space:int=0):
        self.setStyleSheet('')
        self.setMinimumSize(0,40)
            
        self.lb_text = QtWidgets.QLabel(self)
        self.lb_ico = QtWidgets.QLabel(self)
        
        self.lb_text.setText(text)
        
        self.lb_ico.setPixmap(self.manager.get_png(ico))
        self.lb_text.adjustSize()
        self.lb_text.move(int(self.lb_ico.size().width()/2),10)
        self.lb_ico.adjustSize()
        
        layout.addWidget(self,space,QtCore.Qt.AlignmentFlag.AlignBottom)
        
