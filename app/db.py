from sqlalchemy import (Column, Integer, String, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel

DATABASE_URL = 'sqlite:///urlshortner.db'
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    dbase = SessionLocal()
    try:
        yield dbase
    except DBAPIError:
        dbase.close()
    finally:
        dbase.close()
        

class URLShortner(Base):
    __tablename__ = "shortned"
    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    short_url = Column(String(7), unique=True, index=True)

class URLRequest(BaseModel):
    url: str

class URLResponse(URLRequest):
    short_url: str
    class Config:
        orm_mode = True

# Base.metadata.create_all(bind=engine) after alembic this is not needed