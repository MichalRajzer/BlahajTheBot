import os
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
import logging

from basic import Basic
from mod import Mod
from setup import Setup

# Load .env
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Set intents
intents = nextcord.Intents.default()
intents.message_content = True  # Needed for automod
intents.members = True


# Create bot
bot = commands.Bot(intents=intents,)

# Load cogs
bot.add_cog(Basic(bot))
bot.add_cog(Mod(bot))
bot.add_cog(Setup(bot))

# Run bot
if __name__ == '__main__':
    bot.run(os.getenv("BOT_TOKEN"))
