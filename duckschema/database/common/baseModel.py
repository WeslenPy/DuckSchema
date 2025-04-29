from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    select,
    desc,
)
from sqlalchemy.orm import Session
from duckschema.database.config.conn import get_session


class BaseModel:
    __table_args__: dict[str, str] = {'mysql_engine': 'InnoDB'}
    __mapper_args__: dict[str, bool] = {'always_refresh': True}
    # __abstract__ = True

    _id = Column(Integer, primary_key=True, name='id')

    _created_at = Column(
        DateTime,
        name='created_at',
        nullable=False,
        default=datetime.now,
        insert_default=datetime.now,
    )

    _update_at = Column(
        DateTime,
        name='update_at',
        nullable=False,
        default=datetime.now,
        insert_default=datetime.now,
        onupdate=datetime.now,
    )

    _status = Column(
        Boolean,
        name='status',
        nullable=False,
        default=True,
    )

    @property
    def id(cls) -> Column[int]:
        return cls._id

    @property
    def status(cls) -> Column[bool]:
        return cls._status

    @property
    def created_at(cls) -> Column[datetime]:
        return cls._created_at

    @property
    def update_at(cls) -> Column[datetime]:
        return cls._update_at


    @classmethod
    def get_first_row(cls,rows):
        
        with get_session() as session:
            
            return session.scalars(select(*rows
                                    ).order_by(desc(cls._id))).first()


    def save(self, session: Session=None):
        with get_session(session=session) as _session:
            _session:Session
            
            _session.add(instance=self)
            _session.commit()
            _session.refresh(instance=self)
            
                
        return self

    def delete(self, _id: int, session: Session=None) -> bool:
        session = get_session(session=session)
        
        row = session.query(self).filter(self.id == _id).first()

        if row:
            session.delete(instance=row)
            session.commit()
            return True

        return False

    def update(self, data: dict, session: Session=None):
        session = get_session(session=session)
        
        for key, value in data.items():
            if key == 'id':
                continue

            if getattr(self, key, 'not_found') != 'not_found':
                setattr(self, key, value)

        session.commit()
        return self
