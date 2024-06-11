import asyncpg

from pydantic import BaseModel
from typing import List

from .constants import LANGUAGE_MAPPING
from .user import User


class Conversation(BaseModel):
    conversation_id: int
    user_id: int
    conversation_language: str


async def create_conversation(db_conn: asyncpg.Connection, user: User, conversation_language: str) -> Conversation:
    async with db_conn.transaction():
        conversation = await db_conn.fetchrow(
            "INSERT INTO conversations (user_id, conversation_language) VALUES ($1, $2) RETURNING *",
            user.user_id,
            conversation_language,
        )
        await db_conn.execute(
            "UPDATE users SET active_conversation_id = $1 WHERE id = $2",
            conversation.get("id"),
            user.user_id,
        )

    return Conversation(
        conversation_id=conversation.get("id"),
        user_id=conversation.get("user_id"),
        conversation_language=conversation.get("conversation_language"),
    )

async def get_conversation(db_conn: asyncpg.Connection, conversation_id: int) -> Conversation:
    pass

async def get_conversations_by_user_id(db_conn: asyncpg.Connection, user_id: int) -> List[Conversation]:
    pass