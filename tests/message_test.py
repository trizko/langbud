import pytest

from models.user import User, create_user
from models.message import Message, create_message, get_last_message_by_user, get_messages_by_conversation_id, get_message, delete_message


@pytest.mark.asyncio
async def test_create_message(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_last_message_by_user", "en")
        conversation = await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)

        message = await create_message(connection, user, True, "test_create_message")
        assert message.message_id is not None
        assert message.user_id == 1
        assert message.conversation_id == 1
        assert message.is_from_user == True
        assert message.message_text == "test_create_message"


@pytest.mark.asyncio
async def test_get_last_message_by_user(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_last_message_by_user", "en")
        conversation = await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)

        await create_message(connection, user, True, "test_get_last_message_by_user_1")
        await create_message(connection, user, False, "test_get_last_message_by_user_2")
        await create_message(connection, user, True, "test_get_last_message_by_user_3")
        await create_message(connection, user, False, "test_get_last_message_by_user_4")

        message = await get_last_message_by_user(connection, user)
        assert message.message_id is not None
        assert message.user_id == user.user_id
        assert message.conversation_id == conversation.conversation_id
        assert message.is_from_user == False
        assert message.message_text == "test_get_last_message_by_user_4"


@pytest.mark.asyncio
async def test_get_messages_by_conversation_id(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_last_message_by_user", "en")
        conversation = await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)

        await create_message(connection, user, True, "test_get_messages_by_conversation_id_1")
        await create_message(connection, user, True, "test_get_messages_by_conversation_id_2")

        messages = await get_messages_by_conversation_id(connection, user.active_conversation_id)
        assert len(messages) == 2
        for message in messages:
            assert message.conversation_id == 1


@pytest.mark.asyncio
async def test_get_message(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_last_message_by_user", "en")
        conversation = await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)
        new_message = await create_message(connection, user, True, "test_get_message")

        message = await get_message(connection, new_message.message_id)
        assert message.message_id is not None
        assert message.user_id == 1
        assert message.conversation_id == 1
        assert message.is_from_user == True
        assert message.message_text == "test_get_message"


@pytest.mark.asyncio
async def test_delete_message(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_last_message_by_user", "en")
        conversation = await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)
        new_message = await create_message(connection, user, True, "test_get_message")

        await delete_message(connection, new_message.message_id)
        message = await get_message(connection, new_message.message_id)
        assert message is None
