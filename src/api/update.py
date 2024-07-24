from fastapi import APIRouter, status, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, insert, select
import os, sys

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import get_async_session
from api.schemas.update import put_update_item
from api.login import get_token
from api.responses import *
from models.products import *
from models.photo import *
from api.tasks.update import *

router = APIRouter(
    prefix="/update",
    tags=["Update"]
)


@router.get("/")
async def v1():
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "not found"})


@router.put("/shop/item/{id}")
async def update_item(id: int, 
                      request: put_update_item,
                      new_photos: list[UploadFile] = None, 
                      session: AsyncSession = Depends(get_async_session)):
    
    if request.token != await get_token():
         return await status_error_401("invalid token")
    
    
    await session.execute(update(Table_products).values({Table_products.name: request.name, Table_products.short_description: request.short_description,
                                                         Table_products.full_description: request.full_description,
                           Table_products.prise: request.price, Table_products.contacts: request.contacts}).where(Table_products.id == id))
    
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
    
    await session.commit()
    return await status_ok("ok")
