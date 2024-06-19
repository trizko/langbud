import os
import time

import asyncpg
import docker
import pytest
import pytest_asyncio

import psycopg2
from psycopg2 import OperationalError


def wait_for_pg_ready(host, port, user, password, db, timeout=60):
    start_time = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password, dbname=db
            )
            conn.close()
            break
        except OperationalError:
            if time.time() - start_time >= timeout:
                raise TimeoutError("Could not connect to the PostgreSQL server.")
            time.sleep(0.5)


@pytest.fixture(scope="session")
def docker_pg():
    client = docker.from_env()

    # Check if container already exists. if so, stop and remove it
    existing_containers = client.containers.list(all=True, filters={"name": "test-postgres"})
    for container in existing_containers:
        if container.status == "running":
            container.stop()
        container.remove()

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
