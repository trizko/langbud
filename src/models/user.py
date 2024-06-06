import asyncpg
from pydantic import BaseModel
from typing import List, Optional


LANGUAGE_MAPPING = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "tr": "Turkish",
    "pt-BR": "Brazilian Portuguese",
}


class User(BaseModel):
    user_id: int
    discord_username: str
    spoken_language: str
    learning_language: str
    active_conversation_id: Optional[int]


class Conversation(BaseModel):
    conversation_id: int
    user_id: int
    conversation_language: str


class Message(BaseModel):
    message_id: int
    user_id: int
    conversation_id: int
    is_from_user: bool
    message_text: str


class Explanation(BaseModel):
    explanation_id: int
    user_id: int
    message_id: int
    explanation_text: str


async def create_user(
    db_conn: asyncpg.Connection,
    discord_username: str,
    spoken_language: str,
    learning_language: str,
):
    new_user = await db_conn.fetchrow(
        "INSERT INTO users (discord_username, spoken_language, learning_language) VALUES ($1, $2, $3) RETURNING *",
        discord_username,
        spoken_language,
        learning_language,
    )
    return User(
        user_id=new_user.get("id"),
        discord_username=new_user.get("discord_username"),
        spoken_language=new_user.get("spoken_language"),
        learning_language=new_user.get("learning_language"),
    )


async def get_user_by_discord_username(db_conn: asyncpg.Connection, discord_username: str):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE discord_username = $1", discord_username)
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        discord_username=user.get("discord_username"),
        spoken_language=user.get("spoken_language"),
        learning_language=user.get("learning_language"),
    )


async def get_user(db_conn: asyncpg.Connection, user_id: int):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        discord_username=user.get("discord_username"),
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
        discord_username=user.get("discord_username"),
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


async def create_message(
    db_conn: asyncpg.Connection,
    user: User,
    is_from_user: bool,
    message_text: str,
):
    message = await db_conn.fetchrow(
        "INSERT INTO messages (user_id, is_from_user, message_text, message_language) VALUES ($1, $2, $3, $4) RETURNING *",
        user.user_id,
        is_from_user,
        message_text,
        user.learning_language,
    )

    return message


async def get_last_message(db_conn: asyncpg.Connection, user: User):
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

async def update_user_language(db_conn: asyncpg.Connection, user: User, learning_language: str):
    user = await db_conn.fetchrow(
        "UPDATE users SET learning_language = $1 WHERE id = $2 RETURNING *",
        learning_language,
        user.user_id,
    )
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        discord_username=user.get("discord_username"),
        spoken_language=user.get("spoken_language"),
        learning_language=user.get("learning_language"),
    )

async def create_explanation(db_conn: asyncpg.Connection, message: Message, explanation_text: str):
    explanation = await db_conn.fetchrow(
        "INSERT INTO explanations (user_id, message_id, explanation_text) VALUES ($1, $2, $3) RETURNING *",
        message.user_id,
        message.message_id,
        explanation_text,
    )

    return explanation.get("explanation_text")

async def get_explanation_by_message(db_conn: asyncpg.Connection, message: Message):
    explanation = await db_conn.fetchrow(
        "SELECT * FROM explanations WHERE message_id = $1",
        message.message_id,
    )
    if not explanation:
        return None

    return explanation.get("explanation_text")