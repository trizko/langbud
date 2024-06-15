import asyncpg

from pydantic import BaseModel

from .message import Message

class Explanation(BaseModel):
    explanation_id: int
    user_id: int
    message_id: int
    explanation_text: str

    def from_query(query_result):
        return Explanation(
            explanation_id=query_result.get("id"),
            user_id=query_result.get("user_id"),
            message_id=query_result.get("message_id"),
            explanation_text=query_result.get("explanation_text"),
        )


async def create_explanation(db_conn: asyncpg.Connection, message: Message, explanation_text: str) -> Explanation:
    explanation = await db_conn.fetchrow(
        "INSERT INTO explanations (user_id, message_id, explanation_text) VALUES ($1, $2, $3) RETURNING *",
        message.user_id,
        message.message_id,
        explanation_text,
    )

    return Explanation(
        explanation_id=explanation.get("id"),
        user_id=explanation.get("user_id"),
        message_id=explanation.get("message_id"),
        explanation_text=explanation.get("explanation_text"),
    )


async def get_explanation_by_message(db_conn: asyncpg.Connection, message: Message) -> Explanation:
    explanation = await db_conn.fetchrow(
        "SELECT * FROM explanations WHERE message_id = $1",
        message.message_id,
    )
    if not explanation:
        return None

    return Explanation(
        explanation_id=explanation.get("id"),
        user_id=explanation.get("user_id"),
        message_id=explanation.get("message_id"),
        explanation_text=explanation.get("explanation_text"),
    )