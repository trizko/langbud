import pytest

from models.user import User, create_user, get_user, get_user_by_discord_username

@pytest.mark.asyncio
async def test_create_user(db_pool):
    async with db_pool.acquire() as connection:
        user = await create_user(connection, "test_user", "en")
        assert user.discord_username == "test_user"
        assert user.spoken_language == "en"
        assert user.active_conversation_id is not None
        assert user.user_id is not None

@pytest.mark.asyncio
async def test_get_user(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_user", "en")
        user_id = new_user.user_id
        user = await get_user(connection, user_id)
        assert user.discord_username == new_user.discord_username
        assert user.spoken_language == new_user.spoken_language
        assert user.active_conversation_id == new_user.active_conversation_id
        assert user.user_id == new_user.user_id

@pytest.mark.asyncio
async def test_get_user_by_discord_username(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_get_user_by_discord_username", "en")
        user = await get_user_by_discord_username(connection, "test_get_user_by_discord_username")
        assert user.discord_username == new_user.discord_username
        assert user.spoken_language == new_user.spoken_language
        assert user.active_conversation_id == new_user.active_conversation_id
        assert user.user_id == new_user.user_id
