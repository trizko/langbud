import asyncpg

from pydantic import BaseModel

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
        "SELECT * FROM messages WHERE user_id = $1 AND is_from_user = false AND message_language = $2 ORDER BY id DESC LIMIT 1",
        user.user_id,
        user.learning_language,
    )
    if not message:
        return None

    return Message(
        message_id=message.get("id"),
        user_id=message.get("user_id"),
        is_from_user=message.get("is_from_user"),
        message_text=message.get("message_text"),
        message_language=message.get("message_language"),
    )
