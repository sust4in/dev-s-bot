from nextcord.ext import commands
import nextcord
import feedparser
from datetime import datetime, timedelta
from utils.newsletter_utils import NewsletterUtils


class Newsletter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.newsletter_utils = NewsletterUtils()

    async def fetch_rss_items(self):
        items = []
        response = self.newsletter_utils.get_resources()
        if response['status'] == 'ok' and response['data']:
            for rss_record in response['data']:
                feed = feedparser.parse(rss_record.url)
                for entry in feed.entries:
                    published_date = datetime(*entry.published_parsed[:6])
                    if datetime.now() - published_date < timedelta(days=1):
                        items.append((entry.title, entry.link))
        return items

    @nextcord.slash_command(name="newsletter", description="Get the latest articles from our feeds")
    async def newsletter(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        items = await self.fetch_rss_items()
        if items:
            for title, link in items:
                await interaction.channel.send(f"**{title}**\n<{link}>")
            await interaction.followup.send("Here are the latest articles from the feeds.", ephemeral=True)
        else:
            await interaction.followup.send("No new articles in the last 24 hours.")

    @nextcord.slash_command(name="list_newsletter_resources", description="List all newsletter resources.")
    async def list_newsletter_resources(self, interaction: nextcord.Interaction):
        response = self.newsletter_utils.get_resources()
        if response['status'] == 'ok' and response['data']:
            resources_list = "\n".join(f"{resource.id}: {resource.url}" for resource in response['data'])
            await interaction.response.send_message(resources_list or "No resources found.")
        else:
            await interaction.response.send_message("Failed to retrieve resources.")

    @nextcord.slash_command(name="add_newsletter_resource", description="Add a new newsletter resource.")
    async def add_newsletter_resource(self, interaction: nextcord.Interaction, url: str):
        response = self.newsletter_utils.create_resource(url)
        if response['status'] == 'ok':
            await interaction.response.send_message(response['message'])
        else:
            await interaction.response.send_message(response['message'])

    @nextcord.slash_command(name="update_newsletter_resource", description="Update an existing newsletter resource.")
    async def update_newsletter_resource(self, interaction: nextcord.Interaction, resource_id: int, new_url: str):
        response = self.newsletter_utils.update_resource(resource_id, new_url)
        if response['status'] == 'ok':
            await interaction.response.send_message(response['message'])
        else:
            await interaction.response.send_message(response['message'], ephemeral=True)


def setup(bot):
    bot.add_cog(Newsletter(bot))
