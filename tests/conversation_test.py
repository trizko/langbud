import pytest

from models.conversation import Conversation, create_conversation, get_conversation, get_conversations_by_user_id
from models.user import User, create_user, get_user


@pytest.mark.asyncio
async def test_create_conversation(db_pool):
    async with db_pool.acquire() as connection:
        user = await create_user(connection, "test_create_conversation", "en", "es")
        conversation = await create_conversation(connection, user, "es")
        user = await get_user(connection, user.user_id)
        assert conversation.user_id == user.user_id
        assert conversation.conversation_language == "es"
        assert conversation.conversation_id == user.active_conversation_id

@pytest.mark.asyncio
async def test_get_conversation(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_conversation", "en", "es")
        new_conversation = await create_conversation(connection, new_user, "es")
        conversation_id = new_conversation.conversation_id
        conversation = await get_conversation(connection, conversation_id)
        user = await get_user(connection, new_user.user_id)
        assert conversation.user_id == user.user_id
        assert conversation.conversation_language == "es"
        assert conversation.conversation_id == user.active_conversation_id

@pytest.mark.asyncio
async def test_get_conversations_by_user_id(db_pool):
    async with db_pool.acquire() as connection:
        user = await create_user(connection, "test_get_conversations_by_user_id", "en", "es")
        conversation = await create_conversation(connection, user, "es")
        conversations = await get_conversations_by_user_id(connection, user.user_id)
        assert len(conversations) == 2
        assert conversations[1].user_id == user.user_id
        assert conversations[1].conversation_language == "es"
        assert conversations[1].conversation_id == user.active_conversation_id