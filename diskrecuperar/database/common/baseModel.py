
from sqlalchemy import Integer,Column,DateTime,Boolean
from diskrecuperar.database.config.base import Model
from sqlalchemy.orm.session import Session
from datetime import datetime

class BaseModel(Model):
    __mapper_args__= {'always_refresh': True}
    __abstract__=True

    id  = Column(Integer, primary_key=True,autoincrement=True)
    
    status = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime,default=datetime.now,nullable=False)
    update_at = Column(DateTime,default=datetime.now,nullable=False,onupdate=datetime.now)
    
    
    def __init__(self, status=True,created_at=datetime.now,update_at=datetime.now):
        
        
        
        self.status=status
        self.created_at= created_at()
        self.update_at= update_at()
        
        
        
        
    def save_model(self,session:Session=None)->None:
        from diskrecuperar.database.config.conn import Session
        if session is None:session = Session()
        session.add(self)
        session.commit()
        session.close()
        return self
    