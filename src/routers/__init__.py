from fastapi import APIRouter

from .api import router as api_router
from .discord import router as discord_router
from .static import router as static_router


router = APIRouter()
router.include_router(api_router)
router.include_router(discord_router)
router.include_router(static_router)
