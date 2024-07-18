import os
import httpx

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from models.conversation import Conversation, create_conversation, get_conversation, get_conversations_by_user_id


router = APIRouter(prefix="/api")


@router.post("/conversation")
async def conversation():
    return create_conversation()


@router.get("/conversations")
async def conversations():
    return get_conversations_by_user_id()


@router.get("/logout")
async def logout():
    return RedirectResponse(url="/")


def setup_api_routes(app):
    app.include_router(router)
    return app