from PyQt6 import QtWidgets,QtCore,QtGui
from diskrecuperar.utils.manager.image import ImageManager


class Window(QtWidgets.QMainWindow,ImageManager):
    def __init__(self,parent=None) -> None:
        super().__init__(parent=parent)
        
        # self.layoutV = QtWidgets.QVBoxLayout()
        
        # self.customTop()
        
    @property
    def _geometry(cls) -> QtCore.QRect:
        return  QtGui.QGuiApplication.primaryScreen().geometry()
    
    @property
    def center(cls)->QtCore.QPoint:
        return cls._geometry.center()    
    
    
    @property
    def w(cls)->QtCore.QPoint:
        return  cls._geometry.width()  
    
    @property
    def h(cls)->QtCore.QPoint:
        return  cls._geometry.height()
    
    
    def setHeight(self,widget:QtWidgets.QWidget,height:int):
        widget.setMaximumHeight(height)
        widget.setMinimumHeight(height)
        
        
    def removeSpacing(self,layout:QtWidgets.QBoxLayout):
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
    def setFrameLess(self):
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        
    def show(self) -> None:
        
       
        return super().show()




