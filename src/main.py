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

from models.user import create_user, get_user_by_username, create_message, get_messages_by_user

from db import Database

load_dotenv()

# Setup the logger
logger = logging.getLogger("uvicorn")

# Setup database connection pooling object
database = Database(os.getenv("PG_URI"))

# Setup the OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
explain_messages = [
    {
        "role": "system",
        "content": "You are a friendly Spanish-teaching chatbot. You take the users Spanish messages and explain them word for word in English. Also, include ways you can respond to this message in Spanish.",
    },
]


async def create_chatbot_response(db_conn, user, prompt):
    logger.info(f"Creating chatbot response for user {user} with prompt: {prompt}")
    message = await create_message(db_conn, user.user_id, is_from_user=True, message_text=prompt)
    messages = await get_messages_by_user(db_conn, user)
    response = openai_client.chat.completions.create(model="gpt-4", messages=messages)
    content = response.choices[0].message.content
    message = await create_message(db_conn, user.user_id, is_from_user=False, message_text=content)

    return content


def chatbot_explain():
    latest_message = messages[-1]
    explain_messages.append({"role": "user", "content": latest_message["content"]})
    response = openai_client.chat.completions.create(
        model="gpt-4o", messages=explain_messages
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
    
    # Get or create the user
    db_pool = await database.get_pool()
    async with db_pool.acquire() as connection:
        user = await get_user_by_username(connection, message.author.name)
        if not user:
            user = await create_user(connection, message.author.name, "en", "es")
        
        logger.info(f"Received message from {message.author.name}: {message.content}")
        response = await create_chatbot_response(connection, user, message.content)

        # Respond to direct messages
        if isinstance(message.channel, discord.DMChannel):
            await message.channel.send(response)

        # Respond to mentions
        if discord_client.user in message.mentions:
            await message.channel.send(response)


# Setup FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the discord client in a separate task
    task = asyncio.create_task(discord_client.start(os.getenv("DISCORD_BOT_TOKEN")))
    # Connect to the database
    await database.connect()
    yield
    # Close the database connection
    await database.disconnect()
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
