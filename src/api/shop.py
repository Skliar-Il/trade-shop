from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete 
from typing import List, Optional
from fastapi_cache.decorator import cache
from sqlalchemy.sql import func
from io import BytesIO
from pydantic import Json


import os, sys, asyncio, base64

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import get_async_session, s3
from models.products import Table_products
from models.photo import Table_photos
from api.schemas.shop import *
from api.responses import *
from api.login import get_token
from api.tasks.shop import push_photos


router = APIRouter(
    prefix="/shop",
    tags=["Shop"]
)

@router.get("/")
async def v1():
    return await status_error_404()


@router.get("/list/items")
@cache(expire=30)
async def items(session: AsyncSession = Depends(get_async_session)):
    data = await session.execute(select(Table_products.id, Table_products.name, Table_products.short_description,
                                        Table_products.date_published, Table_products.date_published,Table_products.price,
                                        Table_products.contacts, Table_photos.photo_link)
                                 .join(Table_photos, Table_photos.product_id == Table_products.id))
    #или писать через .filter(Table_products.id == Table_photos.product_id)
    
    return {"status": "ok", "detail": data.mappings().all()}


@router.get("/item/{id}")
@cache(expire=30)
async def get_item(id: int, session: AsyncSession = Depends(get_async_session)):
    data = await session.execute(select(Table_products.id, Table_products.name, Table_products.short_description, 
                                        Table_products.full_description,
                                        Table_products.date_published, Table_products.date_published,Table_products.price,
                                        Table_products.contacts, Table_photos.photo_link)
                                        .filter(Table_products.id == Table_photos.product_id)
                                 .where(Table_products.id == id)
                                 )
    data = data.mappings().all()
    
    if data == []:
        return await status_error_404()
    
    
    return {"status": "ok", "detail": data}



@router.post("/new_item")
async def new_item(
    request: post_new_item = Body(),
    photos: List[UploadFile] = None,   
    session: AsyncSession = Depends(get_async_session)):
    
    
    if request.token != await get_token():
       return await status_error_401("invalid token")
    

    await session.execute(insert(Table_products).values({Table_products.name: request.name, Table_products.short_description: request.short_description,
                                                   Table_products.full_description: request.full_description, Table_products.price: request.price,
                                                   Table_products.contacts: request.contacts
                                                  }))
    await session.flush()
    
    last_id = await session.execute(func.max(Table_products.id))
    last_id = last_id.scalar()
    
    for i in range(1, len(photos)+1):
        await session.execute(insert(Table_photos).values({Table_photos.product_id: last_id, Table_photos.photo_link:
            f"https://storage.yandexcloud.net/trade-shop/{last_id}_{i}_photo.jpg"}))
    
    await session.commit()
    
    await push_photos(photos, last_id)
    
    return await status_ok()



@router.delete("/delete_item/{id}")
async def delete_item(id: int, request: delete_item, session: AsyncSession = Depends(get_async_session)):
    if request.token != await get_token():
        return await status_error_401("invalid token")
    
    await session.execute(delete(Table_products).where(Table_products.id == id))
    await session.commit()
    
    return await status_ok()
    
    
    
    
    
         






