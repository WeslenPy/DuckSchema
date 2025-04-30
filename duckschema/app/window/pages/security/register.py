from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSvgWidgets import *
from PySide6.QtSvg import *
from duckschema.utils.manager.image import ImageManager
from duckschema.app.components.input.widget import InputPassword,InputEmail
from duckschema.app.components.button.widget import PushButton
from duckschema.app.components.message.popup import PopUp
from duckschema.api.diskapi.api import RequestManager

class RegisterPage(QWidget):
    def __init__(self, parent:QStackedWidget = None,pages=None) -> None:
        super().__init__()
        self.stack:QStackedWidget = parent
        
        self.manager = ImageManager()
        self.request = RequestManager()
        
        self.setup()
        
    def setup(self):
        

        self.spacer_v = QSpacerItem(10,10,
                            QSizePolicy.Policy.Minimum,
                            QSizePolicy.Policy.Expanding)
    
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5,10,0,10)
        
        self.content_frame = QFrame()
        
        self.logo_frame = QFrame()
        
        self.form_frame = QFrame()
        self.buttons_frame = QFrame()
        
        self.logo_layout = QVBoxLayout(self.logo_frame)
        self.logo_layout.setContentsMargins(10,10,10,10)
        self.logo_layout.setSpacing(0)
        
        
        self.label_logo = QLabel()
        self.label_subtitle = QLabel()
        self.label_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_logo.setPixmap(self.manager.get_png(filename="icon"))
        self.label_subtitle.setText("Cadastre-se aqui:")
        self.label_subtitle.setProperty("class",["fs-2","font-robot",
                                                 "fs-w-400","mt-2"])
        
        
        self.logo_layout.addWidget(self.label_logo)
        self.logo_layout.addWidget(self.label_subtitle)
        
        
        self.form_layout = QVBoxLayout(self.form_frame)
        self.form_layout.setContentsMargins(0,40,0,0)
        
        
        self.input_email = InputEmail(text="exemplo@gmail.com")
        self.input_password = InputPassword(text="*******")
        
        
        self.form_layout.addWidget(self.input_email)
        self.form_layout.addWidget(self.input_password)
        
    
        self.buttons_layout = QVBoxLayout(self.buttons_frame)
        self.buttons_layout.setContentsMargins(0,0,0,50)
        
        
        self.register_btn = PushButton(name="Registrar")
        self.back_btn = PushButton(name="Voltar")
      
        self.back_btn.clicked.connect(self.changePage)
        self.register_btn.clicked.connect(self.checkRegister)
        
        self.register_btn.setProperty("class",["btn-login",
                                            "mb-2","fs-2"])
        
        
        self.back_btn.setProperty("class",["btn-transparent",
                                               "fs-2"])
        
        
        self.buttons_layout.addWidget(self.register_btn)
        self.buttons_layout.addWidget(self.back_btn)
        
        self.content_layout = QVBoxLayout(self.content_frame)
        
                
        self.popup = PopUp(self)
        self.content_layout.addWidget(self.popup)
        
        self.content_layout.addWidget(self.logo_frame)
        self.content_layout.addWidget(self.form_frame)
        self.content_layout.addItem(self.spacer_v)
        self.content_layout.addWidget(self.buttons_frame,alignment=Qt.AlignmentFlag.AlignBottom)
        
        self.main_layout.addWidget(self.content_frame)
        
        self.stack.addWidget(self)
                
         
        
    def responseData(self,response:dict):
        
        data:dict = response.get("data",{})
        
        message:dict = data.get("message","Erro ao processar dados!")
        error = data.get("error",True)
        if error:
            return self.popup.showMessageError(
                message=message)      
            
            
        self.popup.showMessageSuccess(
                message=message,onclick=self.changePage) 
        
            
    def checkRegister(self):
        
        email = self.input_email.text()
        password = self.input_password.text()
        
        if not self.input_email.checkField():
            return self.popup.showMessageError(
                message="Preencha o campo de e-mail corretamente!") 
        
              
        elif not self.input_password.checkField():
            return self.popup.showMessageError(
                message="Preencha o campo de senha corretamente!") 
        
        
        self.request.post(
                        url=self.request.url.register,
                        data=dict(email=email,
                                    password=password))

        
        self.request.request_finished.connect(self.responseData)
    
        
        
        
    def changePage(self):
        self.stack.setCurrentIndex(0)