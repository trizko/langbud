import asyncpg

from pydantic import BaseModel
from typing import List, Optional


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


async def get_user_by_discord_username(
    db_conn: asyncpg.Connection, discord_username: str
) -> User:
    user = await db_conn.fetchrow(
        "SELECT * FROM users WHERE discord_username = $1", discord_username
    )
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


async def update_user_language(
    db_conn: asyncpg.Connection, user: User, spoken_language: str
) -> User:
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
