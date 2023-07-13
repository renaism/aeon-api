from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError
from typing import Annotated

from app.dependencies import get_api_key
from app.models.preferred_activity_name import (
    CreatePreferredActivityName, 
    PreferredActivityName, 
    UpdatePreferredActivityName
)

router = APIRouter(
    prefix="/api/v1/preferred-activity-name",
    tags=["activity_monitor"],
    dependencies=[Depends(get_api_key)],
)


async def get_activity(
    guild_id: int,
    original_name: str
) -> PreferredActivityName:
    activity = await PreferredActivityName.find_one(
        PreferredActivityName.guild_id == guild_id,
        PreferredActivityName.original_name == original_name,
    )

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )
    
    return activity


ActivityDep = Annotated[PreferredActivityName, Depends(get_activity)]


@router.get("/list")
async def list_(
    guild_id: int,
) -> list[PreferredActivityName]:
    activities = await PreferredActivityName.find(
        PreferredActivityName.guild_id == guild_id
    ).to_list()

    return activities


@router.post("/create", status_code=201)
async def create(
    req: CreatePreferredActivityName,
) -> PreferredActivityName:
    activity = PreferredActivityName(**req.dict())
    
    try:
        await activity.insert()
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity name already exists for the server",
        )

    return activity


@router.get("/detail")
async def detail(
    activity: ActivityDep,
) -> PreferredActivityName:
    return activity


@router.put("/edit")
async def edit(
    activity: ActivityDep,
    req: UpdatePreferredActivityName,
) -> PreferredActivityName:
    await activity.set(req.dict())

    return activity


@router.delete("/delete", status_code=204)
async def delete(
    activity: ActivityDep,
):    
    await activity.delete()