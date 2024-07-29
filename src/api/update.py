from fastapi import APIRouter, status, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, insert, select
import os, sys

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import get_async_session
from api.schemas.update import *
from api.login import get_token
from api.responses import *
from models.products import *
from models.photo import *
from models.blog import *
from api.tasks.update import *

router = APIRouter(
    prefix="/update",
    tags=["Update"]
)


@router.get("/")
async def v1():
    return await status_error_404()


@router.put("/shop/item/{id}")
async def update_shop_item(id: int, 
                      request: update_shop_item,
                      new_photos: list[UploadFile] = None, 
                      session: AsyncSession = Depends(get_async_session)):
    
    if request.token != await get_token():
         return await status_error_401("invalid token")
    
    
    await session.execute(update(Table_products).values({Table_products.name: request.name, Table_products.short_description: request.short_description,
                                                         Table_products.full_description: request.full_description,
                           Table_products.price: request.price, Table_products.contacts: request.contacts}).where(Table_products.id == id))
    
    if request.last_photos:
        await session.execute(delete(Table_photos).where(Table_photos.product_id == id, Table_photos.photo_link.not_in(request.last_photos)))

        if new_photos:
            counter = 1

            for i in range(len(new_photos)):
                while True:
                    origin = f"https://storage.yandexcloud.net/trade-shop/{id}_{counter}_photo.jpg"

                    if origin in request.last_photos:
                        counter+=1


                    else:
                        await push_photo(new_photos[i], id, counter)
                        await session.execute(insert(Table_photos).values({Table_photos.product_id: id, Table_photos.photo_link: origin}))
                        counter+=1
                        break  
                      
    else:
        await session.execute(delete(Table_photos).where(Table_photos.product_id == id))
        
        if new_photos:
            for i in range(1, len(new_photos)+1):
                origin = f"https://storage.yandexcloud.net/trade-shop/{id}_{i}_photo.jpg"
                await session.execute(insert(Table_photos).values({Table_photos.product_id: id,
                                                                   Table_photos.photo_link: origin}))
                
                await push_photo(new_photos[i-1], id, i)
    

    
    await session.commit()
    return await status_ok()



@router.put("/blog/item/{id}")
async def update_blog_item(id: int, 
                           request: update_blog_item, 
                           new_photos: List[UploadFile] = None,
                           session: AsyncSession = Depends(get_async_session)):
    
    if request.token != await get_token():
        return await status_error_401("invalid token")
    
    
    await session.execute(update(Table_blog).values({Table_blog.name: request.name, Table_blog.description: request.description}))
    
    if request.last_photos:
        await session.execute(delete(Table_photos).where(Table_photos.blog_id == id, 
                                                         Table_photos.photo_link.not_in(request.last_photos)))
        if new_photos:
            counter = 1

            for i in range(len(new_photos)):
                while True:
                    origin = f"https://storage.yandexcloud.net/trade-shop/{id}_{counter}_photo_blog.jpg"

                    if origin in request.last_photos:
                        counter+=1


                    else:
                        await push_photo_blog(new_photos[i], id, counter)
                        await session.execute(insert(Table_photos).values({Table_photos.blog_id: id, Table_photos.photo_link: origin}))
                        counter+=1
                        break
                    
    else:
        await session.execute(delete(Table_photos).where(Table_photos.blog_id == id))
        
        if new_photos:
            for i in range(1, len(new_photos)+1):
                origin = f"https://storage.yandexcloud.net/trade-shop/{id}_{i}_photo_blog.jpg"
                
                await session.execute(insert(Table_photos).values({Table_photos.blog_id: id,
                                                                  Table_photos.photo_link: origin}))
                
                await push_photo_blog(new_photos[i-1], id, i)
        
    

                
    await session.commit()
    return await status_ok()
    
    
    
    
    
    
