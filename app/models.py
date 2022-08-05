from .db import Base
from pydantic import BaseModel
from sqlalchemy import (Column, String)

class URLShortner(Base):
    __tablename__ = "url_srt"
    id = Column(String(32), primary_key=True)
    original_url = Column(String(255),unique = True)
    code = Column(String(7), unique = True)
    short_url = Column(String(255))

class URLRequest(BaseModel):
    original_url: str

class URLResponse(URLRequest):
    code: str
    short_url: str
    id: str
    class Config:
        orm_mode = True