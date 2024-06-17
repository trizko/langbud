import pytest

from models.user import (
    create_user,
    get_user,
    get_user_by_discord_username,
    update_user,
    update_user_language,
    delete_user,
)


@pytest.mark.asyncio
async def test_create_user(db_pool):
    async with db_pool.acquire() as connection:
        user = await create_user(connection, "test_user", "en")
        assert user.discord_username == "test_user"
        assert user.spoken_language == "en"
        assert user.active_conversation_id is None
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
        new_user = await create_user(
            connection, "test_get_user_by_discord_username", "en"
        )
        user = await get_user_by_discord_username(
            connection, "test_get_user_by_discord_username"
        )
        assert user.discord_username == new_user.discord_username
        assert user.spoken_language == new_user.spoken_language
        assert user.active_conversation_id == new_user.active_conversation_id
        assert user.user_id == new_user.user_id


@pytest.mark.asyncio
async def test_update_user(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_update_user", "en")
        assert new_user.active_conversation_id is None

        await update_user(connection, new_user.user_id, 420)
        user = await get_user(connection, new_user.user_id)

        assert user.user_id == new_user.user_id
        assert user.discord_username == "test_update_user"
        assert user.spoken_language == "en"
        assert user.active_conversation_id == 420


@pytest.mark.asyncio
async def test_update_user_language(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_update_user_language", "en")
        assert new_user.spoken_language == "en"

        await update_user_language(connection, new_user, "es")
        user = await get_user(connection, new_user.user_id)

        assert user.user_id == new_user.user_id
        assert user.discord_username == "test_update_user_language"
        assert user.spoken_language == "es"
        assert user.active_conversation_id is None


@pytest.mark.asyncio
async def test_delete_user(db_pool):
    async with db_pool.acquire() as connection:
        new_user = await create_user(connection, "test_delete_user", "en")
        user_id = new_user.user_id
        user = await get_user(connection, user_id)
        assert user is not None

        await delete_user(connection, user_id)
        user = await get_user(connection, user_id)
        assert user is None
