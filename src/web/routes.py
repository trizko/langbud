import os
import httpx

from pydantic import BaseModel

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv


load_dotenv()
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")


class UserMessage(BaseModel):
    prompt: str


class Response(BaseModel):
    message: str


router = APIRouter()


@router.post('/chat/')
async def generate_text(message: UserMessage):
    return Response(message="200 OK")


@router.get('/')
async def index():
    return FileResponse("src/web/frontend/index.html")


@router.get('/login/')
async def login():
    return FileResponse("src/web/frontend/login.html")


@router.get("/login-with-discord")
async def login():
    return RedirectResponse(url=f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify+email")


@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found in request")

    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
        response_data = response.json()
        access_token = response_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        user_response = await client.get("https://discord.com/api/users/@me", headers={"Authorization": f"Bearer {access_token}"})
        user_data = user_response.json()

    return user_data


def setup_routes(app):
    app.mount("/static", StaticFiles(directory="src/web/frontend"), name="static")
    app.include_router(router)
    return app