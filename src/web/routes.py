from pydantic import BaseModel
from fastapi import APIRouter


class UserMessage(BaseModel):
    prompt: str


class Response(BaseModel):
    message: str


router = APIRouter()


@router.post('/chat/')
async def generate_text(message: UserMessage):
    return Response(message="200 OK")


def setup_routes(app):
    app.include_router(router)
    return app