import pytest

from models.user import User, create_user

@pytest.mark.asyncio
async def test_create_user(db_pool):
    async with db_pool.acquire() as connection:
        user = await create_user(connection, "test_user", "en", "es")
        assert user.discord_username == "test_user"
        assert user.spoken_language == "en"
        assert user.learning_language == "es"
        assert user.active_conversation_id is not None
        assert user.user_id is not None
