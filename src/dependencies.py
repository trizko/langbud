from fastapi import Request

async def get_db_pool(request: Request):
    return await request.app.state.db.get_pool()
