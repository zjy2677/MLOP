from fastapi import FastAPI
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.items import router as items_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(items_router, prefix="/api/v1", tags=["items"])
