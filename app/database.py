from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import app.models

async def init_db():
    db = AsyncIOMotorClient("mongodb://127.0.0.1:27017")
    document_models = [ "app.models." + model for model in app.models.__all__ ]

    await init_beanie(db.aeon_dev, document_models=document_models)