from .db import Base
from pydantic import BaseModel
from sqlalchemy import (Column, String)

class URLShortner(Base):
    __tablename__ = "async_test"
    id = Column(String(32), primary_key=True)
    original_url = Column(String(255))
    short_url = Column(String(7), unique=True)

class URLRequest(BaseModel):
    original_url: str

class URLResponse(URLRequest):
    short_url: str
    id: str
    class Config:
        orm_mode = True