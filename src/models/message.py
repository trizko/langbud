from pydantic import BaseModel


class Message(BaseModel):
    message_id: int
    user_id: int
    conversation_id: int
    is_from_user: bool
    message_text: str
