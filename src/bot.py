import os

import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Respond to direct messages
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send('Hello! How can I help you today?')

    # Respond to mentions
    if client.user in message.mentions:
        await message.channel.send('You mentioned me!')

client.run(os.getenv('DISCORD_BOT_TOKEN'))
