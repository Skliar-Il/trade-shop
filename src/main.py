from fastapi import FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from telebot import TeleBot
from fastapi.responses import JSONResponse

from database import get_async_session
from models.users import Table_Users
from api.shop import router as router_shop

from config import TG_BOT_TOKEN



app = FastAPI(
    title="trade_shop"
)

@app.get("/")
async def title():
    
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="error 404 not found")



app.include_router(
    router=router_shop,
    prefix="/shop",
    tags="Shop"
)