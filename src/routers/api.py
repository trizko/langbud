from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from dependencies import get_db_pool, get_user_session
from models.user import get_user_by_discord_username, update_user
from models.conversation import get_conversation, get_conversations_by_user_id, create_conversation
from models.message import create_message, get_messages_by_conversation_id
from models.utils import format_messages_openai


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
        return { "conversations": conversations, "active_conversation_id": user.active_conversation_id }


@router.post("/conversations")
async def create_conversation(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        data = await request.json()
        conversation = await create_conversation(connection, user.user_id, data["conversation_language"])
        user = await update_user(connection, user.user_id, conversation.conversation_id)
        return conversation


@router.get("/messages")
async def get_messages(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        messages = await get_messages_by_conversation_id(connection, user.active_conversation_id)
        return messages


@router.post("/messages")
async def post_message(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        data = await request.json()
        message = await create_message(connection, user, True, data["message_text"])
        return message


@router.get("/messages/generate")
async def generate_message(request: Request, pool = Depends(get_db_pool), user_session = Depends(get_user_session)):
    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        conversation = await get_conversation(connection, user.active_conversation_id)
        raw_messages = await get_messages_by_conversation_id(connection, user.active_conversation_id)
        messages = await format_messages_openai(user, raw_messages, conversation.conversation_language)
        content = request.app.state.llm.complete(model="gpt-4o", messages=messages)
        message = await create_message(connection, user, is_from_user=False, message_text=content)
        return message


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    request.session.pop("access_token", None)
    return RedirectResponse(url="/")
