from typing import List

from openai import OpenAI


class LLM:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
    

    async def complete(self, messages: List[dict], model: str = "gpt-4o", max_tokens: int = None) -> str:
        response = await openai_client.chat.completions.create(model=model, messages=messages, max_tokens=max_tokens)
        content = response.choices[0].message.content
        return content
