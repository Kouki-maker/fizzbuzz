from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import logging
from datetime import datetime
import hashlib
import json
from core.database import AsyncSessionLocal
from sqlalchemy import select

from src.stats.models import EndpointStats

logger = logging.getLogger(__name__)


class StatsMiddleware(BaseHTTPMiddleware):
    """Middleware to track endpoints statistics"""

    EXCLUDED_PATHS = {"/docs", "/redoc", "/openapi.json", "/health", "/stats"}

    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(excluded) for excluded in self.EXCLUDED_PATHS):
            return await call_next(request)

        method = request.method
        path = request.url.path
        params = dict(request.query_params)


        params_hash = hashlib.md5(
            json.dumps(params, sort_keys=True).encode()
        ).hexdigest()

        response = await call_next(request)


        try:
            await self._save_stats(
                endpoint_name=path,
                method=method,
                params=params,
                params_hash=params_hash,
            )
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")

        return response

    async def _save_stats(
        self,
        endpoint_name: str,
        method: str,
        params: dict,
        params_hash: str,
    ):
        """Store stats in database"""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(EndpointStats).where(
                    EndpointStats.endpoint_name == endpoint_name,
                    EndpointStats.params_hash == params_hash,
                )
                result = await session.execute(stmt)
                summary = result.scalar_one_or_none()

                if summary:
                    summary.total_calls += 1
                    summary.last_called = datetime.utcnow()

                else:
                    summary = EndpointStats(
                        endpoint_name=endpoint_name,
                        method=method,
                        params=params,
                        params_hash=params_hash,
                        total_calls=1,
                        last_called=datetime.utcnow(),
                    )
                    session.add(summary)

                await session.commit()

            except Exception as e:
                await session.rollback()
                logger.error(f"Error saving stats to database: {e}")
                raise
