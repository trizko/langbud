from pydantic import BaseModel


class Message(BaseModel):
    message_id: int
    user_id: int
    conversation_id: int
    is_from_user: bool
    message_text: str

    def from_query(query_result):
        return Message(
            message_id=query_result.get("id"),
            user_id=query_result.get("user_id"),
            conversation_id=query_result.get("conversation_id"),
            is_from_user=query_result.get("is_from_user"),
            message_text=query_result.get("message_text"),
        )
