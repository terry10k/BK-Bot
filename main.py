import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import music


load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

cogs =[music]


client = commands.Bot(command_prefix="./", intents = discord.Intents.all())


for i in range(len(cogs)):
  cogs[i].setup(client)

#your own token
client.run(BOT_TOKEN)

