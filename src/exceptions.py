from fastapi.responses import RedirectResponse

class RequiresLoginError(Exception):
    pass

async def handle_requires_login_error(*_):
    return RedirectResponse(url="/")