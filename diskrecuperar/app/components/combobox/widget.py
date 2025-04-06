from diskrecuperar.app.components.listview.widget import ListView

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QCloseEvent, QDropEvent, QFocusEvent, QPaintEvent, QShowEvent
from PySide6.QtWidgets import *

class ComboBox(QFrame):

    def __init__(self,parent=None,holder:str=""):
        super().__init__(parent=parent)

        self.parentWindow=parent
        self.holder=holder
        self.placeholder = f"Selecione o seu {holder}"
        
        self.setup()
    
    def resetField(self):
        self.clear()
       
    def clear(self):
        return self.combobox.clear()
        
    def setup(self):
        
        self.layout_h = QVBoxLayout()
        
        self.combobox = QComboBox()        
        self.name_label = QLabel()
        
        self.name_label.setText(self.holder)
        self.name_label.setProperty("class",["text-white","text-left-small","fs-1"])
        
        
        self.setMaximumHeight(65)
        self.name_label.setMaximumHeight(20)
        self.combobox.setMaximumHeight(40)
        
        self.layout_h.addWidget(self.name_label)
        self.layout_h.addWidget(self.combobox)
        
        self.layout_h.setSpacing(0)
        self.layout_h.setContentsMargins(0,0,0,0)
        
        self.setLayout(self.layout_h)

        self.combobox.setMaxVisibleItems(5)
        self.combobox.setEditable(True)
        self.modelCustom = QStandardItemModel()
        
        
        self.completer_custom = QCompleter(self.modelCustom,self)
        self.combobox.setCompleter(self.completer_custom)
        self.combobox.setModel(self.modelCustom)
        
        
        self.combobox.setPlaceholderText(self.placeholder)
        self.combobox.setCurrentText(self.placeholder)
        
        
        self.combobox.addItems([str("text- "+ str(i)) for i in range(0,10)])
        self.combobox.setAutoFillBackground(False)
        
        
        
        self.combobox.setProperty("class",["form-box"])
        self.modelCustom.setProperty("class",["frame-radius"])