import discord
import typing 
if typing.TYPE_CHECKING:
    from src.objects import Bot

class Listeners(discord.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    

def setup(bot: Bot):
    bot.add_cog(Listeners(bot))