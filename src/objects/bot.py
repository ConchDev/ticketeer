import discord
from src.objects import StartupType
import dotenv
import os
import logging
from tortoise import Tortoise

dotenv.load_dotenv()

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.aiosqlite",
            "credentials": {
                "file_path": "database.db"
            },
        },
    },
    "apps": {
        "default": {
            "models": ["src.database.models", "aerich.models"],
        }
    }
},

class Bot(discord.Bot):
    def __init__(self, mode: StartupType):
        self.intents = discord.Intents.default()
        self.intents.members = True
        self.logger = logging.getLogger("discord")

        kwargs = {"intents": self.intents}

        if mode == StartupType.dev:
            kwargs["debug_guilds"] = os.getenv("DEBUG_GUILDS").split(",")

        super().__init__(**kwargs)
    
    async def on_connect(self):
        """
        Called when the bot connects to Discord.
        Connects to the database.
        """
        self.logger.info("Connected to Discord.")
        self.logger.info("Connecting to database...")

        await Tortoise.init(
            config=DB_CONFIG,
            use_tz=True
        )
        await Tortoise.generate_schemas()

        self.logger.info("Connected to database.")
    
    async def on_disconnect(self):
        """
        Called when the bot disconnects from Discord.
        Disconnects from the database to make sure no data is lost.
        """
        self.logger.info("Disconnected from Discord.")
        self.logger.info("Disconnecting from database...")
        await Tortoise.close_connections()

    async def on_ready(self):
        """
        Called when the bot is ready.
        """
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        self.logger.info("------")
    
    def load_cogs(self):
        """
        Loads all of the cogs in the src/cogs directory.
        """
        for filename in os.listdir("src/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"src.cogs.{filename[:-3]}")

    def run(self):
        """
        Loads the cogs and runs the bot.
        """
        self.load_cogs()
        super().run(os.getenv("TOKEN"), reconnect=True)