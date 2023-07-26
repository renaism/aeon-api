from fastapi import APIRouter, Depends

from app.dependencies import get_api_key, PaginationDep
from app.models.log import (
    CreateLog,
    Log
)


router = APIRouter(
    prefix="/api/v1/log",
    tags=["log"],
    dependencies=[Depends(get_api_key)],
)


@router.get("/list")
async def list_(
    pagination: PaginationDep,
    category: str | None = None,
    title: str | None = None,
) -> list[Log]:
    query = Log.find()

    # Filter by category
    if category:
        query = query.find(
            {
                "category": { "$regex": category, "$options": "i" }
            }
        )
    
    # Filter by title
    if title:
        query = query.find(
            {
                "title": { "$regex": title, "$options": "i" }
            }
        )
    
    # Pagination
    query = query.skip(pagination.skip).limit(pagination.limit)

    # Sort by timestamp descending (newest first)
    query = query.sort(-Log.timestamp)
    
    # Get data as list
    logs = await query.to_list()

    return logs


@router.post("/create", status_code=201)
async def create(
    req: CreateLog,
) -> Log:
    log = Log(**req.dict())
    await log.insert()

    return log