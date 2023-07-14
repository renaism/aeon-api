import urllib.parse

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import app.models

from app.config import DBConfig

async def init_db():
    host = DBConfig.HOST
    name = DBConfig.NAME
    username = urllib.parse.quote(DBConfig.USERNAME, safe="")
    password = urllib.parse.quote(DBConfig.PASSWORD, safe="")
    url = f"mongodb://{username}:{password}@{host}/?authSource={name}"

    db = AsyncIOMotorClient(url)
    document_models = [ "app.models." + model for model in app.models.__all__ ]

    await init_beanie(db[name], document_models=document_models)