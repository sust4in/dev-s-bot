from nextcord.ext import commands
import nextcord
import feedparser
from datetime import datetime, timedelta


class Newsletter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.RSS_URLS = ['https://careercutler.substack.com/feed', 'https://www.developing.dev/feed',
                         'https://levelupsoftwareengineering.substack.com/feed', 'https://read.engineerscodex.com/feed',
                         'https://codingchallenges.substack.com/feed', 'https://blog.dataengineer.io/feed',
                         'https://newsletter.techleadmentor.com/feed', 'https://www.thecaringtechie.com/feed',
                         'https://refactoring.fm/feed', 'https://strategizeyourcareer.substack.com/feed',
                         'https://www.saiyangrowthletter.com/feed', 'https://tidyfirst.substack.com/feed',
                         'https://devinterrupted.substack.com/feed', 'https://newsletter.pragmaticengineer.com/feed',
                         'https://changelog.com/news/feed', 'https://newsletter.weskao.com/feed',
                         'https://newsletter.systemdesign.one/feed', 'https://blog.bytebytego.com/feed',
                         'https://bytesizeddesign.substack.com/feed', 'https://newsletter.francofernando.com/feed',
                         'https://sreweekly.com/feed/']

    async def fetch_rss_items(self):
        items = []
        for url in self.RSS_URLS:
            feed = feedparser.parse(url)
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


def setup(bot):
    bot.add_cog(Newsletter(bot))
