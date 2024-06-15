import asyncpg

from pydantic import BaseModel
from typing import List, Optional

from .constants import LANGUAGE_MAPPING


class User(BaseModel):
    user_id: int
    discord_username: str
    spoken_language: str
    active_conversation_id: Optional[int]

    def from_query(query_result):
        return User(
            user_id=query_result.get("id"),
            discord_username=query_result.get("discord_username"),
            spoken_language=query_result.get("spoken_language"),
            active_conversation_id=query_result.get("active_conversation_id"),
        )


async def create_user(
    db_conn: asyncpg.Connection,
    discord_username: str,
    spoken_language: str,
) -> User:
    new_user = await db_conn.fetchrow(
        "INSERT INTO users (discord_username, spoken_language) VALUES ($1, $2) RETURNING *",
        discord_username,
        spoken_language,
    )

    return User.from_query(new_user)


async def get_user_by_discord_username(db_conn: asyncpg.Connection, discord_username: str) -> User:
    user = await db_conn.fetchrow("SELECT * FROM users WHERE discord_username = $1", discord_username)
    if not user:
        return None

    return User.from_query(user)


async def get_user(db_conn: asyncpg.Connection, user_id: int) -> User:
    user = await db_conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not user:
        return None

    return User.from_query(user)


async def update_user(
    db_conn: asyncpg.Connection,
    user_id: int,
    active_conversation_id: int,
) -> User:
    user = await db_conn.fetchrow(
        "UPDATE users SET active_conversation_id = $1 WHERE id = $2 RETURNING *",
        active_conversation_id,
        user_id,
    )
    if not user:
        return None

    return User.from_query(user)


async def update_user_language(db_conn: asyncpg.Connection, user: User, spoken_language: str) -> User:
    user = await db_conn.fetchrow(
        "UPDATE users SET spoken_language = $1 WHERE id = $2 RETURNING *",
        spoken_language,
        user.user_id,
    )
    if not user:
        return None

    return User.from_query(user)


async def delete_user(db_conn: asyncpg.Connection, user_id: int):
    try:
        await db_conn.execute("DELETE FROM users WHERE id = $1", user_id)
    except Exception:
        return False

    return True


async def get_messages_by_user(db_conn: asyncpg.Connection, user: User) -> List[dict]:
    messages = await db_conn.fetch(
        "SELECT is_from_user, message_text FROM messages WHERE user_id = $1 AND message_language = $2 ORDER BY id ASC LIMIT 50",
        user.user_id,
        user.learning_language,
    )
    if not messages:
        return []

    system_message = {
        "role": "system",
        "content": f"You are a friendly {LANGUAGE_MAPPING[user.learning_language]}-speaking chatbot named Maya. Your task is to help the user learn {LANGUAGE_MAPPING[user.learning_language]}. You should continue the conversation in {LANGUAGE_MAPPING[user.learning_language]}, but if the user makes a mistake, correct them in {LANGUAGE_MAPPING[user.spoken_language]}.",
    }
    formatted_messages = [
        {
            "role": "user" if message.get("is_from_user") else "assistant",
            "content": message.get("message_text"),
        }
        for message in messages
    ]
    formatted_messages.insert(0, system_message)
    return formatted_messages
