from nextcord.ext import commands
import nextcord


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping",
                            description="It responds with Pong!.")
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Pong!")


def setup(bot):
    bot.add_cog(FunCommands(bot))
