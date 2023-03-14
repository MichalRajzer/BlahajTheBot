import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging


class Blahaj(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_handler = handler

    async def on_ready(self):
        logging.info("Bot is ready!")

    async def on_disconnect(self):
        logging.warning("Bot has disconnected!")


if __name__ == '__main__':
    load_dotenv()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    intents.presences = True

    handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='w')

    bot = Blahaj("/", intents=intents, log_handler=handler)
    bot.run(os.getenv('BOT_TOKEN'))
