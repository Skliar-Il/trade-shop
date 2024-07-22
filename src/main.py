from fastapi import FastAPI, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from telebot import TeleBot
from fastapi.responses import JSONResponse
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as asyncredis
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware

from database import get_async_session
from api.shop import router as router_shop
from api.update import router as router_update
from api.login import router as router_login
from config import REDIS_PORT, REDIS_HOST



app = FastAPI(
    title="trade_shop",
    openapi_prefix="/v1",
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def title():
    
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "not found"})

@app.on_event("startup")
async def startup_event():
    redis_cache = asyncredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding = "utf8", decode_responses = True)
    FastAPICache.init(RedisBackend(redis_cache), prefix="fastapi-cache")




app.include_router(
    router=router_shop
)

app.include_router(
    router=router_update
)

app.include_router(
    router=router_login
)

