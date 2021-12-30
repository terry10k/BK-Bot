import discord
from discord.ext import commands

import music

cogs =[music]


client = commands.Bot(command_prefix="./", intents = discord.Intents.all())


for i in range(len(cogs)):
  cogs[i].setup(client)

client.run("OTI2MDIyNTU0OTE1ODM1OTA0.Yc1ntQ.4Zxv_ZiV0PbGsF1nXalR5lRAB28")