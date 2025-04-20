
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QEnterEvent, QFocusEvent, QKeyEvent, QWheelEvent
from PySide6.QtWidgets import *
from diskrecuperar.utils.manager.money import MoneyManager
from diskrecuperar.app.components.icon.widget import Icon
from diskrecuperar.app.components.button.widget import PushButton

from diskrecuperar.utils.manager.image import ImageManager


class InputText(QFrame):
    
    
    @property
    def editingFinished(cls):
        return cls.input_field.editingFinished
    
    @property
    def textChanged(cls):
        return cls.input_field.textChanged
    
    
    
    def __init__(self,parent=None,text:str=""):
        super().__init__(parent=parent)
        
        self.parentWindow = parent
        self.textPlaceHolder = text

        self._setup()
        
    def _setup(self):
        
        self.layout_h = QHBoxLayout()
        
        self.input_field = QLineEdit()
        
        self.input_field.setPlaceholderText(self.textPlaceHolder)
        self.input_field.setProperty("class",["form-input"])
        
        
        self.setMaximumHeight(70)
        self.input_field.setMaximumHeight(70)
        
        self.layout_h.addWidget(self.input_field)
        
        self.layout_h.setSpacing(0)
        self.layout_h.setContentsMargins(0,0,0,0)
        
        self.setLayout(self.layout_h)
        
            
    def value(self):
        try:return float(self.text())
        except: return 0
        
    def resetField(self):
        self.clear()
        
    def setText(self, text: str) -> None:
        text = str(text)
        return self.input_field.setText(text)
           
    def selectAll(self) -> None:
        if self.text():
            return self.input_field.selectAll()
    
    def setValidator(self,regex:QRegularExpressionValidator):
        self.input_field.setValidator(regex)
    
    def setAlignment(self,alignment:Qt.AlignmentFlag):
        self.input_field.setAlignment(alignment)
        
    def setCursorPosition(self,pos:int):
        self.input_field.setCursorPosition(pos)
        
    def clear(self):
        self.input_field.clear()
        
    def addAction(self,action,position):
        return self.input_field.addAction(action,position)
    
    def setCompleter(self,completer:QCompleter):
        return  self.input_field.setCompleter(completer)
        
    def text(self):
        return self.input_field.text()
    
    def installEventFilter(self,event:QEvent):
        return self.input_field.installEventFilter(event)
        
    def setPlaceholderText(self,text:str):
        return self.input_field.setPlaceholderText(text)
    
    def setProperty(self, name: str, value: list) -> bool:
        return self.input_field.setProperty(name,value)
    
    
    def focusOutEvent(self, e: QFocusEvent) -> None:
        
        text= self.input_field.text()
        validator  = self.input_field.validator()
        
        if validator and  not validator.validate(text,0) or len(text)<=0:
            self.setProperty("class",["form-input","border-warning",])
            self.invalid = "1"
        else:pass
        
        return  self.input_field.focusOutEvent(e)
    
    
class InputForm(QFrame):
    
    
    @property
    def editingFinished(cls):
        return cls.input_field.editingFinished
    
    @property
    def textChanged(cls):
        return cls.input_field.textChanged
    
    
    
    def __init__(self,parent=None,text:str=""):
        super().__init__(parent=parent)
        
        self.parentWindow = parent
        self.textPlaceHolder = text
        
        self.image = ImageManager()
        
        
        self.styled = """
          QFrame{
                border:none;
                border: 1.5px solid {{color}};
                border-radius: 10px;
                background-color: #FFFFFF;
                padding-right: 10px;
                
            }
            
            QFrame:hover{
                border: 1.5px solid #45c484;
            }
        """
        
        
        self.normal = self.styled.replace(
            "{{color}}","rgba(58, 54, 54, 0.9)")        
        
        
        self.focus = self.styled.replace(
            "{{color}}","#45c484")
        
        

        self._setup()
        
        
        
    def focusInputIn(self,e:QFocusEvent):
        
        self.frame_control.setStyleSheet(self.focus)

        self.funcs[0](e)
        
        return  e.accept()
        
        
    def focusInputOut(self,e:QFocusEvent):
        self.frame_control.setStyleSheet(self.normal)
        
        self.funcs[1](e)
        
        return  e.accept()
        
    def _setup(self):
        
        
        
        self.main_layout = QVBoxLayout()
        
        self.frame_control = QFrame()
        self.frame_control.setFrameShape(QFrame.Shape.StyledPanel)
        
        self.layout_h = QHBoxLayout(self.frame_control)
        
        self.label_control = QLabel()
        self.label_control.setProperty("class",["fs-2",
                                                "font-robot",
                                                "fs-w-400"])
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(self.textPlaceHolder)
        self.input_field.setProperty("class",["form-control"])
        self.input_field.setFrame(False)
        self.input_field.setCursor(Qt.CursorShape.PointingHandCursor)
        
        
        self.icon_btn = QPushButton()
        self.icon_btn.setIcon(self.image.get_svg(filename="eye_open"))
        self.icon_btn.setIconSize(QSize(22,22))
        self.icon_btn.setProperty("class",["btn-icon"])
        self.icon_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        
        
        self.funcs = [  self.input_field.focusInEvent,  self.input_field.focusOutEvent]
        
        self.input_field.focusInEvent = self.focusInputIn
        self.input_field.focusOutEvent = self.focusInputOut
        
            
        self.frame_control.setStyleSheet(self.normal)
       
                            
        # self.setMaximumHeight(70)
        self.input_field.setMinimumHeight(40)
        self.frame_control.setMinimumHeight(40)
        
        self.layout_h.addWidget(self.input_field)
        self.layout_h.addWidget(self.icon_btn)
        
        self.layout_h.setSpacing(0)
        self.layout_h.setContentsMargins(0,0,0,0)
        
        
        self.main_layout.addWidget(self.label_control)
        self.main_layout.addWidget(self.frame_control)
        
        self.setLayout(self.main_layout)
        
        
    def setTitle(self,text):
        self.label_control.setText(text)
        
    def setEcho(self,echo):
        self.input_field.setEchoMode(echo)
        
    def getEcho(self):
        return self.input_field.echoMode()
        
        
    def setHiddenIcon(self,hide):
        self.icon_btn.setHidden(hide)
        
    def setIcon(self,icon:QIcon):
        self.icon_btn.setIcon(icon)
        
            
    def value(self):
        try:return float(self.text())
        except: return 0
        
    def resetField(self):
        self.clear()
        
    def setText(self, text: str) -> None:
        text = str(text)
        return self.input_field.setText(text)
           
    def selectAll(self) -> None:
        if self.text():
            return self.input_field.selectAll()
    
    def setValidator(self,regex:QRegularExpressionValidator):
        self.input_field.setValidator(regex)
    
    def setAlignment(self,alignment:Qt.AlignmentFlag):
        self.input_field.setAlignment(alignment)
        
    def setCursorPosition(self,pos:int):
        self.input_field.setCursorPosition(pos)
        
    def clear(self):
        self.input_field.clear()
        
    def addAction(self,action,position):
        return self.input_field.addAction(action,position)
    
    def setCompleter(self,completer:QCompleter):
        return  self.input_field.setCompleter(completer)
        
    def text(self):
        return self.input_field.text()
    
    def installEventFilter(self,event:QEvent):
        return self.input_field.installEventFilter(event)
        
    def setPlaceholderText(self,text:str):
        return self.input_field.setPlaceholderText(text)
    
    def setProperty(self, name: str, value: list) -> bool:
        return self.input_field.setProperty(name,value)
    
    
    def focusOutEvent(self, e: QFocusEvent) -> None:
        
        text= self.input_field.text()
        validator  = self.input_field.validator()
        
        if validator and  not validator.validate(text,0) or len(text)<=0:
            self.setProperty("class",["form-input","border-warning",])
            self.invalid = "1"
        else:pass
        
        return  self.input_field.focusOutEvent(e)
    


class InputPassword(InputForm):
    
    ECHO = QLineEdit.EchoMode.PasswordEchoOnEdit
    
    def __init__(self, parent=None, text: str = ""):
        super().__init__(parent, text)
        
        self.setup()
        
    def setup(self):
        
        self.setEcho(self.ECHO)
        self.setTitle("Senha")
        
        
        self.icon_btn.clicked.connect(self.cleanPassword)
        
                
        
    def cleanPassword(self):
        
        if self.getEcho() == self.ECHO:
            self.setIcon(self.image.get_svg("eye_close"))
            self.setEcho(QLineEdit.EchoMode.Normal)
        else:
            self.setIcon(self.image.get_svg("eye_open"))
            self.setEcho(self.ECHO) 
        
        
class InputEmail(InputForm):
    
    def __init__(self, parent=None, text: str = ""):
        super().__init__(parent, text)
        
        self.setup()
        
    def setup(self):
        
        self.setEcho(QLineEdit.EchoMode.Normal)
        
        self.setTitle("E-mail")
        self.setHiddenIcon(True)
        

        
        
    
class InputNumber(InputText):
    invalid = "0"
    
    def __init__(self, parent=None, text: str = ""):
        super().__init__(parent, text)
        
        regex = QRegularExpression(r'^\d+$')

        self.setValidator(QRegularExpressionValidator(regex))
   
    def value(self):
        try:return int(self.text())
        except: return 0
        
        
class InputFloat(InputText):
    def __init__(self, parent=None, text: str = ""):
        super().__init__(parent, text)
        
        
        regex = QRegularExpression(r'^[\d.,]+$')

        self.setValidator(QRegularExpressionValidator(regex))
        
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.manager = MoneyManager()
        
        self.locale_currency = QLocale(QLocale.Language.Portuguese,QLocale.Country.Brazil)
        self.setLocale(self.locale_currency)        
        
        self.setText("0")
        # self.setInputMask("000.009,99;_")
        # self.textChanged.connect(self.parseCurrency)
        
        self.input_field.mousePressEvent = self.mousePressAll
        
    def mousePressAll(self,event:QMouseEvent):
        self.selectAll()
        return self.mousePressEvent(event)
        
        
    def parseCurrency(self,e:str):
        text = float(e.replace(",","."))
        
        self.setCursorPosition(len(e))
        self.setText(self.locale_currency.toCurrencyString(text))



class InputButton(InputText,Icon):
    def __init__(self,parent=None,text:str=""):
        super().__init__(parent=parent,text=text)

        self.list_items = []
        self.search_enable =False
        
        self.setup()
        
    def setup(self):

        button_action = PushButton()
        button_action.setMinimumHeight(30)
        button_action.setMaximumWidth(45)
        button_action._setIconItem("search")
        button_action.setProperty("class",["btn-search"])       
        
        
        self.layout_h.addWidget(button_action)
    
    
            
class InputSearch(InputText,Icon):
    def __init__(self,parent=None,text:str=""):
        super().__init__(parent=parent,text=text)

        self.list_items = []
        self.search_enable =False
        
        self.setup()
        
        self.input_field.mousePressEvent = self.mousePressAll
        
    def mousePressAll(self,event:QMouseEvent):
        self.selectAll()
        return self.mousePressEvent(event)
        
        
    def addSearchAction(self):
        
        search_action = self.search
        # search_action.set
        return  self.addAction(search_action,
                               QLineEdit.ActionPosition.TrailingPosition)
        
    def enabledSearch(self):
        self.search_enable  = not self.search_enable
        if self.search_enable:
            self.search_action.setIcon(self.cancel)
            
        else:
            self.clear()
            self.search_action.setIcon(self.search)
            
    def wheelEvent(self, e: QWheelEvent) -> None:
        return super().wheelEvent(e)
            
    def setup(self):
        
        
        self.search_action =self.addSearchAction()
        self.search_action.triggered.connect(self.enabledSearch)
        
        
         
        self.setAutoFillBackground(False)
        
        self.editingFinished.connect(self.addEntry)

        self.model = QStandardItemModel(self)
        
        self.completer_input = QCompleter(self.model, self)
        self.completer_input.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer_input.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer_input.setMaxVisibleItems(5)
        self.setCompleter(self.completer_input)
        
        self.installEventFilter(self.completer_input)
        self.installEventFilter(self.model)
        
        
        for row in self.list_items:
            self.model.appendRow(QStandardItem(row))
            
        
        self.setProperty("class",["form-input","input-search"])

    def addEntry(self):
        entryItem = self.text()
        self.list_items.append(entryItem)

        if not self.model.findItems(entryItem):
            self.model.appendRow(QStandardItem(entryItem))

