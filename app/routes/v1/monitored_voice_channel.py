from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError
from typing import Annotated

from app.dependencies import get_api_key
from app.models.monitored_voice_channel import (
    CreateMonitoredVoiceChannel, 
    MonitoredVoiceChannel, 
    UpdateMonitoredVoiceChannel
)

router = APIRouter(
    prefix="/api/v1/monitored-voice-channels",
    tags=["activity_monitor"],
    dependencies=[Depends(get_api_key)],
)


async def get_voice_channel(channel_id: int) -> MonitoredVoiceChannel:
    voice_channel = await MonitoredVoiceChannel.find_one(
        MonitoredVoiceChannel.channel_id == channel_id
    )

    if not voice_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice channel not found",
        )
    
    return voice_channel


VoiceChannelDep = Annotated[MonitoredVoiceChannel, Depends(get_voice_channel)]


@router.get("/")
async def all() -> list[MonitoredVoiceChannel]:
    voice_channels = await MonitoredVoiceChannel.find().to_list()

    return voice_channels


@router.post("/", status_code=201)
async def create(
    req: CreateMonitoredVoiceChannel,
) -> MonitoredVoiceChannel:
    voice_channel = MonitoredVoiceChannel(**req.dict())
    
    try:
        await voice_channel.insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Voice channel already exists",
        )

    return voice_channel


@router.get("/{channel_id}")
async def detail(
    voice_channel: VoiceChannelDep,
) -> MonitoredVoiceChannel:
    return voice_channel


@router.put("/{channel_id}")
async def edit(
    voice_channel: VoiceChannelDep,
    req: UpdateMonitoredVoiceChannel,
) -> MonitoredVoiceChannel:
    await voice_channel.set(req.dict())

    return voice_channel


@router.delete("/{channel_id}", status_code=204)
async def delete(
    voice_channel: VoiceChannelDep,
):    
    await voice_channel.delete()