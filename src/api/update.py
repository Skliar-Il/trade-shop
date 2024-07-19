from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete, insert
import os, sys

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import get_async_session
from api.schemas.update import put_update_item
from api.login import get_token
from api.responses import status_error_401, status_ok
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
async def update_item(id: int, request: put_update_item, session: AsyncSession = Depends(get_async_session)):
    if request.token != await get_token():
        return await status_error_401("invalid token")
    
    await session.execute(update(Table_products.name, Table_products.short_description, Table_products.full_description,
                           Table_products.prise, Table_products.contacts).where(Table_products.id == id))
    
    
    await session.execute(delete(Table_photos).where(Table_photos.product_id == id and Table_photos.photo_link not in request.last_photos))
    
    for i in range(len(request.new_photos)):
        counter = 0
        
        while True:
            if f"https://storage.yandexcloud.net/trade-shop/{id}_{counter}_main.jpg" in request.last_photos:
                counter+=1
            
            else:
                await push_photo(request.new_photos[i], id, counter)
                break
    return await status_ok()
