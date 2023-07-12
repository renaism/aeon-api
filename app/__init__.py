from fastapi import FastAPI

from app.database import init_db
from app.routes.v1.monitored_voice_channel import router as monitored_voice_channel_router


app = FastAPI(
    title="Aeon API",
    description="REST API for Aeon Bot",
)

app.include_router(monitored_voice_channel_router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def root() -> dict:
    return { "msg": "OK!" }