import os
import httpx

from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(prefix="/api")


@router.get("/logout")
async def logout():
    return RedirectResponse(url="/")


def setup_api_routes(app):
    app.include_router(router)
    return app