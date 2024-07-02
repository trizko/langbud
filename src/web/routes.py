from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


class UserMessage(BaseModel):
    prompt: str


class Response(BaseModel):
    message: str


router = APIRouter()


@router.post('/chat/')
async def generate_text(message: UserMessage):
    return Response(message="200 OK")


@router.get('/')
async def index():
    return FileResponse("src/web/frontend/index.html")


@router.get('/login/')
async def login():
    return FileResponse("src/web/frontend/login.html")


def setup_routes(app):
    app.mount("/static", StaticFiles(directory="src/web/frontend"), name="static")
    app.include_router(router)
    return app