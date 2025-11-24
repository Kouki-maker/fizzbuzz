import logging
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from src.stats.router import router as stats_router
from src.fizzbuzz.router import router as fizzbuzz_router


from core.config import settings

from core.database import init_db


from fastapi import FastAPI

from src.stats.middleware import StatsMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting application...")

    await init_db()

    logger.info("Application started successfully")

    yield

    logger.info("Shutting down application...")
    logger.info("Application stopped")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-ready API with statistics tracking and caching",
    lifespan=lifespan
)
app.include_router(stats_router)
app.include_router(fizzbuzz_router)

app.add_middleware(StatsMiddleware)

logger = logging.getLogger(__name__)


@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health():
    return {"Health": "OK"}
