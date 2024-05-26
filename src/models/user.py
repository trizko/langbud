import asyncpg
from pydantic import BaseModel
from typing import List


class User(BaseModel):
    user_id: int
    username: str
    spoken_language: str
    learning_language: str
    messages: List[dict]


async def create_user(db_conn: asyncpg.Connection, username: str, spoken_language: str, learning_language: str):
    new_user = await db_conn.fetchrow(
        "INSERT INTO users (username, spoken_language, learning_language) VALUES ($1, $2, $3)",
        username,
        spoken_language,
        learning_language
    )
    return new_user

async def get_user_by_username(db_conn: asyncpg.Connection, username: str):
    user = await db_conn.fetchrow("SELECT * FROM users WHERE username = $1", username)
    return user

async def get_user(db_conn: asyncpg.Connection, user_id: int):
    pass

async def update_user(db_conn: asyncpg.Connection, user_id: int):
    pass

async def delete_user(db_conn: asyncpg.Connection, user_id: int):
    pass

async def get_user_messages(db_conn: asyncpg.Connection, user_id: int):
    pass