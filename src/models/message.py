import asyncpg

from pydantic import BaseModel
from typing import List

from .user import User


class Message(BaseModel):
    message_id: int
    user_id: int
    conversation_id: int
    is_from_user: bool
    message_text: str

    def from_query(query_result):
        return Message(
            message_id=query_result.get("id"),
            user_id=query_result.get("user_id"),
            conversation_id=query_result.get("conversation_id"),
            is_from_user=query_result.get("is_from_user"),
            message_text=query_result.get("message_text"),
        )


async def create_message(
    db_conn: asyncpg.Connection,
    user: User,
    is_from_user: bool,
    message_text: str,
) -> Message:
    message = await db_conn.fetchrow(
        "INSERT INTO messages (user_id, conversation_id, is_from_user, message_text) VALUES ($1, $2, $3, $4) RETURNING *",
        user.user_id,
        user.active_conversation_id,
        is_from_user,
        message_text,
    )

    return Message.from_query(message)


async def get_last_message_by_user(db_conn: asyncpg.Connection, user: User) -> Message:
    message = await db_conn.fetchrow(
        "SELECT * FROM messages WHERE user_id = $1 AND is_from_user = false AND conversation_id = $2 ORDER BY id DESC LIMIT 1",
        user.user_id,
        user.active_conversation_id,
    )
    if not message:
        return None

    return Message.from_query(message)


async def get_messages_by_conversation_id(
    db_conn: asyncpg.Connection, conversation_id: int, limit: int = 25
) -> List[Message]:
    messages = await db_conn.fetch(
        """
        WITH last_messages AS (
            SELECT
                *
            FROM messages
            WHERE conversation_id = $1
            ORDER BY created_at DESC
            LIMIT $2
        ) SELECT * FROM last_messages ORDER BY id ASC
        """,
        conversation_id,
        limit,
    )
    return [Message.from_query(message) for message in messages]


async def get_message(db_conn: asyncpg.Connection, message_id: int) -> Message:
    message = await db_conn.fetchrow("SELECT * FROM messages WHERE id = $1", message_id)
    if not message:
        return None

    return Message.from_query(message)


async def delete_message(db_conn: asyncpg.Connection, message_id: int):
    try:
        await db_conn.execute("DELETE FROM messages WHERE id = $1", message_id)
    except Exception:
        return False

    return True


async def get_last_message_by_conversation_id(
    db_conn: asyncpg.Connection, conversation_id: int
) -> Message:
    message = await db_conn.fetchrow(
        "SELECT * FROM messages WHERE conversation_id = $1 ORDER BY id DESC LIMIT 1",
        conversation_id,
    )
    if not message:
        return None

    return Message.from_query(message)