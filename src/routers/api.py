from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from dependencies import get_db_pool, get_user_session
from models.user import get_user_by_discord_username, update_user
from models.conversation import get_conversations_by_user_id
from models.message import get_messages_by_conversation_id


router = APIRouter(prefix="/api")


@router.get("/user")
async def get_user(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        return user


@router.put("/user")
async def update_active_conversation(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        data = await request.json()
        user = await update_user(connection, user.user_id, data["active_conversation_id"])
        return user


@router.get("/conversations")
async def get_conversations(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        conversations = await get_conversations_by_user_id(connection, user.user_id)
        return conversations


@router.get("/messages")
async def get_messages(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        messages = await get_messages_by_conversation_id(connection, user.active_conversation_id)
        return messages


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    request.session.pop("access_token", None)
    return RedirectResponse(url="/")
