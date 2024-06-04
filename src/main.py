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

from models.user import (
    create_user,
    get_user_by_username,
    create_message,
    create_explanation,
    get_explanation_by_message,
    get_messages_by_user,
    get_last_message,
    update_user_language,
    LANGUAGE_MAPPING,
)

from db import Database

load_dotenv()

# Setup the logger
logger = logging.getLogger("uvicorn")

# Setup database connection pooling object
database = Database(os.getenv("PG_URI"))

# Setup the OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def create_chatbot_response(db_conn, user, prompt):
    logger.info(f"Creating chatbot response for user {user} with prompt: {prompt}")
    await create_message(db_conn, user, is_from_user=True, message_text=prompt)
    messages = await get_messages_by_user(db_conn, user)
    response = openai_client.chat.completions.create(model="gpt-4o", messages=messages)
    content = response.choices[0].message.content
    await create_message(
        db_conn, user, is_from_user=False, message_text=content
    )

    return content


async def chatbot_explain(db_conn, user):
    latest_message = await get_last_message(db_conn, user)
    explanation = await get_explanation_by_message(db_conn, latest_message)
    if explanation:
        return explanation

    explain_messages = [
        {
            "role": "system",
            "content": f"You are a friendly {LANGUAGE_MAPPING[user.learning_language]}-teaching chatbot. You take the users {LANGUAGE_MAPPING[user.learning_language]} messages and explain them word for word in {LANGUAGE_MAPPING[user.spoken_language]}. Also, include ways you can respond to this message in {LANGUAGE_MAPPING[user.learning_language]}.",
        },
    ]
    explain_messages.append({"role": "user", "content": latest_message.message_text})
    response = openai_client.chat.completions.create(
        model="gpt-4o", messages=explain_messages
    )
    content = response.choices[0].message.content
    explanation = await create_explanation(db_conn, latest_message, content)

    return explanation


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
    try:
        await interaction.response.defer(ephemeral=False, thinking=True)
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_username(connection, interaction.user.name)
            explanation = await chatbot_explain(connection, user)
        await interaction.followup.send(explanation)
    except Exception as e:
        await interaction.followup.send(f"An error occurred when explaining the chatbot response")
        logger.error(f"An error occurred when explaining the chatbot response: {e}")
        return


@tree.command(name="select-language", description="Selects the language you want to learn from list of supported options")
@app_commands.describe(languages="Select the language you want to learn")
@app_commands.choices(languages=[
    app_commands.Choice(name="Spanish", value="es"),
    app_commands.Choice(name="French", value="fr"),
    app_commands.Choice(name="German", value="de"),
    app_commands.Choice(name="Italian", value="it"),
    app_commands.Choice(name="Brazilian Portuguese", value="pt-BR"),
    app_commands.Choice(name="Turkish", value="tr"),
])
async def select_language(interaction, languages: app_commands.Choice[str]):
    try:
        await interaction.response.defer()
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_username(connection, interaction.user.name)
            if not user:
                user = await create_user(connection, interaction.user.name, "en", languages.value)
            else:
                user = await update_user_language(connection, user, languages.value)
        await interaction.followup.send(f"User language successfully set to {LANGUAGE_MAPPING[user.learning_language]}")
    except Exception as e:
        await interaction.followup.send(f"An error occurred when selecting the language")
        logger.error(f"An error occurred when selecting the language: {e}")
        return



@discord_client.event
async def on_ready():
    await tree.sync()
    logger.info(f"Discord bot logged in as {discord_client.user}")


@discord_client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == discord_client.user:
        return

    # Ignore empty messages
    if not message.content:
        return

    # Get or create the user
    db_pool = await database.get_pool()
    async with db_pool.acquire() as connection:
        user = await get_user_by_username(connection, message.author.name)
        if not user:
            user = await create_user(connection, message.author.name, "en", "es")

        # Respond to direct messages
        if isinstance(message.channel, discord.DMChannel):
            response = await create_chatbot_response(connection, user, message.content)
            await message.channel.send(response)

        # Respond to mentions
        if discord_client.user in message.mentions:
            response = await create_chatbot_response(connection, user, message.content)
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
