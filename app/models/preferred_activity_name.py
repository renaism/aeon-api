from beanie import Document
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel


class PreferredActivityName(Document):
    guild_id: int
    original_name: str
    preferred_name: str

    class Settings:
        name = "preferred_activity_name"
        indexes = [
            IndexModel(
                [ ("guild_id", ASCENDING), ("original_name", ASCENDING) ],
                unique=True,
            ),
        ]
    

class CreatePreferredActivityName(BaseModel):
    guild_id: int
    original_name: str
    preferred_name: str


class UpdatePreferredActivityName(BaseModel):
    preferred_name: str