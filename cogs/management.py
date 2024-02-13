from nextcord.ext import commands
import nextcord


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="clear", description="Clear a specified number of messages.")
    async def clear(self, interaction: nextcord.Interaction, number: int):
        if interaction.user.guild_permissions.manage_messages:
            if number < 1:
                await interaction.response.send_message("You must delete at least one message.", ephemeral=True)
                return

            deleted = await interaction.channel.purge(limit=number)
            await interaction.response.send_message(f"Deleted {len(deleted)} message(s)", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)


def setup(bot):
    bot.add_cog(Management(bot))
