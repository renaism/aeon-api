from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import app.models

from app.config import DBConfig

async def init_db():
    host = DBConfig.HOST
    name = DBConfig.NAME
    username = DBConfig.USERNAME
    password = DBConfig.PASSWORD

    db = AsyncIOMotorClient(f"mongodb://{username}:{password}@{host}/?authSource={name}")
    document_models = [ "app.models." + model for model in app.models.__all__ ]

    await init_beanie(db[name], document_models=document_models)