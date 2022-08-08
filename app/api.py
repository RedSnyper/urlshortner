from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import HttpUrl
from fastapi.responses import RedirectResponse
from .db import get_db
from .models import URLResponse, URLShortner
from .utils import get_url_code, get_uuid
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from typing import List, Tuple

router = APIRouter(
    tags = ['URL Shortner']
)
redirect = APIRouter()
root_url = 'http://localhost:8000/'

@router.post('/shorten',response_model=URLResponse)
async def short_url(db: AsyncSession = Depends(get_db),url: HttpUrl = Body(...,embed=True)):
    query = select(URLShortner).where(URLShortner.original_url == url)
    result:List[Tuple[URLShortner]]=list(await db.execute(query))
    if result:  #guaranted to be only 1 result as the database only stores unique results
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail=f"entry for the url already exists: {result[0][0].short_url}")
    id = await get_uuid()
    code = await get_url_code(url)
    short_url = f'{root_url}{code}'
    query = insert(URLShortner).values(
        id = id,
        original_url = url,
        code = code,
        short_url = short_url
    )
    try:
        await db.execute(query)
        await db.commit()
    except DBAPIError as e : 
        # logging.error(e)
        #rollback here
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail="Something went wrong")
    
    finally:
        return URLResponse(id = id, original_url=url, code=code,
                    short_url=short_url)

@router.get('/all', response_model=List[URLResponse])
async def shortened_urls(db: AsyncSession = Depends(get_db)):
    query = select(URLShortner)
    result =  await db.execute(query)
    return result.scalars().all()

#TODO: add some caching technique for most requested short url requests
@redirect.get('/{code}')
async def redirect_link(code: str, db: AsyncSession = Depends(get_db)):
    query = select(URLShortner).filter(URLShortner.code == code)
    result:List[Tuple[URLShortner]] = list(await db.execute(query))
    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = 'The link does not exist')
    return RedirectResponse(url=result[0][0].original_url)
