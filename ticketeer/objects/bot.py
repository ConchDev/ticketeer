import discord
from ticketeer.objects.enums import StartupType
import dotenv
import os
import logging
from tortoise import Tortoise

dotenv.load_dotenv()

DB_CONFIG = {
    "connections": {
        "ticketeer": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": "ticketeer/database/database.db"
            },
        },
    },
    "apps": {
        "ticketeer": {
            "models": ["ticketeer.database.models", "aerich.models"],
            "default_connection": "ticketeer",
        }
    }
}


class Bot(discord.Bot):
    def __init__(self, mode: StartupType):
        intents = discord.Intents.default()
        intents.members = True
        self.logger = logging.getLogger("ticketeer")
        self.logger.warning("Discord.py is using an internal logger.")
        logging.basicConfig(level=logging.INFO)
        self.logger.warning("Ticketeer is using an internal logger.")


        kwargs = {"intents": intents}

        if mode == StartupType.dev:
            kwargs["debug_guilds"] = os.getenv("DEBUG_GUILDS").split(",")
            self.logger.setLevel(logging.DEBUG)

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
        await self.sync_commands()

    async def on_disconnect(self):
        """
        Called when the bot disconnects from Discord.
        Disconnects from the database to make sure no data is lost.
        """
        self.logger.info("Disconnected from Discord.")
        self.logger.info("Disconnecting from database...")
        await Tortoise.close_connections()
        self.logger.info("Disconnected from database.")

    async def close(self):
        """
        Closes the bot.
        """
        await super().close()
        await Tortoise.close_connections()

    async def on_ready(self):
        """
        Called when the bot is ready.
        """
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    def load_cogs(self):
        """
        Loads all of the cogs in the cogs directory.
        """
        for filename in os.listdir("ticketeer/cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"ticketeer.cogs.{filename[:-3]}")

    def run(self):
        """
        Loads the cogs and runs the bot.
        """
        self.load_cogs()
        super().run(os.getenv("TOKEN"), reconnect=True)
