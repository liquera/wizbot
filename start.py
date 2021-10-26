import os
import sys
import asyncio
import discord
from discord.ext import commands
import strings as c
from dotenv import load_dotenv

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=c.prefix, intents=intents, help_command=None)

if __name__ == '__main__':
    bot.load_extension('cog')

bot.run(TOKEN)
