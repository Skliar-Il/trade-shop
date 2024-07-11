from fastapi import FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from telebot import TeleBot
from fastapi.responses import JSONResponse

from database import get_async_session
from api.shop import router as router_shop



app = FastAPI(
    title="trade_shop",
    openapi_prefix="/v1",
)

@app.get("/")
async def title():
    
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "not found"})



app.include_router(
    router=router_shop,
    prefix="/shop",
    tags=["Shop"]
)