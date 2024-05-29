import asyncpg
from pydantic import BaseModel
from typing import List, Optional


class User(BaseModel):
    user_id: int
    username: str
    spoken_language: str
    learning_language: str
    messages: Optional[List[str]] = []


async def create_user(db_conn: asyncpg.Connection, username: str, spoken_language: str, learning_language: str):
    new_user = await db_conn.fetchrow(
        "INSERT INTO users (username, spoken_language, learning_language) VALUES ($1, $2, $3) RETURNING *",
        username,
        spoken_language,
        learning_language
    )
    return User(
        user_id=new_user.get("id"),
        username=new_user.get("username"),
        spoken_language=new_user.get("spoken_language"),
        learning_language=new_user.get("learning_language")
    )

async def get_user_by_username(db_conn: asyncpg.Connection, username: str):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
    if not user:
        return None

    return User(
        user_id=user.get("id"),
        username=user.get("username"),
        spoken_language=user.get("spoken_language"),
        learning_language=user.get("learning_language")
    )

async def get_user(db_conn: asyncpg.Connection, user_id: int):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    if not user:
        return None

async def update_user(db_conn: asyncpg.Connection, user_id: int):
    pass

async def delete_user(db_conn: asyncpg.Connection, user_id: int):
    pass

async def get_user_messages(db_conn: asyncpg.Connection, user_id: int):
    pass