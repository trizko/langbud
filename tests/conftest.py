import os
import pytest
import pytest_asyncio
import docker
import time
import asyncpg


@pytest.fixture(scope="session")
def docker_pg():
    client = docker.from_env()
    container = client.containers.run(
        "postgres",
        name="test-postgres",
        environment={
            "POSTGRES_PASSWORD": "password",
            "POSTGRES_USER": "user",
            "POSTGRES_DB": "testdb",
        },
        ports={"5432/tcp": 5432},
        detach=True,
    )
    time.sleep(5)  # Give some time for the database to initialize
    yield
    container.stop()
    container.remove()


@pytest_asyncio.fixture
async def db_pool(docker_pg):
    pool = await asyncpg.create_pool(
        user="user", password="password", database="testdb", host="127.0.0.1", port=5432
    )

    # run database migrations with dbmt
    os.system(
        "dbmt up --db-url postgresql://user:password@localhost:5432/testdb --migrations-dir migrations"
    )

    yield pool
    await pool.close()
