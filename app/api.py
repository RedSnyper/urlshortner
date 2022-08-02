from pydantic import HttpUrl
from fastapi.responses import RedirectResponse
from .db import get_db, URLShortner, URLResponse
from .shorten_url import shorten_url
from sqlalchemy.orm import Session
from typing import List
from fastapi import (APIRouter, 
                    Body, 
                    Depends, 
                    HTTPException, 
                    status)


router = APIRouter(
    tags = ['URL Shortner']
)
redirect = APIRouter()

@router.post('/shorten',response_model=URLResponse)
async def short_url(db: Session = Depends(get_db),url: HttpUrl = Body(...,embed=True)):
    url_exists: URLShortner = db.query(URLShortner).filter(URLShortner.url == url).first()
    if url_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
        detail=f"entry for the shortened key already exists: {url_exists.short_url}")
    short_url = await shorten_url(url)
    obj = URLShortner(url= url, short_url = short_url)
    db.add(obj)
    db.commit()
    return obj


@router.get('/all', response_model=List[URLResponse])
def shortened_urls(db: Session = Depends(get_db)):
    urls: URLShortner = db.query(URLShortner).all()
    if not urls:
        raise HTTPException(status_code = status.HTTP_200_OK, detail = "No entries yet")
    return urls

@redirect.get('/{short_url}')
def redirect_link(short_url: str, db: Session = Depends(get_db)):
    obj: URLShortner = db.query(URLShortner).filter(URLShortner.short_url == short_url).first()
    if not obj:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail = 'The link does not exist')
    return RedirectResponse(url=obj.url)

