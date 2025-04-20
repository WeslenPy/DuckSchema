import bcrypt
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

class EncryptProvider:
    
    SECRET_KEY: bytes = urlsafe_b64encode(s=b"v/KHA<[L8BaPJ?2hXd:jFpe{Qy(+uVqU")
    
    
    def __init__(self) -> None:
        self.fernet = Fernet(key=self.SECRET_KEY)
    
    @staticmethod
    def verify(password:str,password_input:str)->str:
        return bcrypt.checkpw(
            password=str.encode(self=password),
            hashed_password=str.encode(self=password_input))
    
    
    @staticmethod
    def crypto(password:str)->str:
        return bcrypt.hashpw(
            password=str.encode(self=password),
            salt=bcrypt.gensalt(rounds=25,
                                prefix=str.encode(self="H2X21S")))
    
    
    
    def encrypt_field(self,field):
        return self.fernet.encrypt(str.encode(field)).decode()
    
     
    def decrypt_field(self,field):
        return self.fernet.decrypt(str.encode(field)).decode()
    
    