from beanie import Document
from datetime import datetime
from pydantic import BaseModel, Field
from pymongo import ASCENDING, DESCENDING

from app.helper import utc_current_time


class Log(Document):
    category: str
    title: str
    detail: dict
    timestamp: datetime

    class Settings:
        name = "log"
        indexes = [
            [ ("category", ASCENDING) ],
            [ ("title", ASCENDING) ],
            [ ("timestamp", DESCENDING) ],
        ]


class CreateLog(BaseModel):
    category: str
    title: str
    detail: dict
    timestamp: datetime = Field(default_factory=utc_current_time)