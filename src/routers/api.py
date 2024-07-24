from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from dependencies import get_db_pool
from models.user import get_user_by_discord_username
from models.conversation import create_conversation, get_conversations_by_user_id


router = APIRouter(prefix="/api")


@router.post("/conversation")
async def conversation():
    return create_conversation()


@router.get("/conversations")
async def conversations(request: Request, pool = Depends(get_db_pool)):
    user_session = request.session.get("user")
    if not user_session:
        return RedirectResponse(url="/")

    async with pool.acquire() as connection:
        user = await get_user_by_discord_username(connection, user_session["username"])
        conversations = await get_conversations_by_user_id(connection, user.user_id)
        return conversations


@router.get("/logout")
async def logout():
    return RedirectResponse(url="/")
