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


async def get_user_with_messages(db_conn: asyncpg.Connection, user: User):
    messages = await db_conn.fetch(
        "SELECT is_from_user, message_text FROM messages WHERE user_id = $1",
        user.user_id,
    )
    if not messages:
        return user

    system_message = {
        "role": "system",
        "content": f"You are a friendly {LANGUAGE_MAPPING[user.learning_language]}-speaking chatbot. Your task is to help the user learn {LANGUAGE_MAPPING[user.learning_language]}. You should continue the conversation in {LANGUAGE_MAPPING[user.learning_language]}, but if the user makes a mistake, correct them in {LANGUAGE_MAPPING[user.spoken_language]}.",
    }
    user.messages = [
        {
            "role": "user" if message.get("is_from_user") else "assistant",
            "content": message.get("message_text"),
        }
        for message in messages
    ]
    user.messages.insert(0, system_message)
    return user
