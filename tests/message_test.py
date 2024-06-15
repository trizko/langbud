import pytest

from models.message import Message, create_message, get_messages_by_conversation_id, get_messages_by_user_id, get_message, delete_message


@pytest.mark.asyncio
async def test_create_message(db_pool):
    async with db_pool.acquire() as connection:
        message = await create_message(connection, 1, 1, True, "test_create_message")
        assert message.message_id is not None
        assert message.user_id == 1
        assert message.conversation_id == 1
        assert message.is_from_user == True
        assert message.message_text == "test_create_message"


@pytest.mark.asyncio
async def test_get_messages_by_conversation_id(db_pool):
    async with db_pool.acquire() as connection:
        await create_message(connection, 1, 1, True, "test_get_messages_by_conversation_id_1")
        await create_message(connection, 1, 1, True, "test_get_messages_by_conversation_id_2")

        messages = await get_messages_by_conversation_id(connection, 1)
        assert len(messages) == 2
        for message in messages:
            assert message.conversation_id == 1


@pytest.mark.asyncio
async def test_get_messages_by_user_id(db_pool):
    async with db_pool.acquire() as connection:
        await create_message(connection, 1, 1, True, "test_get_messages_by_user_id_1")
        await create_message(connection, 1, 2, True, "test_get_messages_by_user_id_2")

        messages = await get_messages_by_user_id(connection, 1)
        assert len(messages) == 2
        for message in messages:
            assert message.user_id == 1


@pytest.mark.asyncio
async def test_get_message(db_pool):
    async with db_pool.acquire() as connection:
        message = await create_message(connection, 1, 1, True, "test_get_message")
        message = await get_message(connection, message.message_id)
        assert message.message_id is not None
        assert message.user_id == 1
        assert message.conversation_id == 1
        assert message.is_from_user == True
        assert message.message_text == "test_get_message"


@pytest.mark.asyncio
async def test_delete_message(db_pool):
    async with db_pool.acquire() as connection:
        message = await create_message(connection, 1, 1, True, "test_delete_message")
        await delete_message(connection, message.message_id)
        message = await get_message(connection, message.message_id)
        assert message is None