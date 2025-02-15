from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError
from typing import Annotated

from app.dependencies import get_api_key
from app.models.monitored_voice_channel import (
    CreateMonitoredVoiceChannel, 
    MonitoredVoiceChannel
)

router = APIRouter(
    prefix="/api/v1/monitored-voice-channel",
    tags=["activity_monitor"],
    dependencies=[Depends(get_api_key)],
)


async def get_voice_channel(
    guild_id: int,
    channel_id: int,
) -> MonitoredVoiceChannel:
    voice_channel = await MonitoredVoiceChannel.find_one(
        MonitoredVoiceChannel.guild_id == guild_id,
        MonitoredVoiceChannel.channel_id == channel_id,
    )

    if not voice_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voice channel not found",
        )
    
    return voice_channel


VoiceChannelDep = Annotated[MonitoredVoiceChannel, Depends(get_voice_channel)]


@router.get("/list")
async def list_(
    guild_id: int | None = None
) -> list[MonitoredVoiceChannel]:
    if guild_id is None:
        # Find all voice channels for all guilds
        query = MonitoredVoiceChannel.find()
    else:
        # Find all voice channels for a specific guild
        query = MonitoredVoiceChannel.find(
            MonitoredVoiceChannel.guild_id == guild_id
        )
    
    voice_channels = await query.to_list()

    return voice_channels


@router.post("/create", status_code=201)
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


@router.get("/detail")
async def detail(
    voice_channel: VoiceChannelDep,
) -> MonitoredVoiceChannel:
    return voice_channel


@router.delete("/delete", status_code=204)
async def delete(
    voice_channel: VoiceChannelDep,
):    
    await voice_channel.delete()