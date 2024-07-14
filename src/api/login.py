from sqlalchemy import select
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
import sys, os, asyncio, time

sys.path.append(os.path.join(sys.path[0][:-3]))

from database import async_session_factory
from models.admins import Table_Admins

@cache(expire=30)
async def get_token():
    async with async_session_factory() as session: 
        token = await session.execute(select(Table_Admins.token))
        
        return token.scalar()
    
