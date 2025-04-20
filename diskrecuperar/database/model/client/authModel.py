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
    def email(cls):
        return cls._email
        
    @property
    def password(cls):
        return cls._password
    
    
    @email.getter
    def email(cls):
        return EncryptProvider().decrypt_field(cls.email)

    @password.getter
    def password(cls):
        return EncryptProvider().decrypt_field(cls.password)
    
    
    @email.setter
    def email(cls,value):
        email=  EncryptProvider().encrypt_field(value)

        cls._email = email

    @password.setter
    def password(cls,value):
        
        password = EncryptProvider().encrypt_field(value)
        
        cls._password = password


    def __init__(self, token: str, 
                        email: str, 
                        password: str, **kwargs):
        
        self.token = token
        self.email = email
        self.password = password
        
        
        
        
        

    @classmethod
    def get_user_by_email(
        cls, email: str, session: Session
    ) -> Auth:
        user = session.scalar(select(cls).where(cls.email == email))

        return user
