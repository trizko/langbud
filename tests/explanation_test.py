import pytest

from models.user import create_user, get_user
from models.conversation import create_conversation
from models.message import create_message
from models.explanation import create_explanation, get_explanation_by_message


@pytest.mark.asyncio
async def test_create_explanation(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_create_explanation", "en")
        await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)

        message = await create_message(
            connection, user, True, "test_create_explanation"
        )
        explanation = await create_explanation(
            connection, message, "test_create_explanation"
        )
        assert explanation.user_id == user.user_id
        assert explanation.message_id == message.message_id
        assert explanation.explanation_text == "test_create_explanation"


@pytest.mark.asyncio
async def test_get_explanation_by_message(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(
            connection, "test_get_explanation_by_message", "en"
        )
        await create_conversation(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)

        message = await create_message(
            connection, user, True, "test_get_explanation_by_message"
        )
        await create_explanation(connection, message, "test_get_explanation_by_message")
        result = await get_explanation_by_message(connection, message)
        assert result.user_id == user.user_id
        assert result.message_id == message.message_id
        assert result.explanation_text == "test_get_explanation_by_message"
