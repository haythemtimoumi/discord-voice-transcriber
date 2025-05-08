# main.py
import nextcord
from nextcord.ext import commands
import logging
import os
from dotenv import load_dotenv
import asyncio

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

load_dotenv()

intents = nextcord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.voice")
            logging.info("✅ Voice cog loaded")
        except Exception as e:
            logging.exception(f"❌ Failed to load cog: {e}")

bot = MyBot()

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.event
async def on_ready():
    logging.info(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')
    logging.info(f'✅ Connected to {len(bot.guilds)} guild(s)')
    logging.info(f'✅ Registered commands: {", ".join([cmd.name for cmd in bot.commands])}')

async def main():
    await bot.setup_hook()  # ✅ make sure hook is manually triggered
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No DISCORD_TOKEN in .env")
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
