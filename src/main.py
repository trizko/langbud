import os
import logging

import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
logger = logging.getLogger("uvicorn")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
messages = [
    {"role": "system", "content": "You are a friendly Spanish-speaking chatbot. Your task is to help the user learn Spanish. You should continue the conversation in Spanish, but if the user makes a mistake, correct them in English."},
]

def create_chatbot_response(prompt):
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    content = response.choices[0].message.content
    messages.append({"role": "system", "content": content})

    return content

app = FastAPI()

class UserMessage(BaseModel):
    prompt: str

class Response(BaseModel):
    message: str

@app.post("/chat/")
async def generate_text(message: UserMessage):
    return Response(message=create_chatbot_response(message.prompt))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)