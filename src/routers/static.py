import os

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv


load_dotenv()
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORED_OAUTH2_REDIRECT_URI = os.getenv("DISCORED_OAUTH2_REDIRECT_URI")


router = APIRouter()
router.mount("/static", StaticFiles(directory="src/frontend"), name="static")


@router.get('/')
async def index():
    return FileResponse("src/web/frontend/index.html")


@router.get('/chat/')
async def chat():
    return FileResponse("src/web/frontend/app.html")
