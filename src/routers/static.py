import os

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


router = APIRouter()
router.mount("/static", StaticFiles(directory="src/frontend"), name="static")


@router.get('/')
async def index():
    return FileResponse("src/frontend/index.html")


@router.get('/chat/')
async def chat():
    return FileResponse("src/frontend/app.html")
