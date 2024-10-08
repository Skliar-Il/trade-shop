from fastapi import Depends, APIRouter, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert, func
from typing import List
from fastapi_cache.decorator import cache

import sys, os 


sys.path.append(os.path.join(sys.path[0][:-4]))

from api.schemas.blog import *
from api.responses import *
from database import get_async_session, s3
from models.blog import *
from models.photo import * 
from api.tasks.blog import push_photos
from api.login import get_token


router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)


@router.get("/")
async def title():
    return await status_error_404()

@router.get("/list/items")
@cache(expire=30)
async def get_items(session: AsyncSession = Depends(get_async_session)):
    data = await session.execute(select(Table_blog.id, Table_blog.date_published, Table_blog.description, Table_blog.name,
                                        Table_photos.photo_link).join(Table_photos, Table_blog.id == Table_photos.blog_id, isouter=True))
    
    return {"status": "ok", "detail": data.mappings().all()}


@router.get("/item/{id}")
@cache(expire=30)
async def get_item(id: int, 
                   session: AsyncSession = Depends(get_async_session)):
    
    data = await session.execute(select(Table_blog.id, Table_blog.date_published, Table_blog.description, Table_blog.name,
                                        Table_photos.photo_link)
                                 .join(Table_photos, Table_blog.id == Table_photos.blog_id, isouter=True)
                                 .where(Table_blog.id == id))  
        
    data = data.mappings().all()
    
    if data == []:
        return await status_error_404()
    
    return {"status": "ok", "detail": data}

@router.post("/new_item")
async def new_item(request: post_new_item, 
                   photos: List[UploadFile] = None, 
                   session: AsyncSession = Depends(get_async_session)):
    
    if request.token != await get_token():
       return await status_error_401("invalid token")    
    
    await session.execute(insert(Table_blog).values({Table_blog.name: request.name, Table_blog.description: request.description}))

    if photos:
        await session.flush()
    
        last_id = await session.execute(func.max(Table_blog.id))
        last_id = last_id.scalar()
        
        for i in range(1, len(photos)+1):
            await session.execute(insert(Table_photos).values({Table_photos.blog_id: last_id, Table_photos.photo_link:
                f"https://storage.yandexcloud.net/trade-shop/{last_id}_{i}_photo_blog.jpg"}))
        await push_photos(photos, last_id)
    
    await session.commit()
    return await status_ok()
    
    
    
@router.delete("/delete_item")
async def delete_item(id: int, request: delete_item, session: AsyncSession = Depends(get_async_session)):
    if request.token != await get_token():
        return await status_error_401("invalid token")
    
    await session.execute(delete(Table_blog).where(Table_blog.id == id))
    
    await session.commit()
    
    return await status_ok()