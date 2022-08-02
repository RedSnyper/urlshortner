import hashlib
import base64
import databases
import sqlalchemy
import uuid
import logging 
from fastapi import FastAPI, status, HTTPException, Body
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import DBAPIError
from pydantic import BaseModel, HttpUrl, BaseSettings
from typing import List


class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str
    database_name : str
    database_username : str 
    
    class Config: 
        env_file = '.env'

settings = Settings()



DATABASE_URL = f"mysql+aiomysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# DATABASE_URL = "pymysql://postgres:admin123@localhost:5432/urlshortner"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

urls = sqlalchemy.Table(
    "test",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(32), primary_key = True),
    sqlalchemy.Column("original_url", sqlalchemy.String(255)),
    sqlalchemy.Column("short_url", sqlalchemy.String(7))
)

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)


class URLRequest(BaseModel):
    original_url: str

class URLResponse(URLRequest):
    short_url: str
    id: str
    class Config:
        orm_mode = True

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/')
def main():
    return {"hello":"world"}



@app.get('/all', response_model=List[URLResponse])
async def shortened_urls():
    query = urls.select()
    result =  await database.fetch_all(query)
    if not result:
        raise HTTPException(status_code = status.HTTP_200_OK, detail = "No entries yet")
    return result


@app.post('/shorten',response_model=URLResponse)
async def short_url(url: HttpUrl = Body(...,embed=True)):

    query = urls.select().where(urls.c.original_url == url)
    url_exist = await database.fetch_one(query)
    if url_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail=f"entry for the shortened key already exists: {url_exist.short_url}")
    
    id = await get_uuid()
    short_url = await shorten_url(url)

    query = urls.insert().values(
        id = id,
        original_url = url,
        short_url = short_url
    )
    try:
        await database.execute(query)
    except DBAPIError as e : 
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail="Something went wrong")
    finally:
        return URLResponse(id = id, original_url=url, 
                    short_url=short_url)



@app.get('/{short_url}')
async def redirect_link(short_url: str):
    query = urls.select().where(urls.c.short_url == short_url)
    result = await database.fetch_one(query) 
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = 'The link does not exist')
    return RedirectResponse(url=result.original_url)


async def shorten_url(url: str):
    encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(url.encode()).digest()).decode()
    return encoded_str[:7]

async def get_uuid():
    return uuid.uuid1().hex



