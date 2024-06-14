from pydantic import BaseModel

class Explanation(BaseModel):
    explanation_id: int
    user_id: int
    message_id: int
    explanation_text: str
