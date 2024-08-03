from fastapi import Request
from fastapi.responses import RedirectResponse

async def get_db_pool(request: Request):
    return await request.app.state.db.get_pool()

async def get_user_session(request: Request):
    user_session = request.session.get("user")
    if not user_session:
        return RedirectResponse(url="/")

    return user_session