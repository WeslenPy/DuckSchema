from __future__ import annotations

from sqlalchemy import Column, String, select
from sqlalchemy.orm import Mapped,Session

from diskrecuperar.database.common.baseModel import BaseModel
from diskrecuperar.database.config import Model

from diskrecuperar.utils.encrypt.provider import EncryptProvider



class Auth(BaseModel, Model):
    __tablename__: str = 'auth'

    token: Mapped[str] = Column(String(length=100), nullable=False)

    _email: Mapped[str] = Column(
        String(length=100), 
        name="email",
        nullable=False, unique=True
    )

    _password: Mapped[str] = Column(String(length=100),
                                    name="password", nullable=False)
    
    
    @property
    def email(self):
        return self._email
        
    @property
    def password(self):
        return self._password
    
    
    @email.getter
    def email(self):
        return EncryptProvider().decrypt_field(self._email)

    @password.getter
    def password(self):
        return EncryptProvider().decrypt_field(self._password)
    
    
    @email.setter
    def email(self,value):
        email=  EncryptProvider().encrypt_field(value)

        self._email = email

    @password.setter
    def password(self,value):
        
        password = EncryptProvider().encrypt_field(value)
        
        self._password = password


    def __init__(self, token: str, 
                        email: str, 
                        password: str, **kwargs):
        
        super().__init__(**kwargs)
        
        self.token = token
        self.email = email
        self.password = password
        
        
        
        
    @classmethod
    def get_first_row(cls):
        
        return super().get_first_row(
            rows=[cls._email,cls._password,cls.token])

    @classmethod
    def get_user_by_email(
        cls, email: str, session: Session
    ) -> Auth:
        user = session.scalar(select(cls).where(cls.email == email))

        return user
