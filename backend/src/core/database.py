from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.models import (
    User, Post, Follow, Like, Comment, Notification
)


async def connect_db(mongodb_url: str, db_name: str) -> None:
    client = AsyncIOMotorClient(mongodb_url)
    await init_beanie(
        database=client[db_name],
        document_models=[User, Post, Follow, Like, Comment, Notification],
    )


# Usage in main.py:
#
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from src.core.database import connect_db
# from src.core.config import settings
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await connect_db(settings.MONGODB_URL, settings.DATABASE_NAME)
#     yield
#
# app = FastAPI(lifespan=lifespan)