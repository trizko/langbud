from fastapi import Depends, Request

async def get_db_pool(request: Request):
    return await request.app.state.db.get_pool()
