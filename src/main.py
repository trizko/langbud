import os
import logging

import asyncio
import uvicorn

import discord
from discord import app_commands

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from models.constants import LANGUAGE_MAPPING
from models.conversation import create_conversation, get_conversation, get_conversations_by_user_id
from models.explanation import create_explanation, get_explanation_by_message
from models.message import get_last_message_by_user, create_message, get_messages_by_conversation_id, get_last_message_by_conversation_id
from models.user import get_user_by_discord_username, create_user, update_user
from models.utils import format_messages_openai

from db import Database
from llm import LLM

load_dotenv()

# Setup the logger
logger = logging.getLogger("uvicorn")

# Setup database connection pooling object
database = Database(os.getenv("PG_URI"))

# Setup the LLM client
llm = LLM(api_key=os.getenv("OPENAI_API_KEY"))


async def create_chatbot_response(db_conn, user, prompt):
    try:
        logger.info(f"Creating chatbot response for user {user} with prompt: {prompt}")
        await create_message(db_conn, user, is_from_user=True, message_text=prompt)
        conversation = await get_conversation(db_conn, user.active_conversation_id)
        raw_messages = await get_messages_by_conversation_id(db_conn, user.active_conversation_id)
        messages = await format_messages_openai(db_conn, user, raw_messages, conversation.conversation_language)
        content = llm.complete(model="gpt-4o", messages=messages)
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
        return explanation.explanation_text

    explain_messages = [
        {
            "role": "system",
            "content": f"You are a friendly {LANGUAGE_MAPPING[conversation.conversation_language].name}-teaching chatbot. You take the users {LANGUAGE_MAPPING[conversation.conversation_language].name} messages and explain them word for word in {LANGUAGE_MAPPING[user.spoken_language].name}. Also, include ways you can respond to this message in {LANGUAGE_MAPPING[conversation.conversation_language].name}.",
        },
    ]
    explain_messages.append({"role": "user", "content": latest_message.message_text})
    content = llm.complete(model="gpt-4o", messages=explain_messages, max_tokens=500)
    explanation = await create_explanation(db_conn, latest_message, content)

    return explanation.explanation_text


# Setup the Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discord_client = discord.Client(intents=intents)
tree = app_commands.CommandTree(discord_client)


languages = [
    app_commands.Choice(name="Spanish", value="es"),
    app_commands.Choice(name="Mexican Spanish", value="es-MX"),
    app_commands.Choice(name="French", value="fr"),
    app_commands.Choice(name="German", value="de"),
    app_commands.Choice(name="Swiss German", value="de-ch"),
    app_commands.Choice(name="Italian", value="it"),
    app_commands.Choice(name="Brazilian Portuguese", value="pt-BR"),
    app_commands.Choice(name="Turkish", value="tr"),
    app_commands.Choice(name="Japanese", value="jp"),
]


@tree.command(
    name="new-conversation",
    description="Creates a new conversation with the chosen language",
)
@app_commands.choices(language=languages)
async def new_conversation(interaction, language: app_commands.Choice[str]):
    try:
        await interaction.response.defer()
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_discord_username(connection, interaction.user.name)
            if not user:
                user = await create_user(connection, interaction.user.name, "en")

            conversation = await create_conversation(connection, user, language.value)
            user = await update_user(connection, user.user_id, conversation.conversation_id)
        await interaction.followup.send(
            f"Great! Let's start speaking {LANGUAGE_MAPPING[conversation.conversation_language].name}. {LANGUAGE_MAPPING[conversation.conversation_language].greeting}!"
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
            if not user:
                user = await create_user(connection, interaction.user.name, "en")

            conversations = await get_conversations_by_user_id(connection, user.user_id)
            if not conversations:
                await interaction.followup.send("You do not have any conversations. Create one with the `/new-conversation <language>` slash command.")
                return


            # Prepare table header
            response = "Your can select a conversation to activate with the `/select-converation <conversation_id>` slash command:\n"
            response += "```"
            response += f"{'Conversation ID':<15} {'Language':<22} {'Last Message':<50}\n"
            response += f"{'-' * 15} {'-' * 22} {'-' * 50}\n"

            # Add table rows
            for idx, conversation in enumerate(conversations):
                latest_message = await get_last_message_by_conversation_id(connection, conversation.conversation_id)

                message_text = ""
                if not latest_message:
                     message_text = "No messages"
                else:
                    message_text = latest_message.message_text

                index = 0
                if conversation.conversation_id == user.active_conversation_id:
                    index = f"{idx+1} (active)"
                else:
                    index = idx+1

                response += f"{index:<15} {LANGUAGE_MAPPING[conversation.conversation_language].name:<22} {message_text[0:50 if len(message_text)>50 else len(message_text)]}...\n"

            response += "```"

            await interaction.followup.send(response)
    except Exception as e:
        await interaction.followup.send("An error occurred when listing the conversations")
        logger.error(f"An error occurred when listing the conversations: {e}")
        return


@tree.command(
    name="select-conversation",
    description="Selects a conversation to activate",
)
@app_commands.describe(conversation_id="The ID of the conversation to activate")
async def select_conversation(interaction, conversation_id: int):
    try:
        await interaction.response.defer()
        db_pool = await database.get_pool()
        async with db_pool.acquire() as connection:
            user = await get_user_by_discord_username(connection, interaction.user.name)
            if not user:
                user = await create_user(connection, interaction.user.name, "en")

            conversations = await get_conversations_by_user_id(connection, user.user_id)
            if not conversations:
                await interaction.followup.send("You do not have any conversations. Create one with the `/new-conversation <language>` slash command.")
                return

            if conversation_id > len(conversations) or conversation_id < 1:
                await interaction.followup.send("Invalid conversation ID")
                return

            conversation = conversations[conversation_id - 1]

            user = await update_user(connection, user.user_id, conversation.conversation_id)
        await interaction.followup.send(
            f"Great! Let's start speaking {LANGUAGE_MAPPING[conversation.conversation_language].name}. {LANGUAGE_MAPPING[conversation.conversation_language].greeting}!"
        )
    except Exception as e:
        await interaction.followup.send("An error occurred when activating the conversation")
        logger.error(f"An error occurred when activating the conversation: {e}")
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
            user = await create_user(connection, message.author.name, "en")

        # Check if the user has an active conversation
        if not user.active_conversation_id:
            await message.channel.send("You do not have an active conversation. Create one with the `/new-conversation <language>` slash command.")
        elif isinstance(message.channel, discord.DMChannel):
            response = await create_chatbot_response(connection, user, message.content)
            await message.channel.send(response)
        elif discord_client.user in message.mentions:
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
