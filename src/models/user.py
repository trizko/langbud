import asyncpg
from pydantic import BaseModel
from typing import List, Optional


LANGUAGE_MAPPING = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
}


class User(BaseModel):
    user_id: int
    username: str
    spoken_language: str
    learning_language: str
    messages: Optional[List[dict]] = []


async def create_user(
    db_conn: asyncpg.Connection,
    username: str,
    spoken_language: str,
    learning_language: str,
):
    new_user = await db_conn.fetchrow(
        "INSERT INTO users (username, spoken_language, learning_language) VALUES ($1, $2, $3) RETURNING *",
        username,
        spoken_language,
        learning_language,
    )
    return User(
        user_id=new_user.get("id"),
        username=new_user.get("username"),
        spoken_language=new_user.get("spoken_language"),
        learning_language=new_user.get("learning_language"),
    )


async def get_user_by_username(db_conn: asyncpg.Connection, username: str):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        username=user.get("username"),
        spoken_language=user.get("spoken_language"),
        learning_language=user.get("learning_language"),
    )


async def get_user(db_conn: asyncpg.Connection, user_id: int):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        username=user.get("username"),
        spoken_language=user.get("spoken_language"),
        learning_language=user.get("learning_language"),
    )


async def update_user(
    db_conn: asyncpg.Connection,
    user_id: int,
    spoken_language: str,
    learning_language: str,
):
    user = await db_conn.fetchrow(
        "UPDATE users SET spoken_language = $1, learning_language = $2 WHERE id = $3 RETURNING *",
        spoken_language,
        learning_language,
        user_id,
    )
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        username=user.get("username"),
        spoken_language=user.get("spoken_language"),
        learning_language=user.get("learning_language"),
    )


async def delete_user(db_conn: asyncpg.Connection, user_id: int):
    try:
        await db_conn.execute("DELETE FROM users WHERE id = $1", user_id)
    except Exception:
        return False

    return True


async def get_messages_by_user(db_conn: asyncpg.Connection, user: User):
    messages = await db_conn.fetch(
        "SELECT is_from_user, message_text FROM messages WHERE user_id = $1",
        user.user_id,
    )
    if not messages:
        return []

    system_message = {
        "role": "system",
        "content": f"You are a friendly {LANGUAGE_MAPPING[user.learning_language]}-speaking chatbot. Your task is to help the user learn {LANGUAGE_MAPPING[user.learning_language]}. You should continue the conversation in {LANGUAGE_MAPPING[user.learning_language]}, but if the user makes a mistake, correct them in {LANGUAGE_MAPPING[user.spoken_language]}.",
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


async def create_message(
    db_conn: asyncpg.Connection,
    user_id: int,
    is_from_user: bool,
    message_text: str,
):
    message = await db_conn.execute(
        "INSERT INTO messages (user_id, is_from_user, message_text) VALUES ($1, $2, $3) RETURNING *",
        user_id,
        is_from_user,
        message_text,
    )

    return message


async def get_last_message(db_conn: asyncpg.Connection, user: User):
    message = await db_conn.fetchrow(
        "SELECT * FROM messages WHERE user_id = $1 AND is_from_user = false ORDER BY id DESC LIMIT 1",
        user.user_id,
    )
    if not message:
        return None

    return message.get("message_text")
