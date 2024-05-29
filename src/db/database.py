import asyncpg


class Database:
    def __init__(self, dsn: str = None):
        self._pool = None
        self.dsn = dsn

    async def connect(self):
        self._pool = await asyncpg.create_pool(dsn=self.dsn)

    async def disconnect(self):
        await self._pool.close()

    async def get_pool(self):
        if self._pool is None:
            await self.connect()
        return self._pool
