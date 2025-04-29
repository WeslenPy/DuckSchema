from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import create_engine
from typing import Generator
import contextlib


uri = "sqlite:///Storage.db?check_same_thread=False"
pool_size = 0
pool_recycle =0
max_overflow = 0
pool_timeout = 0

engine = create_engine(uri,pool_size=pool_size,max_overflow=max_overflow,
                       pool_recycle=pool_recycle,pool_timeout=pool_timeout)
                                                 
# Session = sessionmaker(bind=engine,autoflush=True)


@contextlib.contextmanager
def get_session(session=None) : # type: ignore
    with Session(bind=engine, expire_on_commit=False) as session:
        yield session
