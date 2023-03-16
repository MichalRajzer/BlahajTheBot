import nextcord
from nextcord.ext import commands
import logging


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("Basic cog loaded!")

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

    @commands.Cog.listener()
    async def on_connect(self):
        logging.info("Bot connected to Discord!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.warning("Bot disconnected from Discord!")

    @commands.Cog.listener()
    async def on_resumed(self):
        logging.info("Bot resumed connection to Discord!")

    @commands.Cog.listener()
    async def on_message(self, message):
        logging.debug(
            f"Message sent by {message.author} in {message.channel}: {message.content}")
