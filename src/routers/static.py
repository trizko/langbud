from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import FileResponse, RedirectResponse

from dependencies import get_user_session


router = APIRouter()


@router.get('/')
async def index(request: Request):
    user_session = request.session.get("user")
    if user_session:
        return RedirectResponse(url="/chat/")
    return FileResponse("src/frontend/index.html")


@router.get('/chat/')
async def chat(_ = Depends(get_user_session)):
    return FileResponse("src/frontend/app.html")


@router.get('/health', status_code=status.HTTP_200_OK)
async def healthcheck():
    return { "status": "OK" }
