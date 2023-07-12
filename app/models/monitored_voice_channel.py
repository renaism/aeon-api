from beanie import Document, Indexed
from pydantic import BaseModel


class MonitoredVoiceChannel(Document):
    channel_id: Indexed(int, unique=True)
    guild_id: int
    default_name: str
    icon: str | None

    class Settings:
        name = "monitored_voice_channel"
    

class CreateMonitoredVoiceChannel(BaseModel):
    channel_id: int
    guild_id: int
    default_name: str
    icon: str | None = None


class UpdateMonitoredVoiceChannel(BaseModel):
    default_name: str
    icon: str | None = None