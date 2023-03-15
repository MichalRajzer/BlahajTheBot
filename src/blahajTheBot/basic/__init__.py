import nextcord
from nextcord.ext import commands
import logging


class Basic(commands.Cog):
    def __init__(self, bot):
        logging.info("Basic cog loaded!")
        self.bot = bot

    @nextcord.slash_command(description="pong!")
    async def ping(self, interaction: nextcord.Interaction) -> None:
        ping1 = f"{str(round(self.bot.latency * 1000))} ms"
        embed = nextcord.Embed(
            title="**Pong!**", description="**" + ping1 + "**", color=0x3477eb)
        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Bot is ready!")
        await self.bot.change_presence(activity=nextcord.Game("swimming in the ocean"))
