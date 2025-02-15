from beanie import Document
from pydantic import BaseModel
from pymongo import ASCENDING, IndexModel


class MonitoredVoiceChannel(Document):
    guild_id: int
    channel_id: int

    class Settings:
        name = "monitored_voice_channel"
        indexes = [
            IndexModel(
                [ ("guild_id", ASCENDING), ("channel_id", ASCENDING) ],
                unique=True,
            ),
        ]
    

class CreateMonitoredVoiceChannel(BaseModel):
    channel_id: int
    guild_id: int