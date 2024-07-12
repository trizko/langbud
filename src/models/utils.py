import asyncpg

from typing import List

from utils.prompts import system_prompt

from .message import Message
from .user import User


async def format_messages_openai(db_conn: asyncpg.Connection, user: User, messages: List[Message], language: str) -> List[dict]:
    if not messages:
        return []

    system_message = {
        "role": "system",
        "content": system_prompt(learning=language, fluent=user.spoken_language),
    }
    formatted_messages = [
        {
            "role": "user" if message.is_from_user else "assistant",
            "content": message.message_text,
        }
        for message in messages
    ]
    formatted_messages.insert(0, system_message)
    return formatted_messages
