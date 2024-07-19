from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from boto3 import client, session
from boto3.s3.transfer import TransferConfig
from celery import Celery
import os, boto3, sys

from config import POSTGRES_HOST, POSTGRES_NAME, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_PORT, KEY_YANDEX_CLOUD, IDENT_YANDEX_CLOUD, REDIS_PORT, BUCKET


celery = Celery('tasks', broker=f"redis://127.0.0.1:{REDIS_PORT}")


session = boto3.session.Session(aws_access_key_id=IDENT_YANDEX_CLOUD, aws_secret_access_key=KEY_YANDEX_CLOUD, aws_session_token=None, region_name='ru-central1')
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)


class Base(DeclarativeBase):
    pass

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session