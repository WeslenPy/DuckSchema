from PyQt6.QtGui import QCloseEvent, QShowEvent
from src.app.components.window.widget import Window
from src.app.components.button.widget import PushButton

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from src.utils.manager.image import ImageManager


class MessageBox(Window):
    close_box = pyqtSignal(bool)
    accept_box = pyqtSignal(bool)
    
    
    @property
    def warning(cls):pass
    
    @property
    def info(cls)->dict[dict]:
        return {
            "icon":"info",
            "btn":{
                "okBtn":{
                    "hidden":False,
                    "text":"OK"
                }
            }
        }
        
    @property
    def quest(cls)->dict[dict]:
        return {
            "icon":"quest",
            "btn":{
                "confirmBtn":{
                    "hidden":False,
                    "text":"Sim"
                }, 
                "closeBtn":{
                    "hidden":False,
                    "text":"Não"
                },
            }
        }
            
    @property
    def success(cls)->dict[dict]:
        return {
            "icon":"confirm",
            "btn":{
                "okBtn":{
                    "hidden":False,
                    "text":"OK"
                }
            }
        }
        
        
    @property
    def danger(cls)->dict[dict]:
        return {
            "icon":"danger",
            "btn":{
                "okBtn":{
                    "hidden":False,
                    "text":"OK"
                }
            }
        }
    
     
    def __init__(self,window:QWindow):
        super().__init__()
        
        self.window_parent = window

        self.permit_close = False
        self.manager = ImageManager()
        
    def showMessage(self,text:str,settings:dict):
        
        self.setup()
        
        icon_name = settings.get("icon","help")
        self.icon_label.setPixmap(self.manager.get_svg(icon_name))
        
        config:dict = settings.get("btn",{})
        for key,value in config.items():
            if key in self.btn_dict:
                current:PushButton = self.btn_dict[key]
                current.setHidden(value.get("hidden",True))
                current.setText( value.get("text",""))
        
        
        self.resize(int(self.w/3),int(self.h/4))
        self.setTitle(text)
        self.setFrameLess()
        self.show()
        
        
    def showEvent(self, event:QEvent):
        if not event.spontaneous():
            geo = self.geometry()
            geo.moveCenter(self.window_parent.geometry().center())

    def setTitle(self,text:str):
        self.text_label.setText(text)

    def setup(self):
        
        self.spacer_h = QSpacerItem(20,20,QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        
        self.main_frame = QFrame(self)
        self.main_frame.setProperty("class",["bg-secondary","border-grey"])
        
        self.content_layout = QVBoxLayout(self.main_frame)
        
        self.top_frame = QFrame()
        self.bottom_frame = QFrame()
        self.bottom_frame.setMaximumHeight(60)
        
        self.left_frame = QFrame()
        self.right_frame  = QFrame()
        self.left_frame.setMaximumWidth(100)
        
        # self.left_frame.setMaximumWidth(60)
        
        self.left_layout = QHBoxLayout(self.left_frame)
        self.right_layout = QHBoxLayout(self.right_frame)
        
        self.top_layout = QHBoxLayout(self.top_frame)
        
        self.text_label = QLabel()
        self.text_label.adjustSize()
        self.text_label.setProperty("class",["text-white","fs-2"])  
        
        self.icon_label = QLabel()
        
        self.right_layout.addWidget(self.text_label,alignment=Qt.AlignmentFlag.AlignLeft)
        self.left_layout.addWidget(self.icon_label,alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        self.top_layout.addWidget(self.left_frame)
        self.top_layout.addWidget(self.right_frame)
        
        self.bottom_layout = QHBoxLayout(self.bottom_frame)
        
        self.close_btn = PushButton(self,"Cancelar","Cancelar")
        self.confirm_btn = PushButton(self,"Confirmar","Confirmar")
        self.ok_btn = PushButton(self,"OK","OK")
        
        self.close_btn.setMinimumSize(100,40)  
        self.ok_btn.setMinimumSize(100,40)  
        self.confirm_btn.setMinimumSize(100,40)  
        
        self.close_btn.setProperty("class",["btn","btn-red","border-0"])
        self.confirm_btn.setProperty("class",["btn","btn-green-dark","border-0"])
        self.ok_btn.setProperty("class",["btn","btn-green-dark","border-0"])
        
        self.close_btn.addIcon(self.close_btn.cancel)
        self.ok_btn.addIcon(self.ok_btn.confirm)
        self.confirm_btn.addIcon(self.confirm_btn.confirm)
        
        self.close_btn.clicked.connect(self.closeWindow)
        self.ok_btn.clicked.connect(self.closeWindow)
        self.confirm_btn.clicked.connect(self.confirmWindow)
        
        self.ok_btn.setHidden(True)
        self.close_btn.setHidden(True)
        self.confirm_btn.setHidden(True)
        
        self.bottom_layout.addItem(self.spacer_h)
        self.bottom_layout.addWidget(self.ok_btn)
        self.bottom_layout.addWidget(self.close_btn)
        self.bottom_layout.addWidget(self.confirm_btn)
        
        
        self.content_layout.addWidget(self.top_frame)
        self.content_layout.addWidget(self.bottom_frame)
        
        self.setCentralWidget(self.main_frame)
        
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        
        self.btn_dict:dict[PushButton] = {
            "confirmBtn":self.confirm_btn,
            "closeBtn":self.close_btn,
            "okBtn":self.ok_btn,
        }
        
        
    def closeEvent(self, e: QCloseEvent ) -> None:
        if not self.permit_close:return e.ignore()
        else:return super().closeEvent(e)
    
    def showEvent(self, e: QShowEvent) -> None:
        
        self.resize(int(self.w/3),int(self.h/4))
        self.move(self.pos())
        
        return super().showEvent(e)
    
    def closeWindow(self):
        self.permit_close=True
        self.close_box.emit(True)
        self.close()

    def confirmWindow(self):
        self.accept_box.emit(True)
        self.closeWindow()
