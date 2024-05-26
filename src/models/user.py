import asyncpg
from pydantic import BaseModel
from typing import List


class User(BaseModel):
    user_id: int
    username: str
    spoken_language: str
    learning_language: str
    messages: List[dict]


async def create_user(self):
    pass

async def get_user(self, user_id: int):
    pass

async def get_user_by_username(self, username: str):
    pass

async def update_user(self, user_id: int):
    pass

async def delete_user(self, user_id: int):
    pass

async def get_user_messages(self, user_id: int):
    pass