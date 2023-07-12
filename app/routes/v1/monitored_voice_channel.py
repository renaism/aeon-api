from fastapi import APIRouter, HTTPException
from pymongo.errors import DuplicateKeyError

from app.models.monitored_voice_channel import (
    CreateMonitoredVoiceChannel, 
    MonitoredVoiceChannel, 
    UpdateMonitoredVoiceChannel
)

router = APIRouter(
    prefix="/api/v1/monitored-voice-channels",
    tags=["activity_monitor"],
)


@router.get("/")
async def all() -> list[MonitoredVoiceChannel]:
    voice_channels = await MonitoredVoiceChannel.find().to_list()

    return voice_channels


@router.post("/", status_code=201)
async def create(req: CreateMonitoredVoiceChannel) -> MonitoredVoiceChannel:
    voice_channel = MonitoredVoiceChannel(**req.dict())
    
    try:
        await voice_channel.insert()
    except DuplicateKeyError:
        raise HTTPException(400, "Voice channel already exists")

    return voice_channel


@router.get("/{channel_id}")
async def detail(channel_id: int) -> MonitoredVoiceChannel:
    voice_channel = await MonitoredVoiceChannel.find_one(
        MonitoredVoiceChannel.channel_id == channel_id
    )

    if not voice_channel:
        raise HTTPException(404, "Voice channel not found")

    return voice_channel


@router.put("/{channel_id}")
async def edit(channel_id: int, req: UpdateMonitoredVoiceChannel) -> MonitoredVoiceChannel:
    voice_channel = await MonitoredVoiceChannel.find_one(
        MonitoredVoiceChannel.channel_id == channel_id
    )

    if not voice_channel:
        raise HTTPException(404, "Voice channel not found")

    await voice_channel.set(req.dict())

    return voice_channel


@router.delete("/{channel_id}", status_code=204)
async def delete(channel_id: int):
    voice_channel = await MonitoredVoiceChannel.find_one(
        MonitoredVoiceChannel.channel_id == channel_id
    )

    if not voice_channel:
        raise HTTPException(404, "Voice channel not found")
    
    await voice_channel.delete()