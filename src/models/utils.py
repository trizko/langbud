import asyncpg

from typing import List

from .message import Message
from .user import User
from .constants import LANGUAGE_MAPPING


async def format_messages_openai(db_conn: asyncpg.Connection, user: User, messages: List[Message], language: str) -> List[dict]:
    if not messages:
        return []

    system_message = {
        "role": "system",
        "content": f"You are a friendly {LANGUAGE_MAPPING[language].name}-speaking chatbot named Maya. Your task is to help the user learn {LANGUAGE_MAPPING[language].name}. You should continue the conversation in {LANGUAGE_MAPPING[language].name}, but if the user makes a mistake, correct them in {LANGUAGE_MAPPING[user.spoken_language].name}.",
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
