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
