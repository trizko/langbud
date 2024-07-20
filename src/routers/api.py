from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from dependencies import get_db_pool
from models.conversation import create_conversation, get_conversations_by_user_id


router = APIRouter(prefix="/api")


@router.post("/conversation")
async def conversation():
    return create_conversation()


@router.get("/conversations")
async def conversations(pool = Depends(get_db_pool)):
    async with pool.acquire() as connection:
        conversations = await get_conversations_by_user_id(connection, 1)
        return conversations


@router.get("/logout")
async def logout():
    return RedirectResponse(url="/")