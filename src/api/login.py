from sqlalchemy import select, update
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import sys, os, asyncio, time, hashlib, random, string

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import async_session_factory, get_async_session
from models.admins import Table_Admins
from api.responses import *

@cache(expire=30)
async def get_token():
    async with async_session_factory() as session: 
        token = await session.execute(select(Table_Admins.token))
        
        return token.scalar()
    
router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.get("/")
async def title():
    return await status_error_404()



@router.get("/admin/{login}/{password}")
async def login_admin(login: str, password: str, session: AsyncSession = Depends(get_async_session)):
    data_password = await session.execute(select(Table_Admins.password).where(Table_Admins.login == login))
    password = hashlib.sha3_512(password.encode()).hexdigest()
    
    if password == data_password.scalar():
        token = ''.join(random.choice(string.ascii_letters+
                                      string.ascii_lowercase+string.ascii_uppercase) for i in range(random.randint(32, 48)))
        
    
    else: 
        return await status_error_401("invalid password or login or you")
    
    await session.execute(update(Table_Admins).values({Table_Admins.token: token}).where(Table_Admins.login == login))
    await session.commit()
    
    return await status_ok(token)
    