import nextcord
from nextcord.ext import commands
import os
import json
from db.database import init_db

init_db()

with open('config/config.json') as config_file:
    config = json.load(config_file)

intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is running!')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('__'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.getenv('DISCORD_TOKEN'))
