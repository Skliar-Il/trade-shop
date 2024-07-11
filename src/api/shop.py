from fastapi import APIRouter, Depends, status, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from typing import List

import os, sys 

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import get_async_session
from models.products import Table_products
from api.schemas.shop import post_new_item
from api.responses import status_ok

router = APIRouter(
    prefix="/shop",
    tags=["Shop"]
)

@router.get("/")
async def v1():
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "not found"})


@router.get("/list/items")
async def items(session: AsyncSession = Depends(get_async_session)):
    data = await session.execute(select(Table_products.id, Table_products.name, Table_products.description,
                           Table_products.photo, Table_products.date_published, Table_products.date_published,
                           Table_products.prise, Table_products.contacts))

    return {"status": "ok", "detail": data.mappings().all()}


@router.post("/new_item")
async def new_item(request: post_new_item, photo: UploadFile, session: AsyncSession = Depends(get_async_session)):
    #идентификация по токену + redis 
    
    
    #подключиться к яндекс облаку для photo
    session.execute(insert(Table_products).values({Table_products.name: request.name, Table_products.description: request.description,
                                                   }))
    
    
    return request.description