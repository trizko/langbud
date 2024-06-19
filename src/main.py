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

from models.constants import LANGUAGE_MAPPING
from models.conversation import create_conversation, get_conversation, get_conversations_by_user_id
from models.explanation import create_explanation, get_explanation_by_message
from models.message import get_last_message_by_user, create_message, get_messages_by_conversation_id
from models.user import get_user_by_discord_username, create_user, update_user
from models.utils import format_messages_openai

from db import Database

load_dotenv()

# Setup the logger
logger = logging.getLogger("uvicorn")

# Setup database connection pooling object
database = Database(os.getenv("PG_URI"))

# Setup the OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def create_chatbot_response(db_conn, user, prompt):
    try:
        logger.info(f"Creating chatbot response for user {user} with prompt: {prompt}")
        await create_message(db_conn, user, is_from_user=True, message_text=prompt)
        conversation = await get_conversation(db_conn, user.active_conversation_id)
        raw_messages = await get_messages_by_conversation_id(db_conn, user.active_conversation_id)
        messages = await format_messages_openai(db_conn, user, raw_messages, conversation.conversation_language)
        response = openai_client.chat.completions.create(model="gpt-4o", messages=messages)
        content = response.choices[0].message.content
        await create_message(db_conn, user, is_from_user=False, message_text=content)
    except Exception as e:
        logger.error(f"An error occurred when creating chatbot response: {e}")
        return "An error occurred when creating chatbot response"

    return content


async def chatbot_explain(db_conn, user):
    latest_message = await get_last_message_by_user(db_conn, user)
    conversation = await get_conversation(db_conn, user.active_conversation_id)
    explanation = await get_explanation_by_message(db_conn, latest_message)
    if explanation:
        return explanation

    explain_messages = [
        {
            "role": "system",
            "content": f"You are a friendly {LANGUAGE_MAPPING[conversation.conversation_language]}-teaching chatbot. You take the users {LANGUAGE_MAPPING[conversation.conversation_language]} messages and explain them word for word in {LANGUAGE_MAPPING[user.spoken_language]}. Also, include ways you can respond to this message in {LANGUAGE_MAPPING[conversation.conversation_language]}.",
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


languages = [
    app_commands.Choice(name="Spanish", value="es"),
    app_commands.Choice(name="French", value="fr"),
    app_commands.Choice(name="German", value="de"),
    app_commands.Choice(name="Italian", value="it"),
    app_commands.Choice(name="Brazilian Portuguese", value="pt-BR"),
    app_commands.Choice(name="Turkish", value="tr"),
]


@tree.command(
    name="create-conversation",
    description="Creates a new conversation with the chosen language",
)
@app_commands.choices(languages=languages)
async def create_conversation(interaction, languages: app_commands.Choice[str]):
    try:
        await interaction.response.defer()
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_discord_username(connection, interaction.user.name)
            if not user:
                user = await create_user(connection, interaction.user.name, "en")

            conversation = await create_conversation(connection, user, languages.value)
            user = await update_user(connection, user.user_id, conversation.conversation_id)
        await interaction.followup.send(
            f"Conversation successfully created with {LANGUAGE_MAPPING[conversation.conversation_language]} language"
        )
    except Exception as e:
        await interaction.followup.send("An error occurred when creating the conversation")
        logger.error(f"An error occurred when creating the conversation: {e}")
        return


@tree.command(
    name="list-conversations",
    description="Lists all your conversations and their associated languages",
)
async def list_conversation(interaction):
    try:
        await interaction.response.defer()
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_discord_username(connection, interaction.user.name)
            conversations = await get_conversations_by_user(connection, user)
            if not conversations:
                await interaction.followup.send("You do not have any conversations")
                return

            response = "Your conversations are:\n"
            for conversation in conversations:
                response += f"Conversation ID: {conversation.conversation_id}, Language: {LANGUAGE_MAPPING[conversation.conversation_language]}\n"
            await interaction.followup.send(response)
    except Exception as e:
        await interaction.followup.send("An error occurred when listing the conversations")
        logger.error(f"An error occurred when listing the conversations: {e}")
        return


@tree.command(
    name="explain", description="explains the chatbots last response in detail"
)
async def explain(interaction):
    try:
        await interaction.response.defer(ephemeral=False, thinking=True)
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_discord_username(connection, interaction.user.name)
            explanation = await chatbot_explain(connection, user)
        await interaction.followup.send(explanation)
    except Exception as e:
        await interaction.followup.send(
            "An error occurred when explaining the chatbot response"
        )
        logger.error(f"An error occurred when explaining the chatbot response: {e}")
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
        user = await get_user_by_discord_username(connection, message.author.name)
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
