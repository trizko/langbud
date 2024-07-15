import os
import httpx

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

from dotenv import load_dotenv


load_dotenv()
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORED_OAUTH2_REDIRECT_URI = os.getenv("DISCORED_OAUTH2_REDIRECT_URI")


router = APIRouter(prefix="/api")


@router.get("/login-with-discord")
async def login():
    return RedirectResponse(url=f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORED_OAUTH2_REDIRECT_URI}&response_type=code&scope=identify+email")


@router.get("/discord/oauth2/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found in request")

    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORED_OAUTH2_REDIRECT_URI
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


@router.get("/logout")
async def logout():
    return RedirectResponse(url="/")


def setup_api_routes(app):
    app.include_router(router)
    return app