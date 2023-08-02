from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes.v1.log import router as log_router
from app.routes.v1.monitored_voice_channel import router as monitored_voice_channel_router
from app.routes.v1.preferred_activity_name import router as preferred_activity_name_router


app = FastAPI(
    title="Aeon API",
    description="REST API for Aeon Bot",
)

# CORS
origins = [
    "http://localhost:[0-9]*",
    "https://.*aeon.*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="|".join(origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(log_router)
app.include_router(monitored_voice_channel_router)
app.include_router(preferred_activity_name_router)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
async def root() -> dict:
    return { "msg": "OK!" }