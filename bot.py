import nextcord
from nextcord.ext import commands
import config

TOKEN = config.BOT_TOKEN

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


extensions = ['cogs.fun_commands']

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)
    bot.run(TOKEN)
