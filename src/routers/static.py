import os
import httpx

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv


load_dotenv()
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORED_OAUTH2_REDIRECT_URI = os.getenv("DISCORED_OAUTH2_REDIRECT_URI")


router = APIRouter()


@router.get('/')
async def index():
    return FileResponse("src/web/frontend/index.html")


@router.get('/chat/')
async def chat():
    return FileResponse("src/web/frontend/app.html")


def setup_web_routes(app):
    app.mount("/static", StaticFiles(directory="src/web/frontend"), name="static")
    app.include_router(router)
    return app