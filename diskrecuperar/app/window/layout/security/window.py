from diskrecuperar.app.components.window.widget import Window
from diskrecuperar.utils.manager.image import ImageManager
from diskrecuperar.database.model.admin.user import User
from PySide6 import QtWidgets, QtCore, QtGui
from diskrecuperar.database.config.conn import Session

import bcrypt


class LoginMain(Window):
    def __init__(self,parent:QtWidgets.QMainWindow=None):
        super().__init__(parent)
        
        self.window_parent = parent
        
        self.loginWidget = QtWidgets.QWidget(self)
        self.progress = 0
        
        self.FormLogin()
        self.InitGui()
        
    def FormLogin(self):

        
        self.frameTop = QtWidgets.QFrame(self.loginWidget)
        self.frameCenter = QtWidgets.QFrame(self.loginWidget)
        self.frameDown = QtWidgets.QFrame(self.loginWidget)
        self.frameMessage = QtWidgets.QFrame(self.loginWidget)
        self.frameLogin = QtWidgets.QFrame(self.loginWidget)
        self.frameProgress = QtWidgets.QFrame(self.loginWidget)

        self.lb_Message = QtWidgets.QLabel('Usuario Ou Senha Incorreto.',self.loginWidget)
        self.btn_Message  = QtWidgets.QToolButton(self.loginWidget)
        x_close_icon = ImageManager().get_ico_by_png("x_close")
        self.btn_Message.setIcon(x_close_icon)
        self.btn_Message.setIconSize(QtCore.QSize(7,7))

        self.lb_Message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.btn_Message.setMinimumSize(16,16)
        self.lb_Message.setMaximumWidth(220)
        
        self.frameTop.setMaximumHeight(40)
        self.frameDown.setMaximumHeight(40)
        self.frameTop.setMinimumHeight(40)
        self.frameDown.setMinimumHeight(40)
        self.frameMessage.setMaximumWidth(250)
        self.frameMessage.setMinimumHeight(28)
        self.frameProgress.setMaximumSize(420,420)
        self.frameProgress.setMinimumSize(420,420)
        self.frameLogin.setMinimumSize(410,410)
        self.frameLogin.setMaximumSize(410,410)

        self.frameLogin.setStyleSheet('QFrame{background-color:#333333;border-radius:10px;}')
        self.frameMessage.setStyleSheet('QFrame{background-color:red;border-radius:5px;}')
        self.frameProgress.setStyleSheet('''
        QFrame{ border-radius:15px;background-color:qconicalgradient(cx:0.5,cy:0.5,angle:90,stop:0.999 rgba(255,0,127,0),stop:1 rgba(85,170,255,255));}
        ''')

        self.btn_Message.setStyleSheet('QToolButton{background-color:rgba(255, 255, 0,200);border-radius:5px;}\
                                        QToolButton:hover{background-color:rgb(255, 255, 0);}')
        self.lb_Message.setStyleSheet('QLabel{color:white;}')

        self.setStyleSheet('QFrame{background-color:#1E1E1E;}')

        self.btn_Message.clicked.connect(lambda:self.Animation(rever=True))

        self.layoutV = QtWidgets.QVBoxLayout(self.loginWidget)
        self.layoutHLogin = QtWidgets.QHBoxLayout(self.frameCenter)
        self.layoutHTop = QtWidgets.QHBoxLayout(self.frameTop)
        self.layoutHMessage = QtWidgets.QHBoxLayout(self.frameMessage)
        self.layoutHProgress = QtWidgets.QHBoxLayout(self.frameProgress)

        
        self.layoutV.addWidget(self.frameTop)
        self.layoutV.addWidget(self.frameCenter)
        self.layoutV.addWidget(self.frameDown)

        self.layoutHLogin.addWidget(self.frameProgress)
        self.layoutHProgress.addWidget(self.frameLogin)
        self.layoutHTop.addWidget(self.frameMessage)
        self.layoutHMessage.addWidget(self.lb_Message)
        self.layoutHMessage.addWidget(self.btn_Message)

        self.layoutHMessage.setContentsMargins(0,0,0,0)
        self.layoutHProgress.setContentsMargins(0,0,0,0)
        self.layoutV.setContentsMargins(0,0,0,0)
        self.layoutHMessage.setSpacing(0)
        self.layoutV.setSpacing(0)
        self.frameMessage.hide()

        self.Form(self.frameLogin.size().width())

        self.timeProgress = QtCore.QTimer()
        self.timeProgress.timeout.connect(self.ProgressAnimation)


        self.setFrameLess()
        self.setCentralWidget(self.loginWidget)

    def ProgressAnimation(self):
        value = self.progress

        stylesheet = "QFrame{ border-radius:15px;background-color:qconicalgradient(cx:0.5,cy:0.5,angle:90,stop:{stop_1} rgba(255,0,127,0),stop:{stop_2} rgba(85,170,255,255));}"
        pro = (100 -value) /100.0
        newStyle = stylesheet.replace('{stop_1}',str(pro-0.001)).replace('{stop_2}',str(pro))
        self.frameProgress.setStyleSheet(newStyle)

        self.progress+=1
        if self.progress >=100:
            self.timeProgress.stop()
            self.window_parent()
            self.close()

    def Animation(self,rever=False):

        self.frameMessage.show()
        pos = int(self.size().width()/2)-125

        self.animation = QtCore.QPropertyAnimation(self.frameMessage,b'pos')
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QtCore.QEasingCurve.Type.OutBounce)
        if not rever:self.animation.setStartValue(QtCore.QPoint(pos,-29)),self.animation.setEndValue(QtCore.QPoint(pos,10))
        else:self.animation.setStartValue(QtCore.QPoint(pos,10)),self.animation.setEndValue(QtCore.QPoint(pos,-29))
        self.animation.start()

    def Login(self,user:str,password:str):
        with Session() as session:
            user:User = session.query(User).filter(User.username==user).first()
            if user and user.check_password(password=password):
                self.timeProgress.start(0)
            else:
                self.Animation()

    def Form(self,width):

        icon_tp = ImageManager().get_png("user4.png")
        self.IconTp = QtWidgets.QLabel(self.frameLogin)
        
        self.IconTp.setPixmap(icon_tp)

        self.et_senha = QtWidgets.QLineEdit(self.frameLogin)
        self.btn_open= QtWidgets.QToolButton(self.frameLogin)
        self.cb_users = QtWidgets.QComboBox(self.frameLogin)
        
        
        with Session() as session:
            self.users:list[User] = User.find_users(session=session)

        self.cb_users.addItems([i.username for i in self.users])

        self.cb_users.setStyleSheet('''
        QComboBox{border:None;border-radius:12px;background-color:#595959;color:white;padding-left:%s px;}
        QComboBox:drop-down{border:0px solid;;border-radius:10px;image:url(Icons/ICONS_16/drop2.png);padding-top:4px;margin-top:2px;margin-right:3px;}
        QComboBox:drop-down:hover {background:#22c1c3;border:None;}
        QComboBox QAbstractItemView{max-width:200px;min-height:15px;padding-top:5px;border-bottom:2px solid rgba(85,170,255,255);padding-left:%s px;padding-bottom:3px;background-color:#404040;color:white;border-radius:10px;selection-background-color:#404040;outline:0px;}
        ''' % (int(90- len(self.cb_users.currentText())), int(87- len(self.cb_users.currentText()))) )


        self.et_senha.setStyleSheet('QLineEdit{border:None;border-radius:12px;background-color:#595959;color:white;font-size:12px;padding-left:5px;}\
                                     QLineEdit:hover{border:1.5px solid rgba(85,170,255,255);outline:0;}')

        self.btn_open.setStyleSheet('QToolButton{color:white;font-size:10pt;border:2px solid rgba(85,170,255,255);border-radius:12px;text-align:right;}\
                                     QToolButton:hover{background:rgba(85,170,255,255);border:None;outline:0;}')

        self.cb_users.setMaxVisibleItems(3)
        self.cb_users.resize(width,28)
        self.cb_users.setMaximumWidth(200)

        self.et_senha.setMaxLength(30)

        self.cb_users.move(int(width/2-200/2),165)
        self.IconTp.move(int(width/2-self.IconTp.size().width()/2),50)

        self.et_senha.setFocus()
        self.et_senha.setPlaceholderText('Senha')
        self.btn_open.setText('Logar')

        self.et_senha.returnPressed.connect(lambda:self.Login(self.cb_users.currentText(),self.et_senha.text()))
        self.btn_open.pressed.connect(lambda:self.Login(self.cb_users.currentText(),self.et_senha.text()))

        self.et_senha.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.et_senha.resize(width,28)
        self.et_senha.setMaximumWidth(200)
        self.et_senha.move(int(width/2-200/2),200)

        self.btn_open.resize(width,28)
        self.btn_open.setMaximumWidth(200)
        self.btn_open.move(int(width/2-200/2),250)


    def InitGui(self):

        self.setGeometry(200, 200, 600,450)
        self.setMinimumSize(600,600)
        self.move(self.center -self.rect().center() - QtCore.QPoint(0,20))
        self.show()


