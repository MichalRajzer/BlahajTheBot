import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
import logging

from basic import Basic


logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

logging.basicConfig(level=logging.INFO)

load_dotenv()

intents = nextcord.Intents.default()
intents.message_content = True  # Needed for automod
bot = commands.Bot(intents=intents,)


bot.add_cog(Basic(bot))


bot.run(os.getenv("BOT_TOKEN"))
