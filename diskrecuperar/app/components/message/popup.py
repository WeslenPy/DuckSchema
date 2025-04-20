

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QEnterEvent, QFocusEvent, QKeyEvent, QWheelEvent
from PySide6.QtWidgets import *
from diskrecuperar.utils.manager.money import MoneyManager
from diskrecuperar.app.components.icon.widget import Icon
from diskrecuperar.app.components.button.widget import PushAction

from diskrecuperar.utils.manager.image import ImageManager


class PopUp(QFrame):
    
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        
        self.setup()
        
        
    def setup(self):
    
    
        self.closeMessage()
    
        self.spacer_h = QSpacerItem(10,10,
                        QSizePolicy.Policy.Expanding,
                        QSizePolicy.Policy.Minimum)
        
         
        self.frame_content = QFrame()
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
                                         QFrame{
                                           background-color:#ff5252;
                                           border :none; 
                                           border:2px solid #ff5252;
                                           border-radius:10px;
                                         }
                                         """)
        
        self.frame_layout = QHBoxLayout(self.frame_content)
        self.frame_layout.setContentsMargins(10,10,10,10)
        self.frame_layout.setSpacing(0)
        
        self.message_label = QLabel()
        self.message_label.setProperty("class",["fs-1"])
        
        self.btn_close = PushAction(icon="cancel")
        self.btn_close.setProperty("class",["btn-cancel"])
        
        
        self.btn_close.clicked.connect(self.closeMessage)
        
        
        
        
        
        # self.frame_layout.addItem(self.spacer_h)
        self.frame_layout.addWidget(self.message_label)
        self.frame_layout.addWidget(self.btn_close)
        
        
        # self.setMaximumWidth(100)
        self.setMaximumHeight(50)
        
        self.setLayout(self.frame_layout)
        
        
        
        
        
    def showMessageSuccess(self,message,onclick=None):
        
        self.setStyleSheet("""
                            QFrame{
                            background-color:#45c484;
                            border :none; 
                            border:2px solid #45c484;
                            border-radius:10px;
                            color:white;
                            }
                            """)
        
        
        self.btn_close.setStyleSheet("""
                    QPushButton{
                        border:none;
                        border-radius: 10px;
                        background-color:rgba(0,0,0,0.7);
                        color: white;

                        padding-left:10px;
                        padding-right:10px;
                        max-width: 10px;
                    }

                    QPushButton:hover{
                        background-color:rgba(58, 54, 54, 0.7);
                    }
                    """)
        
        
        self.btn_close.clicked.connect(self.closeMessage)
        
        if onclick:
            self.btn_close.clicked.connect(onclick)
        
        
        self.message_label.setText(message)
        self.setHidden(False)
        
    def showMessageError(self,message):
        self.setHidden(False)
        self.message_label.setText(message)
        
        self.btn_close.clicked.connect(self.closeMessage)
               
        
        self.btn_close.setStyleSheet("""
                    QPushButton{
                         border:none;
                        border-radius: 10px;
                        background-color:  #c94f2b;
                        background:   #c94f2b;
                        color: white;

                        padding-left:10px;
                        padding-right:10px;
                        max-width: 10px;
                    }

                    QPushButton:hover{
                        background-color:  rgb(175, 46, 7);
                        background:   rgb(175, 46, 7);
                        color:#000;
                    }
                    """)

        self.setStyleSheet("""
                    QFrame{
                    background-color:#ff5252;
                    border :none; 
                    border:2px solid #ff5252;
                    border-radius:10px;
                    color:white;
                    
                    }
                    """)
        
    def closeMessage(self):
        self.setHidden(True)