import json
import os

from pydantic import BaseModel


class User(BaseModel):
    username: str
    spoken_language: str
    learning_language: str
    messages: [dict]

    def __init__(
        self,
        username: str,
        spoken_language: str,
        learning_language: str,
        messages: [dict],
    ):
        self.username = username
        self.spoken_language = spoken_language
        self.learning_language = learning_language
        self.messages = messages
