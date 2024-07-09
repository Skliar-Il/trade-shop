from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import os
import sys

from config import POSTGRES_HOST, POSTGRES_NAME, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT


class Base(DeclarativeBase):
    pass

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_factory() as session:
        yield session