import os
import logging

import asyncio
import uvicorn

import discord
from discord import app_commands

from contextlib import asynccontextmanager
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
    {
        "role": "system",
        "content": "You are a friendly Spanish-speaking chatbot. Your task is to help the user learn Spanish. You should continue the conversation in Spanish, but if the user makes a mistake, correct them in English.",
    },
]
explain_messages = [
    {
        "role": "system",
        "content": "You are a friendly Spanish-teaching chatbot. You take the users Spanish messages and explain them word for word in English. Also, include ways you can respond to this message in Spanish.",
    },
]


def create_chatbot_response(prompt):
    messages.append({"role": "user", "content": prompt})
    response = openai_client.chat.completions.create(model="gpt-4", messages=messages)
    content = response.choices[0].message.content
    messages.append({"role": "assistant", "content": content})

    return content


def chatbot_explain():
    latest_message = messages[-1]
    explain_messages.append({"role": "user", "content": latest_message["content"]})
    response = openai_client.chat.completions.create(
        model="gpt-4", messages=explain_messages
    )
    content = response.choices[0].message.content
    explain_messages.pop()

    return content


# Setup the Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discord_client = discord.Client(intents=intents)
tree = app_commands.CommandTree(discord_client)


@tree.command(
    name="explain", description="explains the chatbots last response in detail"
)
async def explain(interaction):
    await interaction.response.defer()
    explanation = chatbot_explain()
    await interaction.followup.send(explanation)


@discord_client.event
async def on_ready():
    await tree.sync()
    logger.info(f"Discord bot logged in as {discord_client.user}")


@discord_client.event
async def on_message(message):
    if message.author == discord_client.user:
        return

    # Respond to direct messages
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send(create_chatbot_response(message.content))

    # Respond to mentions
    if discord_client.user in message.mentions:
        await message.channel.send(create_chatbot_response(message.content))


# Setup FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the discord client in a separate task
    task = asyncio.create_task(discord_client.start(os.getenv("DISCORD_BOT_TOKEN")))
    yield
    # Shutdown the discord client
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)


class UserMessage(BaseModel):
    prompt: str


class Response(BaseModel):
    message: str


@app.post("/chat/")
async def generate_text(message: UserMessage):
    return Response(message=create_chatbot_response(message.prompt))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
