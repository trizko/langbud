import os
import logging

import discord
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

# Setup the logger
logger = logging.getLogger("uvicorn")

# Setup the OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
messages = [
    {"role": "system", "content": "You are a friendly Spanish-speaking chatbot. Your task is to help the user learn Spanish. You should continue the conversation in Spanish, but if the user makes a mistake, correct them in English."},
]

def create_chatbot_response(prompt):
    messages.append({"role": "user", "content": prompt})
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    content = response.choices[0].message.content
    messages.append({"role": "system", "content": content})

    return content

# Setup the Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f'We have logged in as {discord_client.user}')

@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    # Respond to direct messages
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send('Hello! How can I help you today?')

    # Respond to mentions
    if discord_client.user in message.mentions:
        await message.channel.send('You mentioned me!')

# Setup FastAPI app
app = FastAPI()

class UserMessage(BaseModel):
    prompt: str

class Response(BaseModel):
    message: str

@app.post("/chat/")
async def generate_text(message: UserMessage):
    return Response(message=create_chatbot_response(message.prompt))

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    discord_client.run(os.getenv('DISCORD_BOT_TOKEN'))