from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from src.stats.models import EndpointStats
from src.stats.schemas import StatsResponse
from sqlalchemy import select

router = APIRouter()

@router.get("/stats", response_model=Optional[StatsResponse], name="Most Called Endpoint")
async def get_most_called_endpoint(
    db: AsyncSession = Depends(get_db)
) -> Optional[StatsResponse]:
    stmt = select(EndpointStats).order_by(EndpointStats.total_calls.desc()).limit(1)
    result = await db.execute(stmt)
    summary = result.scalar_one_or_none()

    if summary:
        return StatsResponse(
            endpoint=summary.endpoint_name,
            parameters=summary.params,
            total_calls=summary.total_calls,
            last_called=summary.last_called,
        )
    return None
